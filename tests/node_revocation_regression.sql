-- Humanity Loop Stage-0 contributor safety regression, 2026-11-08.
-- RUN ONLY by an authorized privileged tester in an approved maintenance window.
-- It uses synthetic identities, a synthetic-only capability, no email, no external API.
-- The FINAL RAISE EXCEPTION is intentional. The exact marker
-- "STAGE0_EXPECTED_PASS_AND_ROLLBACK" means ALL assertions passed and the
-- entire statement, including registrations, tasks, events and submissions,
-- was rolled back. Any other error means FAIL and should be investigated.
-- No production contributor or external service should be used in this test.
DO $stage0$
DECLARE
  hash_a text := md5(random()::text || clock_timestamp()::text) || md5(random()::text || clock_timestamp()::text);
  hash_b text := md5(random()::text || clock_timestamp()::text) || md5(random()::text || clock_timestamp()::text);
  a jsonb;
  b jsonb;
  claim_a jsonb;
  claim_b jsonb;
  result_a jsonb;
  node_a uuid;
  work_a uuid;
  work_b uuid;
  submission_a uuid;
  wrong_owner_denied boolean := false;
  expired_lease_denied boolean := false;
  paused_checkin_denied boolean := false;
  revoked_checkin_denied boolean := false;
  revoked_resume_denied boolean := false;
  revoked_pause_denied boolean := false;
  invalid_token_denied boolean := false;
