# Humanity Loop Transactional Control Plane

**Backend:** Supabase/Postgres  
**Project:** Humanity Loop Control Plane  
**Project ref:** `jxtcccrlnhkcjfnwlfea`  
**Region:** `us-east-1`  
**Cost at creation:** $0/month  
**Schema:** `hl_control`

This database is the transactional runtime-state layer. GitHub remains the public institutional record.

## Security posture

The control-plane tables live in a private, non-public schema.

At initialization:
- `public`, `anon`, and `authenticated` have no schema/table/function privileges on `hl_control`;
- no browser-facing policies or public Data API access are required;
- service credentials must never be committed to GitHub or exposed to browser clients;
- workers should receive only the minimum capability needed to claim/heartbeat/complete their own work;
- Supabase Security Advisor returned zero findings after initialization.

## Core tables

### agents
Persistent worker identity and lineage:
- agent ID / parent ID;
- role;
- provider/model;
- status;
- depth and recursion limits;
- child-count limits;
- compute budget;
- tool and permission ceilings;
- heartbeat/expiry state.

### tasks
Transactional work queue:
- project/task IDs;
- payload;
- risk tier;
- priority;
- staged workflow state;
- lease owner/expiry;
- attempts/max attempts;
- human-approval requirements;
- completion state.

### approvals
Explicit approval records for tasks requiring human or accountable review.

### events
Append-oriented operational events for claims, heartbeats, state transitions, and future control-plane observability.

### dead_letters
Tasks that exceed retry/attempt limits or otherwise require intervention.

### usage
Per-task/agent/provider/model resource records:
- tokens;
- compute units;
- cost;
- energy;
- water;
- carbon;
- metadata.

## Transactional primitives

### claim_next_task(agent_id, lease_seconds)
Claims the highest-priority eligible queued task using:

`FOR UPDATE SKIP LOCKED`

This prevents two workers from claiming the same task concurrently.

Tasks requiring human approval are not claimable until approval is recorded.

### register_or_heartbeat_agent(...)
Creates or refreshes a stable worker identity and emits a heartbeat event.

### heartbeat_agent(agent_id)
Refreshes an active worker heartbeat and writes an event.

### renew_task_lease(task_id, agent_id, lease_seconds)
Extends only the currently owning worker's valid lease.

### advance_task_stage(...)
Persists the current role result, verifies lease ownership/stage identity, and moves the task to the next stage or completed state.

### fail_task(...)
Requeues recoverable failures and moves exhausted tasks into the dead-letter table.

### release_expired_leases()
Recovers abandoned leased work. Expired tasks are requeued until max attempts are reached, then dead-lettered with a failure snapshot.

## Verified self-test

A rollback-wrapped test:
1. created a temporary agent;
2. created a queued task;
3. claimed the task;
4. established a lease;
5. heartbeated the worker;
6. verified the task showed `status=leased` and the expected owner;
7. rolled the test data back.

## Advisor status

After schema initialization and missing-FK-index repair:
- **Security Advisor:** zero findings.
- **Performance Advisor:** only new-database `unused_index` informational notices remain. These should not be interpreted as reasons to remove indexes before production query patterns exist.

## Runtime ownership

GitHub:
- protocol;
- governance;
- source;
- issues;
- durable receipts;
- public action/win/dead-end ledgers.

Supabase/Postgres:
- live queue;
- leases;
- heartbeats;
- attempts;
- approvals;
- transient execution state;
- provider/agent usage;
- operational event stream.

The database must not become the sole copy of verified outcomes. Completed meaningful work is reconciled back to GitHub.

## Live integration status

The dedicated ChatGPT Foundry worker identity is `foundry_chatgpt_hourly`.

The first live integration task, `foundry-bootstrap-2026-10-02`, was claimed transactionally and is being executed through the role-stage persistence functions.

A rollback-wrapped recovery test has also verified:
- stage advancement;
- forced failure → requeue;
- reclaim;
- expired lease detection;
- max-attempt dead-letter handling.

Remaining acceptance work for issue #3:
1. complete one full real Foundry cycle through every role stage;
2. write and read-back verify its GitHub receipt;
3. confirm the scheduled dedicated worker remains enabled and uses the same lifecycle on its next normal run;
4. record resource usage from live cycles as telemetry becomes available.
