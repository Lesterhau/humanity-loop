"""Offline checks: these tests MUST NOT call an AI provider or external API."""
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from foundry_budget_governor import (
    AccountSnapshot, GovernorConfig, WorkRequest, decide, deterministic_only,
)


class BudgetGovernorTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 6, 18, 0, tzinfo=timezone.utc)
        self.snapshot = AccountSnapshot(
            remaining_credits="337.528024209",
            observed_at=self.now,
            reset_at=self.now + timedelta(days=20),
            plan="free",
            provider="AppDeploy",
            source="account_overview_read_only",
        )
        self.request = WorkRequest(
            task_id="test_task_001", risk_tier=0, model_calls=1,
            max_input_tokens_per_call=1000, max_output_tokens_per_call=128,
            run_seconds=30, max_total_credits="1",
            manually_approved=True, idempotency_key="task-test-001",
        )
        self.all_verified = dict(
            provider_spending_cap_verified=True,
            provider_cost_upper_bound_verified=True,
            atomic_lease_verified=True,
        )

    def decision(self, **flags):
        return decide(self.snapshot, self.request, now=self.now,
                      **(flags if flags else self.all_verified))

    def test_known_nov6_balance_denied_below_350_reserve(self):
        result = self.decision()
        self.assertFalse(result.permitted)
        self.assertEqual(result.reason, "protected_reserve")

    def test_above_reserve_still_denies_without_hard_provider_cap(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        decision = decide(snapshot, self.request, now=self.now)
        self.assertEqual(decision.reason, "provider_hard_stop_unverified")

    def test_after_hard_cap_cost_bound_and_lease_verified_allows_reservation_only(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        decision = decide(snapshot, self.request, now=self.now, **self.all_verified)
        self.assertTrue(decision.permitted)
        self.assertEqual(decision.remaining_after_ceiling, "399")
        self.assertEqual(decision.reason, "eligible_for_atomic_reservation")

    def test_denies_stale_snapshots_and_expired_cycle(self):
        snapshot = replace(self.snapshot, remaining_credits="400",
                           observed_at=self.now - timedelta(minutes=61))
        result = decide(snapshot, self.request, now=self.now, **self.all_verified)
        self.assertEqual(result.reason, "stale_credit_snapshot")
        snapshot = replace(snapshot, observed_at=self.now, reset_at=self.now)
        result = decide(snapshot, self.request, now=self.now, **self.all_verified)
        self.assertEqual(result.reason, "credit_cycle_unknown")

    def test_denies_non_free_plan_and_missing_provenance(self):
        snapshot = replace(self.snapshot, remaining_credits="400", plan="pro")
        self.assertEqual(decide(snapshot, self.request, now=self.now, **self.all_verified).reason,
                         "not_zero_cash_plan")
        snapshot = replace(snapshot, plan="free", source="")
        self.assertEqual(decide(snapshot, self.request, now=self.now, **self.all_verified).reason,
                         "missing_credit_provenance")

    def test_denies_missing_approval_unsafe_tier_or_public_action(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        for bad, reason in [
            (replace(self.request, manually_approved=False), "owner_approval_missing"),
            (replace(self.request, risk_tier=1), "tier_not_permitted"),
            (replace(self.request, external_actions=True), "unapproved_external_action_or_retry"),
            (replace(self.request, automatic_retry=True), "unapproved_external_action_or_retry"),
        ]:
            with self.subTest(reason=reason):
                self.assertEqual(decide(snapshot, bad, now=self.now, **self.all_verified).reason, reason)

    def test_denies_excess_model_calls_tokens_and_time(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        for bad, reason in [
            (replace(self.request, model_calls=3), "model_call_limit"),
            (replace(self.request, max_input_tokens_per_call=3001), "input_token_limit"),
            (replace(self.request, max_output_tokens_per_call=513), "output_token_limit"),
            (replace(self.request, run_seconds=121), "runtime_limit"),
        ]:
            with self.subTest(reason=reason):
                self.assertEqual(decide(snapshot, bad, now=self.now, **self.all_verified).reason, reason)

    def test_denies_unverified_cost_bound_or_atomic_lease(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        for omission, expected in [
            ("provider_cost_upper_bound_verified", "provider_cost_bound_unverified"),
            ("atomic_lease_verified", "authoritative_atomic_lease_unverified"),
        ]:
            flags = dict(self.all_verified)
            flags[omission] = False
            self.assertEqual(decide(snapshot, self.request, now=self.now, **flags).reason, expected)

    def test_bad_budgets_and_non_finite_values_denied(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        for ceiling in ("NaN", "Infinity", "-2", "0", "6"):
            result = decide(snapshot, replace(self.request, max_total_credits=ceiling),
                            now=self.now, **self.all_verified)
            self.assertFalse(result.permitted, ceiling)

    def test_always_denies_unauthorized_duplicate_mode(self):
        snapshot = replace(self.snapshot, remaining_credits="400")
        request = replace(self.request, task_id=" ", idempotency_key="")
        self.assertEqual(decide(snapshot, request, now=self.now, **self.all_verified).reason,
                         "missing_task_or_idempotency_key")

    def test_deterministic_path_can_skip_model_cost_but_not_scope_controls(self):
        self.assertTrue(deterministic_only(task_id="approved_tier0").permitted)
        self.assertFalse(deterministic_only(task_id="approved_tier0",
                                            external_actions=True).permitted)
        self.assertFalse(deterministic_only(task_id=" ").permitted)


if __name__ == "__main__":
    unittest.main()
