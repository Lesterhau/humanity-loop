-- Isolated ephemeral test database fixture matching real production table columns
-- required by the G3 canonical-fence candidate. NEVER run against production.
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE service_role NOLOGIN;
CREATE SCHEMA hl_control;
CREATE TABLE hl_control.agents (
  agent_id text PRIMARY KEY,
  parent_id text,
  status text NOT NULL DEFAULT 'active',
  role text NOT NULL DEFAULT 'coordinator',
  permissions jsonb NOT NULL DEFAULT '[]'::jsonb,
  expires_at timestamptz,
  last_heartbeat timestamptz
);
CREATE TABLE hl_control.tasks (
  task_id text PRIMARY KEY,
  project_id text NOT NULL,
  title text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  risk_tier integer NOT NULL DEFAULT 0,
  status text NOT NULL DEFAULT 'queued',
  priority integer NOT NULL DEFAULT 0,
  current_stage text,
  stages jsonb NOT NULL DEFAULT '[]'::jsonb,
  stage_results jsonb NOT NULL DEFAULT '{}'::jsonb,
  lease_owner text REFERENCES hl_control.agents(agent_id),
  lease_expires_at timestamptz,
  attempts integer NOT NULL DEFAULT 0,
  max_attempts integer NOT NULL DEFAULT 3,
  human_approval_required boolean NOT NULL DEFAULT false,
  human_approval_received boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  updated_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  completed_at timestamptz
);
CREATE TABLE hl_control.events (
  event_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  event_type text NOT NULL,
  task_id text REFERENCES hl_control.tasks(task_id),
  agent_id text REFERENCES hl_control.agents(agent_id),
  project_id text,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
CREATE TABLE hl_control.dead_letters (
  dead_letter_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  task_id text REFERENCES hl_control.tasks(task_id),
  project_id text,
  reason text,
  snapshot jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
INSERT INTO hl_control.agents(agent_id,role,permissions) VALUES
  ('fenced_worker_a','coordinator','["tier0"]'),
  ('fenced_worker_b','coordinator','["tier0"]');

INSERT INTO hl_control.agents(agent_id,role,status,permissions) VALUES
 ('tierone_worker','coordinator','active','["tier1"]'),
 ('inactive_worker','coordinator','retired','["tier0"]'),
 ('fenced_child_a','scout','active','["tier0"]');

UPDATE hl_control.agents SET parent_id='fenced_worker_a' WHERE agent_id='fenced_child_a';

INSERT INTO hl_control.tasks (
 task_id,project_id,title,payload,risk_tier,status,
 stages,current_stage,max_attempts,priority
) VALUES
 ('fenced_case_a','humanity-loop','One fenced Tier-0 public checklist',
  '{"fencing_required":"true","idempotency_key":"case-a-operation-key-2026"}',
  0,'held','["scout","verify","safety","outcome"]','scout',3,10),
 ('fenced_race','humanity-loop','Race fenced claim',
  '{"fencing_required":"true","idempotency_key":"race-operation-key-2026"}',
  0,'held','["scout","outcome"]','scout',3,5),
 ('fenced_expiry','humanity-loop','Expiry non-retry',
  '{"fencing_required":"true","idempotency_key":"expiry-operation-key-2026"}',
  0,'held','["scout","outcome"]','scout',3,5),
 ('fenced_restart','humanity-loop','Owner restart fencing',
  '{"fencing_required":"true","idempotency_key":"restart-operation-key-2026"}',
  0,'held','["scout","outcome"]','scout',3,5),
 ('fenced_unsafe','humanity-loop','Not safe Tier-1',
  '{"fencing_required":"true","idempotency_key":"unsafe-operation-key-2026"}',
  1,'held','["scout","outcome"]','scout',3,5),
 ('fenced_needs_approval','humanity-loop','Needs human approval',
  '{"fencing_required":"true","idempotency_key":"approval-operation-key-2026"}',
  0,'held','["scout","outcome"]','scout',3,5),
 ('legacy_queue','humanity-loop','Legacy unfenced candidate',
  '{}',0,'queued','["scout","outcome"]','scout',3,1);
UPDATE hl_control.tasks SET human_approval_required=true,human_approval_received=false
WHERE task_id='fenced_needs_approval';
CREATE OR REPLACE FUNCTION public.assert_true(ok boolean,msg text)
RETURNS void LANGUAGE plpgsql AS $a$
BEGIN
  IF ok IS DISTINCT FROM true THEN RAISE EXCEPTION 'ASSERTION_FAILED: %',msg; END IF;
END $a$;

CREATE OR REPLACE FUNCTION public.assert_rejected(statement text,expected text)
RETURNS void LANGUAGE plpgsql AS $a$
DECLARE message text;
BEGIN
  BEGIN
    EXECUTE statement;
  EXCEPTION WHEN OTHERS THEN
    GET STACKED DIAGNOSTICS message=MESSAGE_TEXT;
    IF position(expected in message)>0 THEN RETURN; END IF;
    RAISE EXCEPTION 'WRONG_REJECTION: expected %, got %',expected,message;
  END;
  RAISE EXCEPTION 'UNEXPECTED_SUCCESS: %',left(statement,160);
END $a$;
