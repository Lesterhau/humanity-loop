"""One-shot public source snapshot: offline fixtures and network boundary tests."""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from public_source_snapshot import (
    MAX_BYTES, global_ips, normalized_visible_text, one_public_html_get,
    source_snapshot, validate_target, main,
)

ROOT=Path(__file__).resolve().parent.parent
TASK=json.loads((ROOT/"foundry-lite/fixtures/ot013-pk-climate-review.json").read_text(encoding="utf-8"))
HTML=b"""<!DOCTYPE html><html><head><title>Pakistan project</title>
<script>const secret='84 of the 117 schools at Priority 1-2 (81.6%)';</script></head>
<body><h2>Summary</h2>
<p>103 (0.2%)</p><p>Compounding high risk</p>
<p>Gujrat, Sialkot, Sheikhupura, and Gujranwala contain
84 of the 117 schools at Priority 1-2 for both hazards (81.6%).</p>
<p>The chart shows where the 117 compounding Priority 1-2 schools are concentrated.</p>
</body></html>"""
AT=datetime(2026,11,22,23,0,tzinfo=timezone.utc)
SOURCE="https://city.lums.edu.pk/what-we-do/city-research/dare-rc/"

class FakeResponse:
    def __init__(self,status=200,body=HTML,content_type="text/html",content_length=None):
        self.status=status
        self.body=body
        self.content_type=content_type
        self.content_length=content_length
    def getheader(self,k,default=None):
        if k=="Content-Type": return self.content_type
        if k=="Content-Length": return self.content_length
        return default
    def read(self,n): return self.body[:n]

class FakeConnection:
    def __init__(self,host,ip,timeout):
        self.host,self.ip,self.timeout=host,ip,timeout
        self.requests=[]
        self.response=FakeResponse()
        self.closed=False
    def request(self,method,path,headers):
        self.requests.append((method,path,headers))
    def getresponse(self): return self.response
    def close(self): self.closed=True

