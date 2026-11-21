"""Offline-only Foundry Lite laptop readiness tests (no Ollama or model calls)."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from foundry_lite_doctor import GIB, diagnose

class LaptopDoctorTests(unittest.TestCase):
    def test_windows_command_does_not_require_unix_tmp_or_python3_name(self):
        r=diagnose(system="Windows",python=(3,12),ram=16*GIB,disk=20*GIB,ollama_executable="C:/Program Files/Ollama/ollama.exe")
        self.assertEqual(r["status"],"inspect_ready")
        self.assertTrue(r["zero_model_inspect_command"].startswith("py -3 "))
        self.assertIn("foundry-lite-inspection.json",r["zero_model_inspect_command"])
        self.assertNotIn("/tmp/",r["zero_model_inspect_command"])
        self.assertEqual(r["model_calls"],0)
        self.assertEqual(r["appdeploy_credits_used"],0)
        self.assertFalse(r["automated_download"])
        self.assertFalse(r["scheduler_created"])

    def test_mac_local_model_probe_is_explicit_and_read_only(self):
        calls=[]
        def probe():
            calls.append("local")
            return "local_service_ready",["qwen3:4b-instruct"]
        base=dict(system="Darwin",python=(3,13),ram=16*GIB,disk=50*GIB,
                  ollama_executable="/usr/local/bin/ollama",local_probe=probe)
        no_probe=diagnose(**base)
        self.assertEqual(calls,[])
        self.assertEqual(no_probe["installed_models"],[])
        self.assertEqual(no_probe["network_access"],"none")
        checked=diagnose(check_local=True,**base)
        self.assertEqual(calls,["local"])
        self.assertEqual(checked["installed_models"],["qwen3:4b-instruct"])
        self.assertEqual(checked["network_access"],"only optional loopback GET /api/tags")
        self.assertEqual(checked["status"],"inspect_ready")

    def test_missing_ollama_and_small_ram_is_not_assumed_working(self):
        r=diagnose(system="Linux",python=(3,11),ram=4*GIB,disk=3*GIB,
                   ollama_executable="")
        self.assertEqual(r["status"],"ollama_not_installed")
        self.assertEqual(r["ram_guidance"],"limited_capacity")
        self.assertEqual(r["local_service"],"not_checked")
        self.assertEqual(r["installed_models"],[])

    def test_local_service_failure_is_reported_without_fallback(self):
        r=diagnose(system="Windows",python=(3,12),ram=8*GIB,disk=50*GIB,
                   ollama_executable="ollama.exe",check_local=True,
                   local_probe=lambda:("local_service_unavailable",[]))
        self.assertEqual(r["status"],"local_service_unavailable")
        self.assertEqual(r["model_calls"],0)
        self.assertEqual(r["appdeploy_credits_used"],0)

    def test_old_python_denied(self):
        r=diagnose(system="Linux",python=(3,9),ram=16*GIB,disk=50*GIB,
                   ollama_executable="ollama")
        self.assertEqual(r["status"],"python_update_needed")
        self.assertFalse(r["python_supported"])
        self.assertEqual(r["network_access"],"none")

    def test_machine_summary_json_serializable_and_no_private_process_data(self):
        r=diagnose(system="Linux",python=(3,12),ram=12*GIB,disk=25*GIB,
                   ollama_executable="/usr/bin/ollama")
        data=json.dumps(r)
        self.assertNotIn("last_pass",data)
        self.assertEqual(r["ram_guidance"],"small_model_likely")
        self.assertNotIn("/usr/bin/ollama",data)

if __name__=="__main__":
    unittest.main()
