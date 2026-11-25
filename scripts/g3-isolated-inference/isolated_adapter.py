"""One-shot CI acceptance adapter: no remote provider, external tools or account."""
import json
import math
import time
import urllib.request
from pathlib import Path

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

class IsolatedLlama:
    def __init__(self,*,transport=None,clock=time.monotonic):
        self.opener=urllib.request.build_opener(NoRedirects,urllib.request.ProxyHandler({}))
        self.transport=transport or self._request
        self.clock=clock
        self.started=clock()
        self.attempted=[]
        self.receipts=[]
        self.failed=False
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
        try:
            r=self.transport({'model':'hl-pinned-smollm2','messages':[{'role':'user','content':prompt}],'max_tokens':MAX_PREDICT,'temperature':0,'stream':False},min(timeout,45,remaining))
            if self.clock()-self.started>MAX_TOTAL_SECONDS: raise TimeoutError('deadline_exhausted')
            choice=r['choices'][0]
            usage=r['usage']; inp,out,total=(usage[k] for k in ('prompt_tokens','completion_tokens','total_tokens'))
            if any(type(n) is not int for n in (inp,out,total)) or not 0<inp<=MAX_CONTEXT or not 0<out<=MAX_PREDICT or total!=inp+out or total>MAX_CONTEXT:
                raise ValueError('invalid_token_receipt')
            if r.get('model')!='hl-pinned-smollm2' or len(r['choices'])!=1 or choice.get('finish_reason')!='stop':
                raise ValueError('wrong_model_or_incomplete_generation')
            msg=choice['message']; response=msg.get('content')
            if msg.get('role')!='assistant' or msg.get('tool_calls') or not isinstance(response,str) or not 0<len(response.strip())<=8000:
                raise ValueError('invalid_model_text')
            self.receipts.append({'stage':stage,'input_tokens':inp,'output_tokens':out,'total_tokens':total,'finish_reason':'stop'})
            return response
        except Exception:
            self.failed=True
            raise
