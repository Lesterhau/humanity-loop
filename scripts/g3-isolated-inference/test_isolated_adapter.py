import unittest
from isolated_adapter import *
from tempfile import TemporaryDirectory

def good():
    return {'model':'hl-pinned-qwen3-4b-instruct-2507','choices':[{'finish_reason':'stop','message':{'role':'assistant','content':'Review draft'}}],'usage':{'prompt_tokens':500,'completion_tokens':10,'total_tokens':510}}
class TestAdapter(unittest.TestCase):
    def test_eight_calls_and_ninth_denied(self):
        a=IsolatedLlama(transport=lambda p,t:good())
        for s in STAGES:self.assertEqual(a(s,'prompt',5),'Review draft')
        self.assertEqual(len(a.receipts),8)
        with self.assertRaises(ValueError):a('scout','p',5)
    def test_out_of_order(self):
        a=IsolatedLlama(transport=lambda p,t:self.fail('called'))
        with self.assertRaises(ValueError):a('verify','p',5)
    def test_duplicate(self):
        a=IsolatedLlama(transport=lambda p,t:good());a('scout','p',5)
        with self.assertRaises(ValueError):a('scout','p',5)
    def test_no_retries(self):
        def fail(p,t):raise OSError()
        a=IsolatedLlama(transport=fail)
        with self.assertRaises(OSError):a('scout','p',5)
        with self.assertRaises(ValueError):a('verify','p',5)
    def test_malformed_response(self):
        for mutate in [lambda r:r.pop('usage'),lambda r:r.update(model='remote'),lambda r:r['usage'].update(completion_tokens=257),lambda r:r['usage'].update(completion_tokens=True),lambda r:r['usage'].update(total_tokens=2),lambda r:r['choices'][0].update(finish_reason='length'),lambda r:r['choices'][0]['message'].update(tool_calls=[{}]),lambda r:r['choices'][0]['message'].update(content=' ')]:
            r=good();mutate(r);a=IsolatedLlama(transport=lambda p,t:r)
            with self.subTest(r=r),self.assertRaises((ValueError,KeyError)):a('scout','p',5)
            self.assertEqual(a.receipts,[])
    def test_payload_limit(self):
        def t(p,timeout):
            self.assertEqual(p['max_tokens'],256);self.assertEqual(p['model'],'hl-pinned-qwen3-4b-instruct-2507');self.assertFalse(p['stream']);self.assertNotIn('tools',p);return good()
        IsolatedLlama(transport=t)('scout','p',5)
    def test_invalid_prompt_and_time(self):
        for prompt,timeout in [('',5),('x'*12001,5),('p',float('nan')),('p',True),('p',-1)]:
            a=IsolatedLlama(transport=lambda p,t:self.fail('called'))
            with self.assertRaises(ValueError):a('scout',prompt,timeout)
    def test_deadline(self):
        times=iter([0,241]);a=IsolatedLlama(transport=lambda p,t:self.fail('called'),clock=lambda:next(times))
        with self.assertRaises(TimeoutError):a('scout','p',5)
    def test_namespace(self):
        with TemporaryDirectory() as d:
            p=Path(d);net=p/'net';net.write_text('header\nheader\n lo: 0 0\n');route=p/'route';route.write_text('Iface Destination\n');v6=p/'v6';v6.write_text('000 00 000 00 000 0 0 0 0 lo\n');verify_namespace(net,route,v6);net.write_text('header\nheader\n lo: 0 0\n eth0: 0 0\n')
            with self.assertRaises(ValueError):verify_namespace(net,route,v6)
    def test_redirect(self):
        with self.assertRaises(ValueError):NoRedirects().redirect_request(None,None,None,None,None,None)

    def test_finish_length_reason_preserved_without_text(self):
        r=good()
        r['choices'][0]['finish_reason']='length'
        r['choices'][0]['message']['content']='PRIVATE_DIAGNOSTIC_SENTINEL'
        a=IsolatedLlama(transport=lambda p,t:r)
        with self.assertRaises(ValueError): a('scout','p',5)
        self.assertEqual(a.last_failure['phase'],'finish_reason')
        self.assertEqual(a.last_failure['finish_reason'],'length')
        self.assertEqual(a.last_failure['completion_tokens'],10)
        self.assertNotIn('PRIVATE_DIAGNOSTIC_SENTINEL',json.dumps(a.last_failure))
        self.assertTrue(a.failed)
        self.assertEqual(a.receipts,[])
    def test_identity_and_token_failures_distinct(self):
        for mutate,phase in [(lambda r:r.update(model='PRIVATE_SENTINEL'),'model_identity'),(lambda r:r['usage'].update(total_tokens=0),'token_receipt')]:
            r=good();mutate(r);a=IsolatedLlama(transport=lambda p,t:r)
            with self.assertRaises(ValueError):a('scout','p',5)
            self.assertEqual(a.last_failure['phase'],phase)
            self.assertNotIn('PRIVATE_SENTINEL',json.dumps(a.last_failure))
    def test_exception_message_not_logged(self):
        def fail(p,t):raise ValueError('PRIVATE_TRANSPORT_SENTINEL')
        a=IsolatedLlama(transport=fail)
        with self.assertRaises(ValueError):a('scout','p',5)
        self.assertEqual(a.last_failure['phase'],'transport')
        self.assertNotIn('PRIVATE_TRANSPORT_SENTINEL',json.dumps(a.last_failure))
    def test_malformed_diagnostic_fields_safe(self):
        r={'choices':[{'finish_reason':{'private':'SENTINEL'},'message':{'content':{'private':'SENTINEL'}}}],'usage':{'prompt_tokens':True,'completion_tokens':9999999,'total_tokens':'SENTINEL'}}
        d=safe_diagnostic('scout','token_receipt',r,ValueError('SENTINEL'))
        self.assertIsNone(d['prompt_tokens'])
        self.assertIsNone(d['completion_tokens'])
        self.assertIsNone(d['total_tokens'])
        self.assertNotIn('SENTINEL',json.dumps(d))

    def test_per_call_elapsed_limit_fails_closed(self):
        times=iter([0,0,46,46])
        a=IsolatedLlama(transport=lambda p,t:good(),clock=lambda:next(times))
        with self.assertRaises(TimeoutError): a('scout','p',45)
        self.assertEqual(a.receipts,[])
        self.assertEqual(a.last_failure['elapsed_ms'],46000)
        self.assertEqual(a.last_failure['call_limit_ms'],45000)
        self.assertTrue(a.failed)
    def test_success_timing_and_remaining_budget(self):
        times=iter([0,230,238])
        limits=[]
        def transport(p,t):
            limits.append(t)
            return good()
        a=IsolatedLlama(transport=transport,clock=lambda:next(times))
        a('scout','p',45)
        self.assertEqual(limits,[10])
        self.assertEqual(a.receipts[0]['elapsed_ms'],8000)
        self.assertEqual(a.receipts[0]['call_limit_ms'],10000)
