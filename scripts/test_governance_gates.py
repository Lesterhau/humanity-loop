import unittest

from governance_gates import evaluate_governance_gate


class GovernanceGateTests(unittest.TestCase):
    def test_clean_reversible_low_risk_work_can_go(self):
        self.assertEqual(
            evaluate_governance_gate({"high_impact": False})["decision"],
            "GO",
        )

    def test_missing_independent_verification_holds_high_impact_work(self):
        result = evaluate_governance_gate({
            "high_impact": True,
            "evidence_verified": False,
            "dissent_review_completed": True,
            "dissent_block": False,
            "rollback_plan": True,
            "containment_plan": True,
        })
        self.assertEqual(result["decision"], "HOLD")
        self.assertIn("independent evidence verification missing", result["reasons"])

    def test_dissent_agent_can_block_consensus(self):
        result = evaluate_governance_gate({
            "high_impact": True,
            "evidence_verified": True,
            "dissent_review_completed": True,
            "dissent_block": True,
            "rollback_plan": True,
            "containment_plan": True,
        })
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("10th-Man identified a fatal flaw", result["reasons"])

    def test_catastrophic_governor_can_veto(self):
        result = evaluate_governance_gate({
            "high_impact": True,
            "evidence_verified": True,
            "dissent_review_completed": True,
            "dissent_block": False,
            "rollback_plan": True,
            "containment_plan": True,
            "catastrophic_risk_triggers": ["critical-infrastructure"],
            "catastrophic_review_completed": True,
            "catastrophic_veto": True,
        })
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("Catastrophic-Risk Governor veto", result["reasons"])

    def test_missing_rollback_or_containment_holds(self):
        result = evaluate_governance_gate({
            "high_impact": True,
            "evidence_verified": True,
            "dissent_review_completed": True,
            "dissent_block": False,
            "rollback_plan": False,
            "containment_plan": True,
        })
        self.assertEqual(result["decision"], "HOLD")

    def test_required_human_approval_holds_until_received(self):
        result = evaluate_governance_gate({
            "high_impact": False,
            "human_approval_required": True,
            "human_approval_received": False,
        })
        self.assertEqual(result["decision"], "HOLD")


if __name__ == "__main__":
    unittest.main()
