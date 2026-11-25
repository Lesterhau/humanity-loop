"""One-shot CI acceptance adapter: no remote provider, external tools or account."""
import json
import math
import time
import urllib.request
from pathlib import Path
from structured_scout import RESPONSE_FORMAT
from structured_decisions import response_format as decision_format

STAGES=('scout','verify','assign','build_act','dissent','safety','revision','outcome')
MODEL_SHA256='decd2598bc2c8ed08c19adc3c8fdd461ee19ed5708679d1c54ef54a5a30d4f33'
IMAGE='ghcr.io/ggml-org/llama.cpp:server-b9519@sha256:abaf7899e16b638411096f6db42563dffa876119037458b7986f2a6bde3df41e'
MAX_PREDICT=256
MAX_CONTEXT=4096
MAX_TOTAL_SECONDS=240
MAX_RESPONSE=65536

class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise ValueError('redirect_denied')

def verify_namespace(interfaces=Path('/proc/net/dev'),routes=Path('/proc/net/route'),ipv6=Path('/proc/net/ipv6_route')):
    names={line.split(':',1)[0].strip() for line in interfaces.read_text().splitlines()[2:] if ':' in line}
    if names!={'lo'}: raise ValueError('network_namespace_not_isolated')
    if any(row.split()[0]!='lo' for row in routes.read_text().splitlines()[1:] if row.strip()):
        raise ValueError('external_ipv4_route')
    if ipv6.exists() and any(row.split()[-1]!='lo' for row in ipv6.read_text().splitlines() if row.strip()):
        raise ValueError('external_ipv6_route')

def safe_diagnostic(stage, phase, response, exc):
    """Fixed vocabulary and bounded scalar metadata only; never log model text."""
    r=response if isinstance(response,dict) else {}
    choices=r.get('choices')
    choice=choices[0] if isinstance(choices,list) and choices and isinstance(choices[0],dict) else {}
    usage=r.get('usage')
    usage=usage if isinstance(usage,dict) else {}
    msg=choice.get('message')
    msg=msg if isinstance(msg,dict) else {}
    def bounded_int(v):
        return v if type(v) is int and 0<=v<=16384 else None
    finish=choice.get('finish_reason')
    return {
        'stage':stage if stage in STAGES else 'unknown',
        'phase':phase if phase in ('transport','deadline','response_shape','token_receipt','model_identity','finish_reason','message_shape') else 'unknown',
        'exception':type(exc).__name__ if type(exc).__name__ in ('ValueError','KeyError','IndexError','TypeError','TimeoutError','HTTPError','URLError','JSONDecodeError','OSError') else 'other',
        'http_status':bounded_int(getattr(exc,'code',None)) if type(getattr(exc,'code',None)) is int and 100<=exc.code<=599 else None,
        'response_object':isinstance(response,dict),
        'choice_count':bounded_int(len(choices)) if isinstance(choices,list) else None,
        'model_alias_matches':r.get('model')=='hl-pinned-smollm2',
        'finish_reason':finish if isinstance(finish,str) and finish in ('stop','length','tool_calls','content_filter') else 'missing_or_other',
        'prompt_tokens':bounded_int(usage.get('prompt_tokens')),
        'completion_tokens':bounded_int(usage.get('completion_tokens')),
        'total_tokens':bounded_int(usage.get('total_tokens')),
        'assistant_role':msg.get('role')=='assistant',
        'nonempty_text':isinstance(msg.get('content'),str) and bool(msg['content'].strip()),
        'tool_calls_present':bool(msg.get('tool_calls')),
    }

class IsolatedLlama:
    def __init__(self,*,transport=None,clock=time.monotonic):
        self.opener=urllib.request.build_opener(NoRedirects,urllib.request.ProxyHandler({}))
        self.transport=transport or self._request
        self.clock=clock
        self.started=clock()
        self.attempted=[]
        self.receipts=[]
        self.failed=False
        self.last_failure=None
    def _request(self,payload,timeout):
        req=urllib.request.Request('http://127.0.0.1:8080/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
        with self.opener.open(req,timeout=timeout) as r:
            if r.status!=200: raise ValueError('inference_http_failed')
            data=r.read(MAX_RESPONSE+1)
            if len(data)>MAX_RESPONSE: raise ValueError('response_too_large')
            return json.loads(data)
    def __call__(self,stage,prompt,timeout):
        if self.failed or len(self.attempted)>=len(STAGES) or stage!=STAGES[len(self.attempted)]:
            raise ValueError('duplicate_or_out_of_order_call')
        if not isinstance(prompt,str) or not 0<len(prompt)<=12000: raise ValueError('invalid_prompt')
        if type(timeout) not in (int,float) or not math.isfinite(timeout) or timeout<=0: raise ValueError('invalid_timeout')
        remaining=MAX_TOTAL_SECONDS-(self.clock()-self.started)
        if remaining<=0: raise TimeoutError('deadline_exhausted')
        self.attempted.append(stage)
        r=None
        phase='transport'
        try:
            payload={'model':'hl-pinned-smollm2','messages':[{'role':'user','content':prompt}],'max_tokens':MAX_PREDICT,'temperature':0,'stream':False}
            if stage=='scout':
                payload['response_format']=RESPONSE_FORMAT
            elif stage in ('verify','safety'):
                payload['response_format']=decision_format(stage)
            r=self.transport(payload,min(timeout,45,remaining))
            phase='deadline'
            if self.clock()-self.started>MAX_TOTAL_SECONDS: raise TimeoutError('deadline_exhausted')
            phase='response_shape'
            choice=r['choices'][0]
            phase='token_receipt'
            usage=r['usage']; inp,out,total=(usage[k] for k in ('prompt_tokens','completion_tokens','total_tokens'))
            if any(type(n) is not int for n in (inp,out,total)) or not 0<inp<=MAX_CONTEXT or not 0<out<=MAX_PREDICT or total!=inp+out or total>MAX_CONTEXT:
                raise ValueError('invalid_token_receipt')
            phase='model_identity'
            if r.get('model')!='hl-pinned-smollm2' or len(r['choices'])!=1:
                raise ValueError('wrong_model_or_choice_count')
            phase='finish_reason'
            if choice.get('finish_reason')!='stop':
                raise ValueError('incomplete_generation')
            phase='message_shape'
            msg=choice['message']; response=msg.get('content')
            if msg.get('role')!='assistant' or msg.get('tool_calls') or not isinstance(response,str) or not 0<len(response.strip())<=8000:
                raise ValueError('invalid_model_text')
            self.receipts.append({'stage':stage,'input_tokens':inp,'output_tokens':out,'total_tokens':total,'finish_reason':'stop'})
            return response
        except Exception as exc:
            self.failed=True
            self.last_failure=safe_diagnostic(stage,phase,r,exc)
            raise
