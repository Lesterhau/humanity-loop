"""Bounded, provider-neutral control-plane primitives for Humanity Loop Foundry Alpha."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set
import uuid


STAGES = [
    "scout",
    "verify",
    "assign",
    "build_act",
    "dissent",
    "safety",
    "revision",
    "outcome",
]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class AgentRecord:
    agent_id: str
    parent_id: Optional[str]
    role: str
    mission: str
    tools: Set[str]
    permissions: Set[str]
    depth: int
    max_depth: int
    max_children: int
    compute_budget: float
    expires_at: Optional[datetime] = None
    status: str = "active"
    child_count: int = 0
    last_heartbeat: Optional[datetime] = None


@dataclass
class TaskRecord:
    task_id: str
    project_id: str
    stages: List[str] = field(default_factory=lambda: list(STAGES))
    stage_index: int = 0
    status: str = "queued"
    lease_owner: Optional[str] = None
    lease_expires_at: Optional[datetime] = None
    attempts: int = 0
    max_attempts: int = 3
    stage_results: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utcnow)
    completed_at: Optional[datetime] = None

    @property
    def current_stage(self) -> Optional[str]:
        if self.stage_index >= len(self.stages):
            return None
        return self.stages[self.stage_index]


class FoundryControlPlane:
    def __init__(self) -> None:
        self.agents: Dict[str, AgentRecord] = {}
        self.tasks: Dict[str, TaskRecord] = {}
        self.events: List[Dict[str, Any]] = []
        self.dead_letter: List[Dict[str, Any]] = []
        self.usage: List[Dict[str, Any]] = []

    def _event(self, event_type: str, **payload: Any) -> None:
        self.events.append({
            "timestamp": utcnow().isoformat(),
            "event_type": event_type,
            **payload,
        })

    def register_root(
        self,
        *,
        role: str,
        mission: str,
        tools: Set[str],
        permissions: Set[str],
        max_depth: int,
        max_children: int,
        compute_budget: float,
        agent_id: Optional[str] = None,
    ) -> AgentRecord:
        agent = AgentRecord(
            agent_id=agent_id or f"agt_{uuid.uuid4().hex[:16]}",
            parent_id=None,
            role=role,
            mission=mission,
            tools=set(tools),
            permissions=set(permissions),
            depth=0,
            max_depth=max_depth,
            max_children=max_children,
            compute_budget=compute_budget,
        )
        self.agents[agent.agent_id] = agent
        self._event("agent_created", agent_id=agent.agent_id, parent_id=None, role=role)
        return agent

    def spawn_child(
        self,
        parent_id: str,
        *,
        role: str,
        mission: str,
        tools: Set[str],
        permissions: Set[str],
        max_depth: Optional[int] = None,
        max_children: int = 0,
        compute_budget: float = 0.0,
        expires_at: Optional[datetime] = None,
        agent_id: Optional[str] = None,
    ) -> AgentRecord:
        parent = self.agents[parent_id]
        if parent.status != "active":
            raise ValueError("parent is not active")
        if parent.child_count >= parent.max_children:
            raise ValueError("parent child-count limit reached")
        child_depth = parent.depth + 1
        if child_depth > parent.max_depth:
            raise ValueError("parent recursion-depth limit reached")
        if not set(tools).issubset(parent.tools):
            raise ValueError("child tools exceed parent tools")
        if not set(permissions).issubset(parent.permissions):
            raise ValueError("child permissions exceed parent permissions")
        if compute_budget > parent.compute_budget:
            raise ValueError("child compute budget exceeds parent budget")
        child_max_depth = parent.max_depth if max_depth is None else max_depth
        if child_max_depth > parent.max_depth:
            raise ValueError("child max_depth exceeds parent max_depth")

        child = AgentRecord(
            agent_id=agent_id or f"agt_{uuid.uuid4().hex[:16]}",
            parent_id=parent.agent_id,
            role=role,
            mission=mission,
            tools=set(tools),
            permissions=set(permissions),
            depth=child_depth,
            max_depth=child_max_depth,
            max_children=max_children,
            compute_budget=compute_budget,
            expires_at=expires_at,
        )
        self.agents[child.agent_id] = child
        parent.child_count += 1
        self._event("agent_created", agent_id=child.agent_id, parent_id=parent.agent_id, role=role)
        return child

    def heartbeat(self, agent_id: str, now: Optional[datetime] = None) -> None:
        agent = self.agents[agent_id]
        if agent.status != "active":
            raise ValueError("inactive agent cannot heartbeat")
        agent.last_heartbeat = now or utcnow()
        self._event("heartbeat", agent_id=agent_id)

    def set_agent_status(self, agent_id: str, status: str) -> None:
        if status not in {"active", "reserve", "quarantined", "retired"}:
            raise ValueError("invalid agent status")
        self.agents[agent_id].status = status
        self._event("agent_status", agent_id=agent_id, status=status)

    def submit_task(
        self,
        *,
        project_id: str,
        stages: Optional[List[str]] = None,
        max_attempts: int = 3,
        task_id: Optional[str] = None,
    ) -> TaskRecord:
        task = TaskRecord(
            task_id=task_id or f"tsk_{uuid.uuid4().hex[:16]}",
            project_id=project_id,
            stages=list(stages or STAGES),
            max_attempts=max_attempts,
        )
        self.tasks[task.task_id] = task
        self._event("task_submitted", task_id=task.task_id, project_id=project_id)
        return task

    def claim_task(
        self,
        task_id: str,
        agent_id: str,
        *,
        lease_seconds: int = 300,
        now: Optional[datetime] = None,
    ) -> TaskRecord:
        now = now or utcnow()
        task = self.tasks[task_id]
        agent = self.agents[agent_id]
        if agent.status != "active":
            raise ValueError("inactive agent cannot claim tasks")
        if task.status in {"completed", "dead_letter"}:
            raise ValueError("task is not claimable")
        if task.lease_owner and task.lease_expires_at and task.lease_expires_at > now:
            raise ValueError("task already has an active lease")
        task.status = "leased"
        task.lease_owner = agent_id
        task.lease_expires_at = now + timedelta(seconds=lease_seconds)
        self._event("task_claimed", task_id=task_id, agent_id=agent_id, stage=task.current_stage)
        return task

    def advance_task(
        self,
        task_id: str,
        agent_id: str,
        result: Any,
        *,
        now: Optional[datetime] = None,
    ) -> TaskRecord:
        now = now or utcnow()
        task = self.tasks[task_id]
        if task.lease_owner != agent_id:
            raise ValueError("agent does not own task lease")
        if task.lease_expires_at and task.lease_expires_at < now:
            raise ValueError("task lease expired")
        stage = task.current_stage
        if stage is None:
            raise ValueError("task has no remaining stage")
        task.stage_results[stage] = result
        task.stage_index += 1
        task.lease_owner = None
        task.lease_expires_at = None
        if task.current_stage is None:
            task.status = "completed"
            task.completed_at = now
            self._event("task_completed", task_id=task_id, project_id=task.project_id)
        else:
            task.status = "queued"
            self._event("task_advanced", task_id=task_id, next_stage=task.current_stage)
        return task

    def fail_task(self, task_id: str, agent_id: str, reason: str) -> TaskRecord:
        task = self.tasks[task_id]
        if task.lease_owner != agent_id:
            raise ValueError("agent does not own task lease")
        task.attempts += 1
        task.lease_owner = None
        task.lease_expires_at = None
        if task.attempts >= task.max_attempts:
            task.status = "dead_letter"
            record = {"task_id": task_id, "project_id": task.project_id, "reason": reason}
            self.dead_letter.append(record)
            self._event("task_dead_letter", **record)
        else:
            task.status = "queued"
            self._event("task_retry", task_id=task_id, reason=reason, attempts=task.attempts)
        return task

    def record_usage(
        self,
        *,
        agent_id: str,
        project_id: str,
        compute_units: float,
        cost_usd: float,
        energy_kwh: float = 0.0,
        water_liters: float = 0.0,
        carbon_kg_co2e: float = 0.0,
    ) -> None:
        self.usage.append({
            "timestamp": utcnow().isoformat(),
            "agent_id": agent_id,
            "project_id": project_id,
            "compute_units": float(compute_units),
            "cost_usd": float(cost_usd),
            "energy_kwh": float(energy_kwh),
            "water_liters": float(water_liters),
            "carbon_kg_co2e": float(carbon_kg_co2e),
        })
        self._event("usage_recorded", agent_id=agent_id, project_id=project_id)

    def snapshot(self) -> Dict[str, Any]:
        active_agents = [asdict(a) for a in self.agents.values() if a.status == "active"]
        current_tasks = [asdict(t) for t in self.tasks.values() if t.status not in {"completed", "dead_letter"}]
        recent_outcomes = [asdict(t) for t in self.tasks.values() if t.status == "completed"]
        failures = list(self.dead_letter)
        return {
            "active_agents": active_agents,
            "current_tasks": current_tasks,
            "recent_outcomes": recent_outcomes,
            "failures": failures,
            "usage": list(self.usage),
            "events": list(self.events),
        }
