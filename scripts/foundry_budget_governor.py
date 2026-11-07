"""Provider-neutral, fail-closed Foundry admission policy.

This module is offline and has no model/HTTP/database side effects. It is a
reference admission gate for provider adapters, NOT a live account-wide cap.
Every executing adapter must implement an atomic one-use reservation, actual
provider-level hard stopping, call/token counters and durable receipts.

Until the provider's enforceable spending limit is verified, AI execution
is DENIED. Hosting a second mirror cannot evade these conditions.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Optional


@dataclass(frozen=True)
class AccountSnapshot:
    remaining_credits: str
    observed_at: datetime
    reset_at: datetime
    plan: str
    provider: str
    source: str

    def parsed_balance(self) -> Decimal:
        try:
            result = Decimal(self.remaining_credits)
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Invalid credit balance")
        if not result.is_finite() or result < 0:
            raise ValueError("Invalid credit balance")
        return result


@dataclass(frozen=True)
class WorkRequest:
    task_id: str
    risk_tier: int
    model_calls: int
    max_input_tokens_per_call: int
    max_output_tokens_per_call: int
    run_seconds: int
    max_total_credits: str
    manually_approved: bool
    idempotency_key: str
    external_actions: bool = False
    automatic_retry: bool = False


@dataclass(frozen=True)
class GovernorConfig:
    reserve_credits: str = "350"
    snapshot_max_age_minutes: int = 60
    max_model_calls: int = 2
    max_input_tokens: int = 3000
    max_output_tokens: int = 512
    max_run_seconds: int = 120
    max_run_credits: str = "5"


@dataclass(frozen=True)
class Admission:
    permitted: bool
    reason: str
    remaining_after_ceiling: Optional[str] = None


def _valid_utc(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def decide(
    snapshot: AccountSnapshot,
    request: WorkRequest,
    *,
    now: datetime,
    config: GovernorConfig = GovernorConfig(),
    provider_spending_cap_verified: bool = False,
    provider_cost_upper_bound_verified: bool = False,
    atomic_lease_verified: bool = False,
) -> Admission:
    """Check strict eligibility BEFORE any external work or AI call.

    This does not itself reserve credits or lease a task. Hosts MUST make an
    atomic reservation against the authoritative ledger and recheck current
    conditions immediately before model invocation. Other apps sharing the
    same account can consume credits asynchronously, so token ceilings alone
    cannot enforce the reserve.
    """
    deny = lambda code: Admission(False, code)
    if not _valid_utc(now) or not _valid_utc(snapshot.observed_at) or not _valid_utc(snapshot.reset_at):
        return deny("untrusted_timestamp")
    if now.tzinfo is None:
        return deny("untrusted_timestamp")
    if snapshot.observed_at > now + timedelta(minutes=1):
        return deny("future_snapshot")
    age = now - snapshot.observed_at
    if age > timedelta(minutes=config.snapshot_max_age_minutes):
        return deny("stale_credit_snapshot")
    if now >= snapshot.reset_at:
        return deny("credit_cycle_unknown")
    if snapshot.plan.lower() != "free":
        return deny("not_zero_cash_plan")
    if not snapshot.provider.strip() or not snapshot.source.strip():
        return deny("missing_credit_provenance")
    if not request.task_id.strip() or not request.idempotency_key.strip():
        return deny("missing_task_or_idempotency_key")
    if request.risk_tier != 0:
        return deny("tier_not_permitted")
    if not request.manually_approved:
        return deny("owner_approval_missing")
    if request.external_actions or request.automatic_retry:
        return deny("unapproved_external_action_or_retry")
    if not (1 <= request.model_calls <= config.max_model_calls):
        return deny("model_call_limit")
    if not (1 <= request.max_input_tokens_per_call <= config.max_input_tokens):
        return deny("input_token_limit")
    if not (1 <= request.max_output_tokens_per_call <= config.max_output_tokens):
        return deny("output_token_limit")
    if not (1 <= request.run_seconds <= config.max_run_seconds):
        return deny("runtime_limit")
    try:
        balance = snapshot.parsed_balance()
        ceiling = Decimal(request.max_total_credits)
        reserve = Decimal(config.reserve_credits)
        cap = Decimal(config.max_run_credits)
    except (InvalidOperation, TypeError, ValueError):
        return deny("invalid_credit_budget")
    if any(not n.is_finite() for n in (ceiling, reserve, cap)):
        return deny("invalid_credit_budget")
    if reserve < 0 or cap <= 0 or ceiling <= 0 or ceiling > cap:
        return deny("credit_run_limit")
    if balance - ceiling < reserve:
        return deny("protected_reserve")
    if not provider_spending_cap_verified:
        return deny("provider_hard_stop_unverified")
    if not provider_cost_upper_bound_verified:
        return deny("provider_cost_bound_unverified")
    if not atomic_lease_verified:
        return deny("authoritative_atomic_lease_unverified")
    return Admission(True, "eligible_for_atomic_reservation", str(balance - ceiling))


def deterministic_only(*, task_id: str, external_actions: bool = False) -> Admission:
    """A separate zero-AI route; execution still needs an authorized task.

    Does not authorize public outreach, production mutations, or paid HTTP APIs.
    """
    if not task_id.strip() or external_actions:
        return Admission(False, "deterministic_scope_denied")
    return Admission(True, "zero_model_calls_only")
