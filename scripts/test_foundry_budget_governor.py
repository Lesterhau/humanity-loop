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

    def test_default_reserve_cannot_be_lowered_to_zero(self):
        snapshot = replace(self.snapshot, remaining_credits="337.528024209")
        config = GovernorConfig(reserve_credits="0")
        result = decide(snapshot, self.request, now=self.now, config=config,
                        **self.all_verified)
        self.assertEqual(result.reason, "unsafe_governor_override")
        self.assertFalse(result.permitted)

    def test_reserve_can_only_be_tightened_not_relaxed(self):
        snapshot = replace(self.snapshot, remaining_credits="401")
        strict = GovernorConfig(reserve_credits="400")
        result = decide(snapshot, self.request, now=self.now, config=strict,
                        **self.all_verified)
        self.assertTrue(result.permitted)
        low = GovernorConfig(reserve_credits="349.999")
        self.assertEqual(decide(snapshot, self.request, now=self.now, config=low,
                                **self.all_verified).reason, "unsafe_governor_override")

    def test_run_credit_ceiling_cannot_be_relaxed(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        for weak in ("5.00001", "500", "Infinity", "-1"):
            with self.subTest(value=weak):
                config = GovernorConfig(max_run_credits=weak)
                self.assertEqual(decide(snapshot, self.request, now=self.now,
                                        config=config, **self.all_verified).reason,
                                 "unsafe_governor_override")

    def test_invalid_governor_policy_objects_fail_closed(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        bad = [
            GovernorConfig(reserve_credits="NaN"),
            GovernorConfig(reserve_credits=200),
            GovernorConfig(max_run_credits=5.0),
            GovernorConfig(max_model_calls=3),
            GovernorConfig(max_input_tokens=3001),
            GovernorConfig(max_output_tokens=513),
            GovernorConfig(max_run_seconds=121),
            GovernorConfig(snapshot_max_age_minutes=61),
            GovernorConfig(snapshot_max_age_minutes=-1),
            GovernorConfig(max_model_calls=True),
            GovernorConfig(max_run_seconds=2.0),
        ]
        for config in bad:
            with self.subTest(config=config):
                decision = decide(snapshot, self.request, now=self.now,
                                  config=config, **self.all_verified)
                self.assertFalse(decision.permitted)
                self.assertEqual(decision.reason, "unsafe_governor_override")

    def test_malformed_structures_do_not_crash(self):
        for snapshot, req, config in [
            (None, self.request, GovernorConfig()),
            (self.snapshot, None, GovernorConfig()),
            (self.snapshot, self.request, None),
            ({}, self.request, GovernorConfig()),
        ]:
            with self.subTest(snapshot=snapshot, request=req, config=config):
                result = decide(snapshot, req, now=self.now, config=config)
                self.assertEqual(result.reason, "invalid_admission_inputs")

    def test_malformed_identity_and_plan_fields_fail_closed(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        for bad_snapshot in [
            replace(snapshot, plan=None),
            replace(snapshot, provider=None),
            replace(snapshot, source=[]),
        ]:
            with self.subTest(bad_snapshot=bad_snapshot):
                self.assertFalse(decide(bad_snapshot, self.request, now=self.now,
                                        **self.all_verified).permitted)
        for bad_request in [
            replace(self.request, task_id=None),
            replace(self.request, idempotency_key=["fake"]),
        ]:
            with self.subTest(bad_request=bad_request):
                self.assertEqual(decide(snapshot, bad_request, now=self.now,
                                        **self.all_verified).reason,
                                 "missing_task_or_idempotency_key")

    def test_truthy_approval_does_not_bypass(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        for approval in (1, "yes", [True]):
            with self.subTest(approval=approval):
                request = replace(self.request, manually_approved=approval)
                decision = decide(snapshot, request, now=self.now,
                                  **self.all_verified)
                self.assertEqual(decision.reason, "owner_approval_missing")

    def test_non_boolean_action_flags_deny(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        for field, value in [
            ("external_actions", 0),
            ("automatic_retry", None),
            ("external_actions", "false"),
        ]:
            with self.subTest(field=field, value=value):
                request = replace(self.request, **{field: value})
                decision = decide(snapshot, request, now=self.now,
                                  **self.all_verified)
                self.assertEqual(decision.reason, "unapproved_external_action_or_retry")

    def test_bool_and_float_integer_fields_denied(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        cases = [
            ("risk_tier", False, "tier_not_permitted"),
            ("model_calls", True, "model_call_limit"),
            ("max_input_tokens_per_call", 1000.0, "input_token_limit"),
            ("max_output_tokens_per_call", True, "output_token_limit"),
            ("run_seconds", 30.0, "runtime_limit"),
        ]
        for field, value, expected in cases:
            with self.subTest(field=field, value=value):
                request = replace(self.request, **{field: value})
                result = decide(snapshot, request, now=self.now,
                                **self.all_verified)
                self.assertEqual(result.reason, expected)

    def test_float_or_boolean_money_is_rejected(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        for bad in (1.0, True, 1):
            with self.subTest(bad=bad):
                request = replace(self.request, max_total_credits=bad)
                self.assertEqual(decide(snapshot, request, now=self.now,
                                        **self.all_verified).reason, "invalid_credit_budget")
                bad_snapshot = replace(snapshot, remaining_credits=bad)
                self.assertEqual(decide(bad_snapshot, self.request, now=self.now,
                                        **self.all_verified).reason, "invalid_credit_budget")

    def test_reset_preceding_balance_observation_denied(self):
        snapshot = replace(self.snapshot, remaining_credits="500",
                           reset_at=self.now - timedelta(minutes=1))
        self.assertEqual(decide(snapshot, self.request, now=self.now,
                                **self.all_verified).reason, "credit_cycle_unknown")

    def test_none_and_malformed_time_denied(self):
        snapshot = replace(self.snapshot, remaining_credits="500")
        for bad in (None, "2026-11-06T18:00:00Z", self.now.replace(tzinfo=None)):
            with self.subTest(bad=bad):
                self.assertEqual(decide(snapshot, self.request, now=bad,
                                        **self.all_verified).reason, "untrusted_timestamp")

    def test_deterministic_only_scope_rejects_nonstrings_or_falsey_lookalikes(self):
        for bad in (None, [], 42, "", " "):
            with self.subTest(bad=bad):
                self.assertFalse(deterministic_only(task_id=bad).permitted)
        self.assertFalse(deterministic_only(task_id="safe", external_actions=0).permitted)

    def test_deterministic_path_can_skip_model_cost_but_not_scope_controls(self):
        self.assertTrue(deterministic_only(task_id="approved_tier0").permitted)
        self.assertFalse(deterministic_only(task_id="approved_tier0",
                                            external_actions=True).permitted)
        self.assertFalse(deterministic_only(task_id=" ").permitted)


if __name__ == "__main__":
    unittest.main()