BEGIN
  a := public.hl_node_register(hash_a,'["stage0-test-only"]'::jsonb,'["en"]'::jsonb,
    'synthetic-transaction-only',null,null,false,'["tier0"]'::jsonb);
  b := public.hl_node_register(hash_b,'[]'::jsonb,'["en"]'::jsonb,
    'synthetic-transaction-only',null,null,false,'["tier0"]'::jsonb);
  node_a := (a->>'node_id')::uuid;
  IF node_a IS NULL OR (a->'risk_permissions') IS DISTINCT FROM '["tier0"]'::jsonb THEN
    RAISE EXCEPTION 'FAIL register/permission scope';
  END IF;
  IF (b->>'node_id')::uuid IS NULL THEN RAISE EXCEPTION 'FAIL second synthetic registration'; END IF;

  INSERT INTO hl_control.node_work_items(title,instructions,required_capabilities,status,priority,risk_tier,expires_at)
  VALUES ('SYNTHETIC STAGE0 A','TEST ONLY - do not execute externally',
    '["stage0-test-only"]'::jsonb,'open',9999,0,now()+interval '1 day')
  RETURNING work_id INTO work_a;

  claim_a := public.hl_node_checkin(hash_a,'["stage0-test-only"]'::jsonb,'["en"]'::jsonb,null,null);
  IF (claim_a->'assignment'->>'work_id')::uuid IS DISTINCT FROM work_a THEN
    RAISE EXCEPTION 'FAIL claim/lease';
  END IF;

  claim_b := public.hl_node_checkin(hash_b,'[]'::jsonb,'["en"]'::jsonb,null,null);
  IF claim_b->'assignment' IS DISTINCT FROM 'null'::jsonb THEN
    RAISE EXCEPTION 'FAIL unauthorized task claim';
  END IF;

  BEGIN
    PERFORM public.hl_node_submit(hash_b,work_a,'{"test":"wrong owner"}'::jsonb);
  EXCEPTION WHEN others THEN
    wrong_owner_denied := SQLERRM LIKE '%not claimed by this node%';
  END;
  IF NOT wrong_owner_denied THEN RAISE EXCEPTION 'FAIL ownership denial'; END IF;

  result_a := public.hl_node_submit(hash_a,work_a,'{"test":"synthetic"}'::jsonb,
    '[]'::jsonb,'synthetic transaction only','[]'::jsonb);
  submission_a := (result_a->>'submission_id')::uuid;
  IF result_a->>'status'<>'quarantined'
    OR (SELECT status FROM hl_control.node_work_items WHERE work_id=work_a)<>'submitted' THEN
    RAISE EXCEPTION 'FAIL quarantine/submit state';
  END IF;

  -- This verifies a private reviewer state transition, not an actual verified
  -- external impact, and not the entire production review interface.
  UPDATE hl_control.node_submissions
    SET status='accepted', reviewed_at=now(), review_note='synthetic rollback'
    WHERE submission_id=submission_a;
  IF (SELECT status FROM hl_control.node_submissions WHERE submission_id=submission_a)<>'accepted'
    THEN RAISE EXCEPTION 'FAIL reviewer-state transition'; END IF;

  INSERT INTO hl_control.node_work_items(title,instructions,required_capabilities,status,priority,risk_tier,expires_at)
  VALUES ('SYNTHETIC STAGE0 B','TEST ONLY - do not execute externally',
    '["stage0-test-only"]'::jsonb,'open',9999,0,now()+interval '1 day')
  RETURNING work_id INTO work_b;
  claim_a := public.hl_node_checkin(hash_a,'["stage0-test-only"]'::jsonb,'["en"]'::jsonb,null,null);
  IF (claim_a->'assignment'->>'work_id')::uuid IS DISTINCT FROM work_b
    THEN RAISE EXCEPTION 'FAIL second claim'; END IF;

  UPDATE hl_control.node_work_items SET lease_expires_at=now()-interval '1 minute'
    WHERE work_id=work_b;
  BEGIN
    PERFORM public.hl_node_submit(hash_a,work_b,'{"test":"expired"}'::jsonb);
  EXCEPTION WHEN others THEN
    expired_lease_denied := SQLERRM LIKE '%lease expired%';
  END;
  IF NOT expired_lease_denied THEN RAISE EXCEPTION 'FAIL expired lease enforcement'; END IF;
  claim_a := public.hl_node_checkin(hash_a,'["stage0-test-only"]'::jsonb,'["en"]'::jsonb,null,null);
  IF (claim_a->'assignment'->>'work_id')::uuid IS DISTINCT FROM work_b
    THEN RAISE EXCEPTION 'FAIL lease requeue'; END IF;

  PERFORM public.hl_node_set_status(hash_a,'paused');
  BEGIN
    PERFORM public.hl_node_checkin(hash_a,'["stage0-test-only"]'::jsonb,'["en"]'::jsonb,null,null);
  EXCEPTION WHEN others THEN
    paused_checkin_denied := SQLERRM LIKE '%inactive node token%';
  END;
  IF NOT paused_checkin_denied THEN RAISE EXCEPTION 'FAIL paused checkin'; END IF;
  IF (public.hl_node_set_status(hash_a,'active')->>'status')<>'active'
    THEN RAISE EXCEPTION 'FAIL normal resume'; END IF;

  PERFORM public.hl_node_set_status(hash_a,'revoked');
  IF (public.hl_node_set_status(hash_a,'revoked')->>'status')<>'revoked'
    THEN RAISE EXCEPTION 'FAIL idempotent revoke'; END IF;
  BEGIN
    PERFORM public.hl_node_set_status(hash_a,'active');
  EXCEPTION WHEN others THEN
    revoked_resume_denied := SQLERRM LIKE '%cannot be reactivated%';
  END;
  BEGIN
    PERFORM public.hl_node_set_status(hash_a,'paused');
  EXCEPTION WHEN others THEN
    revoked_pause_denied := SQLERRM LIKE '%cannot be reactivated%';
  END;
  BEGIN
    PERFORM public.hl_node_checkin(hash_a,'["stage0-test-only"]'::jsonb,'["en"]'::jsonb,null,null);
  EXCEPTION WHEN others THEN
    revoked_checkin_denied := SQLERRM LIKE '%inactive node token%';
  END;
  IF NOT (revoked_resume_denied AND revoked_pause_denied AND revoked_checkin_denied)
    OR (SELECT status FROM hl_control.contributor_nodes WHERE node_id=node_a)<>'revoked' THEN
    RAISE EXCEPTION 'FAIL permanent revocation';
  END IF;

  BEGIN
    PERFORM public.hl_node_set_status(repeat('0',64),'active');
  EXCEPTION WHEN others THEN
    invalid_token_denied := SQLERRM LIKE '%invalid node token%';
  END;
  IF NOT invalid_token_denied THEN RAISE EXCEPTION 'FAIL invalid-token denial'; END IF;

  -- INTENTIONALLY abort this statement to guarantee no synthetic residue.
  RAISE EXCEPTION 'STAGE0_EXPECTED_PASS_AND_ROLLBACK: registration; exclusive claim; forbidden cross-node submit; quarantine; reviewer transition; expired lease deny/requeue; pause/resume; irreversible revoke; unknown-token deny';
END;
$stage0$;
