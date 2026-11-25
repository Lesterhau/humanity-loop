import unittest
from pathlib import Path
from isolated_adapter import MODEL_SHA256,MODEL_ID,MODEL_ALIAS,MODEL_BYTES,MAX_PREDICT,MAX_TOTAL_SECONDS,STAGES
HERE=Path(__file__).resolve().parent
class ModelPinTests(unittest.TestCase):
    def test_model_identity_and_exact_pin(self):
        self.assertEqual(MODEL_ID,'Qwen/Qwen3-4B-Instruct-2507')
        self.assertEqual(MODEL_SHA256,'2fde00ce69dd4899c70d020845e2638353015bba0fdf161b3eb965f2bca4464e')
        self.assertEqual(MODEL_BYTES,2497280736)
    def test_shell_matches_pin(self):
        shell=(HERE/'run-ci.sh').read_text()
        for value in (MODEL_SHA256,MODEL_ALIAS,str(MODEL_BYTES),'https://huggingface.co/bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF/resolve/5ba9dff45461e5bab86959be7d585609fe9e6bc3/Qwen_Qwen3-4B-Instruct-2507-Q4_K_M.gguf','sha256sum','wc -c','--memory 6g','--cpus 4','--network none'):
            self.assertIn(value,shell)
        self.assertNotIn('SmolLM2',shell)
    def test_execution_bounds_unchanged(self):
        self.assertEqual(MAX_PREDICT,256)
        self.assertEqual(MAX_TOTAL_SECONDS,240)
        self.assertEqual(len(STAGES),8)

    def test_download_bound_separate_from_inference(self):
        shell=(HERE/'run-ci.sh').read_text()
        self.assertIn('--max-time 480 --max-filesize 2497280736',shell)
        self.assertIn('timeout --kill-after=5s 240s',shell)
        self.assertNotIn('--retry',shell)
        self.assertIn('--n-predict 256',shell)
        workflow=(HERE.parents[1]/'.github/workflows/g3-isolated-inference-once.yml').read_text()
        self.assertIn('timeout-minutes: 17',workflow)
        self.assertIn('github.run_attempt == 1',workflow)
