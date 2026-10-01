"""Deterministic governance preflight for Humanity Loop high-impact actions."""

from __future__ import annotations

from typing import Any, Dict, List


def evaluate_governance_gate(proposal: Dict[str, Any]) -> Dict[str, Any]:
    """Return GO, HOLD, or BLOCK plus reasons.

    This does not replace human judgment. It enforces the minimum evidence,
    dissent, catastrophic-risk, containment, and approval checks documented in
    GOVERNANCE.md before a high-impact proposal can escalate.
    """
    reasons: List[str] = []

    high_impact = bool(proposal.get("high_impact"))
    if high_impact:
        if not proposal.get("evidence_verified"):
            reasons.append("independent evidence verification missing")
        if not proposal.get("dissent_review_completed"):
            reasons.append("10th-Man review missing")
        if proposal.get("dissent_block"):
            return {
                "decision": "BLOCK",
                "reasons": reasons + ["10th-Man identified a fatal flaw"],
            }
        if not proposal.get("rollback_plan") or not proposal.get("containment_plan"):
            reasons.append("rollback/containment check incomplete")

    catastrophic_triggers = list(proposal.get("catastrophic_risk_triggers") or [])
    if catastrophic_triggers:
        if not proposal.get("catastrophic_review_completed"):
            reasons.append("catastrophic-risk review missing")
        if proposal.get("catastrophic_veto"):
            return {
                "decision": "BLOCK",
                "reasons": reasons + ["Catastrophic-Risk Governor veto"],
            }

    if proposal.get("human_approval_required") and not proposal.get("human_approval_received"):
        reasons.append("required human approval missing")

    if reasons:
        return {"decision": "HOLD", "reasons": reasons}
    return {"decision": "GO", "reasons": []}
