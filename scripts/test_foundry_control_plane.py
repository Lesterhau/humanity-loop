import unittest
from datetime import datetime, timedelta, timezone

from foundry_control_plane import FoundryControlPlane, STAGES


class FoundryControlPlaneTests(unittest.TestCase):
    def setUp(self):
        self.cp = FoundryControlPlane()
        self.root = self.cp.register_root(
            role="project-manager",
            mission="Coordinate bounded work",
            tools={"repo-read", "repo-write", "web-read"},
            permissions={"tier0", "tier1"},
            max_depth=2,
            max_children=8,
            compute_budget=100.0,
            agent_id="agt_root",
        )

    def test_child_cannot_escalate_permissions_or_tools(self):
        with self.assertRaises(ValueError):
            self.cp.spawn_child(
                "agt_root",
                role="builder",
                mission="Build",
                tools={"repo-read", "shell-root"},
                permissions={"tier0", "tier2"},
                compute_budget=10,
            )

    def test_child_count_and_depth_are_bounded(self):
        parent = self.cp.spawn_child(
            "agt_root",
            role="builder",
            mission="Build",
            tools={"repo-read"},
            permissions={"tier0"},
            max_children=1,
            compute_budget=20,
            agent_id="agt_parent",
        )
        child = self.cp.spawn_child(
            parent.agent_id,
            role="specialist",
            mission="Narrow task",
            tools={"repo-read"},
            permissions={"tier0"},
            max_children=0,
            compute_budget=5,
            agent_id="agt_child",
        )
        self.assertEqual(child.depth, 2)
        with self.assertRaises(ValueError):
            self.cp.spawn_child(
                child.agent_id,
                role="too-deep",
                mission="Should fail",
                tools={"repo-read"},
                permissions={"tier0"},
                compute_budget=1,
            )

    def test_lease_prevents_duplicate_claim_and_expired_lease_can_recover(self):
        a2 = self.cp.spawn_child(
            "agt_root",
            role="verifier",
            mission="Verify",
            tools={"repo-read"},
            permissions={"tier0"},
            compute_budget=10,
            agent_id="agt_verify",
        )
        task = self.cp.submit_task(project_id="p1", stages=["verify"], task_id="tsk_1")
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.cp.claim_task(task.task_id, self.root.agent_id, lease_seconds=10, now=now)
        with self.assertRaises(ValueError):
            self.cp.claim_task(task.task_id, a2.agent_id, lease_seconds=10, now=now + timedelta(seconds=5))
        self.cp.claim_task(task.task_id, a2.agent_id, lease_seconds=10, now=now + timedelta(seconds=11))
        self.assertEqual(task.lease_owner, a2.agent_id)

    def test_failures_go_to_dead_letter_after_retry_limit(self):
        task = self.cp.submit_task(project_id="p2", stages=["build"], max_attempts=2, task_id="tsk_fail")
        self.cp.claim_task(task.task_id, self.root.agent_id)
        self.cp.fail_task(task.task_id, self.root.agent_id, "boom-1")
        self.cp.claim_task(task.task_id, self.root.agent_id)
        self.cp.fail_task(task.task_id, self.root.agent_id, "boom-2")
        self.assertEqual(task.status, "dead_letter")
        self.assertEqual(self.cp.snapshot()["failures"][0]["task_id"], task.task_id)

    def test_heartbeat_and_usage_are_visible(self):
        self.cp.heartbeat(self.root.agent_id)
        self.cp.record_usage(
            agent_id=self.root.agent_id,
            project_id="p3",
            compute_units=2.5,
            cost_usd=0.02,
            energy_kwh=0.01,
            water_liters=0.02,
            carbon_kg_co2e=0.004,
        )
        snap = self.cp.snapshot()
        self.assertIsNotNone(self.root.last_heartbeat)
        self.assertEqual(snap["usage"][0]["project_id"], "p3")

    def test_complete_bounded_pipeline(self):
        agents = {}
        for stage in STAGES:
            agents[stage] = self.cp.spawn_child(
                "agt_root",
                role=stage,
                mission=f"Perform {stage}",
                tools={"repo-read"},
                permissions={"tier0"},
                compute_budget=5,
                agent_id=f"agt_{stage}",
            )

        task = self.cp.submit_task(project_id="integration", task_id="tsk_pipeline")
        for stage in STAGES:
            self.assertEqual(task.current_stage, stage)
            agent = agents[stage]
            self.cp.claim_task(task.task_id, agent.agent_id)
            self.cp.advance_task(task.task_id, agent.agent_id, {"stage": stage, "ok": True})

        self.assertEqual(task.status, "completed")
        self.assertEqual(list(task.stage_results), STAGES)
        self.assertEqual(len(self.cp.snapshot()["recent_outcomes"]), 1)


if __name__ == "__main__":
    unittest.main()