class SourceSnapshotTests(unittest.TestCase):
    def fetch(self,url):
        self.assertEqual(url,SOURCE)
        return HTML,"text/html"

    def test_default_requires_explicit_live_public_get(self):
        called=[]
        with self.assertRaisesRegex(ValueError,"live_public_get_requires_explicit_opt_in"):
            source_snapshot("OT-013",TASK,allow_live_get=False,
                            get=lambda u:called.append(u))
        self.assertEqual(called,[])

    def test_direct_public_response_snapshot_never_claims_human_verification(self):
        r=source_snapshot("OT-013",TASK,allow_live_get=True,get=self.fetch,
                          observed_at=AT)
        self.assertEqual(r["source_url"],SOURCE)
        self.assertEqual(r["raw_sha256"],hashlib.sha256(HTML).hexdigest())
        self.assertEqual(r["raw_bytes"],len(HTML))
        self.assertEqual(r["observed_at_utc"],"2026-11-22T23:00:00Z")
        self.assertTrue(r["indicators"]["headline_103"]["observed_in_visible_html"])
        self.assertTrue(r["indicators"]["narrative_117"]["observed_in_visible_html"])
        self.assertTrue(r["indicators"]["narrative_81_6"]["observed_in_visible_html"])
        self.assertEqual(r["arithmetic"]["computed_percent_1dp"],"71.8")
        self.assertEqual(r["arithmetic"]["source_claim_percent"],"81.6")
        self.assertTrue(r["arithmetic"]["arithmetic_discrepancy_candidate"])
        self.assertFalse(r["arithmetic"]["underlying_cohort_truth_verified"])
        self.assertFalse(r["independently_reviewed"])
        self.assertFalse(r["eligible_for_win_ledger"])
        self.assertEqual(r["model_calls"],0)
        self.assertEqual(r["appdeploy_credits_used"],0)
        self.assertEqual(r["external_write_actions"],0)
        self.assertFalse(r["scheduled"])

    def test_html_script_text_is_excluded_from_visible_evidence(self):
        raw=b'<html><script>84 of the 117 schools (81.6%)</script><p>103 (0.2%)</p></html>'
        text=normalized_visible_text(raw)
        self.assertNotIn("84 of the 117",text)
        self.assertEqual(text,"103 (0.2%)")
        x=source_snapshot("OT-013",TASK,allow_live_get=True,
                          get=lambda u:(raw,"text/html"),observed_at=AT)
        self.assertIsNone(x["arithmetic"])

    def test_unknown_case_or_unapproved_url_and_locale_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"case_not_source_allowlisted"):
            validate_target("OT-003",TASK)
        for key,val in [
            ("country","US"),
            ("languages",["ur"]),
            ("case_id","OT-003"),
            ("public_source_urls",["https://elsewhere.example.org/public"]),
        ]:
            task=deepcopy(TASK);task[key]=val
            with self.subTest(key=key),self.assertRaises(ValueError):
                validate_target("OT-013",task)

    def test_public_only_resolver_refuses_private_and_mixed_dns(self):
        public=lambda *args,**kwargs:[(socket.AF_INET,socket.SOCK_STREAM,6,"",("8.8.8.8",443))]
        mixed=lambda *args,**kwargs:[
            (socket.AF_INET,socket.SOCK_STREAM,6,"",("8.8.8.8",443)),
            (socket.AF_INET,socket.SOCK_STREAM,6,"",("127.0.0.1",443))
        ]
        self.assertEqual(global_ips("city.lums.edu.pk",resolver=public),["8.8.8.8"])
        with self.assertRaisesRegex(ValueError,"source_dns_private_address"):
            global_ips("city.lums.edu.pk",resolver=mixed)
        with self.assertRaisesRegex(ValueError,"source_dns_unavailable"):
            global_ips("city.lums.edu.pk",resolver=lambda *a,**k:[])

    def test_one_bounded_get_no_redirect_no_proxy_no_credentials(self):
        instances=[]
        def factory(host,ip,timeout):
            c=FakeConnection(host,ip,timeout);instances.append(c);return c
        resolver=lambda *args,**kwargs:[(socket.AF_INET,socket.SOCK_STREAM,6,"",("8.8.8.8",443))]
        body,media=one_public_html_get(SOURCE,resolver=resolver,connection_factory=factory)
        self.assertEqual(body,HTML)
        self.assertEqual(media,"text/html")
        self.assertEqual(instances[0].host,"city.lums.edu.pk")
        self.assertEqual(instances[0].ip,"8.8.8.8")
        self.assertTrue(instances[0].closed)
        method,path,headers=instances[0].requests[0]
        self.assertEqual(method,"GET")
        self.assertEqual(path,"/what-we-do/city-research/dare-rc/")
        self.assertEqual(headers["Accept-Encoding"],"identity")
        self.assertNotIn("Cookie",headers)
        self.assertNotIn("Authorization",headers)

    def test_reject_redirect_non_html_and_large_response(self):
        resolver=lambda *args,**kwargs:[(socket.AF_INET,socket.SOCK_STREAM,6,"",("8.8.8.8",443))]
        cases=[
            (FakeResponse(status=302), "source_http_non_200"),
            (FakeResponse(content_type="application/json"), "source_non_html_response"),
            (FakeResponse(content_length=str(MAX_BYTES+1)), "source_response_too_large"),
            (FakeResponse(body=b"X"*(MAX_BYTES+1)), "source_response_too_large"),
        ]
        for response,error in cases:
            with self.subTest(error=error),self.assertRaisesRegex(ValueError,error):
                def factory(host,ip,timeout):
                    c=FakeConnection(host,ip,timeout);c.response=response;return c
                one_public_html_get(SOURCE,resolver=resolver,connection_factory=factory)

    def test_empty_invalid_or_bad_encoding_fails(self):
        for raw,content,error in [
            (b"","text/html","source_response_too_large_or_invalid"),
            (b"xxx","application/pdf","source_non_html_response"),
            (b"\xff\xfe","text/html","source_encoding_not_supported"),
        ]:
            with self.subTest(raw=raw),self.assertRaisesRegex(ValueError,error):
                source_snapshot("OT-013",TASK,allow_live_get=True,
                                get=lambda u:(raw,content),observed_at=AT)

    def test_source_is_must_not_be_dynamic_user_supplied_url(self):
        task=deepcopy(TASK)
        task["public_source_urls"].append("https://city.lums.edu.pk/admin")
        with self.assertRaisesRegex(ValueError,"task_exact_source_not_approved"):
            validate_target("OT-013",task)

    def test_timestamps_must_be_utc(self):
        with self.assertRaisesRegex(ValueError,"observation_time_must_be_utc"):
            source_snapshot("OT-013",TASK,allow_live_get=True,get=self.fetch,
                            observed_at=datetime(2026,11,22,22,0))

    def test_main_without_opt_in_never_creates_output(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"out.json"
            result=main(["--case","OT-013","--task",str(ROOT/"foundry-lite/fixtures/ot013-pk-climate-review.json"),
                         "--output",str(p)])
            self.assertEqual(result,2)
            self.assertFalse(p.exists())

if __name__=="__main__":
    unittest.main()
