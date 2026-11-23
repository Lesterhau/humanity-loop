-- Run ONLY after synthetic fixture and migration candidate in ephemeral PostgreSQL.
\set ON_ERROR_STOP on

-- Public roles receive no execute on new fencing entry points.
SELECT public.assert_true(
  NOT has_function_privilege('anon','hl_control.claim_fenced_task_v1(text,text,text,integer)','EXECUTE')
  AND NOT has_function_privilege('authenticated','hl_control.claim_fenced_task_v1(text,text,text,integer)','EXECUTE')
  AND NOT has_function_privilege('service_role','hl_control.claim_fenced_task_v1(text,text,text,integer)','EXECUTE'),
  'fenced_claim_must_not_be_public_rpc'
);

-- Legacy claim path may ONLY take the old unfenced queue.
SELECT public.assert_true(
 (hl_control.claim_next_task('fenced_worker_b',60)).task_id='legacy_queue',
 'legacy_claim_must_ignore_opt_in_fenced_tasks'
);
SELECT public.assert_true(
 (SELECT count(*) FROM hl_control.tasks
  WHERE payload->>'fencing_required'='true' AND lease_owner IS NOT NULL)=0,
 'fenced_tasks_must_not_be_legacy_claimed'
);

-- Tier, manual approval, agent permissions, strict idempotency and TTL.
SELECT public.assert_rejected(
 $SELECT hl_control.claim_fenced_task_v1('fenced_unsafe','fenced_worker_a','unsafe-operation-key-2026',60)$,
 'fenced_task_unavailable'
);
-- A valid task lease never grants access to paid models or external actions.
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_paid','fenced_worker_a','paid-operation-key-2026',60)$$,
 'fenced_task_unavailable'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_outreach','fenced_worker_a','outreach-operation-key-2026',60)$$,
 'fenced_task_unavailable'
);
SELECT public.assert_true(
  (SELECT COUNT(*)=0 FROM hl_control.events
   WHERE event_type='fenced_task_claimed' AND task_id IN ('fenced_paid','fenced_outreach')),
  'no_paid_or_outside_claim_event_may_be_recorded'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_needs_approval','fenced_worker_a','approval-operation-key-2026',60)$$,
 'fenced_task_unavailable'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_case_a','tierone_worker','case-a-operation-key-2026',60)$$,
 'fenced_claim_unapproved_agent'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_case_a','inactive_worker','case-a-operation-key-2026',60)$$,
 'fenced_claim_unapproved_agent'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_case_a','fenced_worker_a','wrong-operation-key',60)$$,
 'fenced_task_unavailable'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_case_a','fenced_worker_a','case-a-operation-key-2026',999999)$$,
 'fenced_claim_invalid_arguments'
);

CREATE TEMP TABLE lease_a AS
  SELECT * FROM hl_control.claim_fenced_task_v1(
    'fenced_case_a','fenced_worker_a','case-a-operation-key-2026',60
  );
SELECT public.assert_true(
  (SELECT fenced_token IS NOT NULL AND fenced_epoch=1 AND status='leased'
   FROM lease_a),
  'first_fenced_claim_must_have_fresh_token_and_epoch'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.claim_fenced_task_v1('fenced_case_a','fenced_worker_b','case-a-operation-key-2026',60)$$,
 'fenced_task_unavailable_or_already_leased'
);

DO $t$
DECLARE t hl_control.tasks; after_task hl_control.tasks; bad_token uuid:=gen_random_uuid();
BEGIN
  SELECT * INTO t FROM lease_a;
  -- Same stable identity is insufficient: a valid unique token and epoch are required.
  BEGIN
    PERFORM hl_control.advance_fenced_stage_v1(
      t.task_id,'fenced_worker_a',t.fenced_epoch,bad_token,
      'scout','{"draft":true}'::jsonb,'verify',false);
    RAISE EXCEPTION 'ASSERTION_FAILED: wrong_token_accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
  END;
  BEGIN
    PERFORM hl_control.advance_fenced_stage_v1(
      t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,
      'scout','{"draft":true}'::jsonb,'outcome',false);
    RAISE EXCEPTION 'ASSERTION_FAILED: stage_skipping_accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_stage_invalid_transition%' THEN RAISE; END IF;
  END;

  SELECT * INTO after_task FROM hl_control.advance_fenced_stage_v1(
    t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,
    'scout','{"draft":"one bounded checklist only"}'::jsonb,'verify',false);
  PERFORM public.assert_true(
    after_task.status='leased' AND after_task.current_stage='verify'
    AND after_task.stage_results ? 'scout',
    'valid_stage_must_move_in_sequence_only'
  );
  BEGIN
    PERFORM hl_control.advance_fenced_stage_v1(
      t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,
      'scout','{"duplicate":true}'::jsonb,'verify',false);
    RAISE EXCEPTION 'ASSERTION_FAILED: duplicate_stage_accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
  END;
  SELECT * INTO after_task FROM hl_control.renew_fenced_lease_v1(
    t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,60);
  PERFORM public.assert_true(after_task.fenced_epoch=t.fenced_epoch
     AND after_task.fenced_token=t.fenced_token,
     'renew_must_preserve_fence_identity');
  PERFORM hl_control.advance_fenced_stage_v1(
    t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,
    'verify','{"verdict":"draft_only"}'::jsonb,'safety',false);
  PERFORM hl_control.advance_fenced_stage_v1(
    t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,
    'safety','{"go":true,"independently_verified":false}'::jsonb,'outcome',false);
  SELECT * INTO after_task FROM hl_control.advance_fenced_stage_v1(
    t.task_id,'fenced_worker_a',t.fenced_epoch,t.fenced_token,
    'outcome','{"human_review_required":true}'::jsonb,NULL,true);
  PERFORM public.assert_true(
     after_task.status='completed' AND after_task.fenced_token IS NULL
     AND after_task.lease_owner IS NULL AND after_task.current_stage IS NULL,
     'completed_fenced_task_must_revoke_live_token');
END $t$;

-- Test that ALL legacy operations refuse an actively fenced task.
CREATE TEMP TABLE lease_restart_old AS
  SELECT * FROM hl_control.claim_fenced_task_v1(
    'fenced_restart','fenced_worker_a','restart-operation-key-2026',60);
SELECT public.assert_rejected(
 $$SELECT hl_control.advance_task_stage('fenced_restart','fenced_worker_a','scout','{}'::jsonb,'outcome',false)$$,
 'fenced_task_requires_token'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.advance_task_stage_v2('fenced_restart','fenced_worker_a','fenced_child_a','scout','{}'::jsonb,'outcome',false)$$,
 'fenced_task_requires_token'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.renew_task_lease('fenced_restart','fenced_worker_a',60)$$,
 'legacy_renew_denied'
);
SELECT public.assert_rejected(
 $$SELECT hl_control.fail_task('fenced_restart','fenced_worker_a','bad')$$,
 'fenced_task_requires_token'
);

-- Expired fenced tasks never automatically requeue and stale workers cannot
-- renew, complete, or declare failure. Manual admin moves them to dead letter.
UPDATE hl_control.tasks SET lease_expires_at=clock_timestamp()-interval '2 second'
WHERE task_id='fenced_restart';
SELECT public.assert_true(hl_control.release_expired_leases()=0,
                          'legacy_expiry_cannot_requeue_fenced_work');
DO $t$
DECLARE old hl_control.tasks; expired hl_control.tasks;
BEGIN
  SELECT * INTO old FROM lease_restart_old;
  BEGIN
    PERFORM hl_control.renew_fenced_lease_v1(
      old.task_id,'fenced_worker_a',old.fenced_epoch,old.fenced_token,60);
    RAISE EXCEPTION 'ASSERTION_FAILED: expired_renewal_accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_renew_stale_or_unauthorized%' THEN RAISE; END IF;
  END;
  BEGIN
    PERFORM hl_control.advance_fenced_stage_v1(
      old.task_id,'fenced_worker_a',old.fenced_epoch,old.fenced_token,
      'scout','{}'::jsonb,'outcome',false);
    RAISE EXCEPTION 'ASSERTION_FAILED: expired_commit_accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
  END;
  SELECT * INTO expired FROM hl_control.expire_fenced_task_v1(old.task_id);
  PERFORM public.assert_true(
    expired.status='dead_letter' AND expired.fenced_token IS NULL
    AND expired.attempts=1,
    'expired_fenced_task_must_dead_letter_without_replay'
  );
END $t$;

-- Explicit admin review/rearm only in this SYNTHETIC test: same owner identity
-- receives a distinct epoch and token; stale old invocation is impossible.
UPDATE hl_control.tasks
SET status='held',payload=jsonb_set(payload,'{idempotency_key}',
    '"restart-second-operation-2026"'),
    lease_owner=NULL,lease_expires_at=NULL,fenced_token=NULL
WHERE task_id='fenced_restart' AND status='dead_letter';
CREATE TEMP TABLE lease_restart_new AS
  SELECT * FROM hl_control.claim_fenced_task_v1(
    'fenced_restart','fenced_worker_a','restart-second-operation-2026',60);
DO $t$
DECLARE old hl_control.tasks; current_lease hl_control.tasks;
BEGIN
  SELECT * INTO old FROM lease_restart_old;
  SELECT * INTO current_lease FROM lease_restart_new;
  PERFORM public.assert_true(
     current_lease.fenced_epoch=old.fenced_epoch+1
     AND current_lease.fenced_token<>old.fenced_token
     AND current_lease.lease_owner=old.lease_owner,
     'same_owner_new_lease_must_have_new_token_and_generation'
  );
  BEGIN
    PERFORM hl_control.advance_fenced_stage_v1(
      old.task_id,'fenced_worker_a',old.fenced_epoch,old.fenced_token,
      'scout','{"stale":true}'::jsonb,'outcome',false);
    RAISE EXCEPTION 'ASSERTION_FAILED: stale_same_owner_commit_accepted';
  EXCEPTION WHEN OTHERS THEN
    IF SQLERRM NOT LIKE '%fenced_stage_stale_or_unauthorized%' THEN RAISE; END IF;
  END;
  PERFORM hl_control.fail_fenced_task_v1(
    current_lease.task_id,'fenced_worker_a',current_lease.fenced_epoch,
    current_lease.fenced_token,'operator_abort');
END $t$;
SELECT public.assert_true(
  (SELECT status='dead_letter' AND fenced_token IS NULL
   FROM hl_control.tasks WHERE task_id='fenced_restart'),
  'abort_revoke_fenced_lease_without_auto_retry'
);
SELECT public.assert_true(
  (SELECT count(*)=1 FROM hl_control.events
   WHERE task_id='fenced_restart' AND event_type='fenced_task_dead_letter'),
  'authorized_abort_emits_exactly_one_terminal_event'
);
SELECT public.assert_true(
  (SELECT count(*)=2 FROM hl_control.dead_letters
   WHERE task_id='fenced_restart'),
  'each_distinct_abandoned_generation_is_logged_once'
);

-- Backward-compatibility proof: legitimate UNFENCED legacy work retains
-- renewal, stage progression, prior retry semantics, expiry handling and v2 role.
SELECT public.assert_true(
  (hl_control.renew_task_lease('legacy_queue','fenced_worker_b',60)).status='leased',
  'legacy_unfenced_renew_must_remain_available'
);
SELECT public.assert_true(
  (hl_control.advance_task_stage('legacy_queue','fenced_worker_b','scout',
    '{"legacy":true}'::jsonb,'outcome',false)).current_stage='outcome',
  'legacy_unfenced_advance_must_remain_available'
);
SELECT public.assert_true(
  (hl_control.fail_task('legacy_queue','fenced_worker_b','synthetic_legacy_retry')).status='queued',
  'legacy_unfenced_fail_must_requeue_when_attempts_remain'
);
SELECT public.assert_true(
  (hl_control.claim_next_task('fenced_worker_a',60)).task_id='legacy_queue',
  'legacy_unfenced_reclaim_must_remain_available'
);
UPDATE hl_control.tasks SET lease_expires_at=clock_timestamp()-interval '2 seconds'
WHERE task_id='legacy_queue';
SELECT public.assert_true(
  hl_control.release_expired_leases()=1,
  'legacy_unfenced_expiry_compatibility_must_remain'
);
SELECT public.assert_true(
  (SELECT status='queued' AND attempts=2 FROM hl_control.tasks
    WHERE task_id='legacy_queue'),
  'legacy_expiry_retains_prior_attempt_accounting'
);
SELECT public.assert_true(
  (hl_control.claim_next_task('fenced_worker_a',60)).task_id='legacy_queue',
  'legacy_unfenced_claim_after_expiry_remains'
);
SELECT public.assert_true(
  (hl_control.advance_task_stage_v2('legacy_queue','fenced_worker_a',
     'fenced_child_a','outcome','{"legacy_v2":true}'::jsonb,NULL,true)).status='completed',
  'legacy_unfenced_role_v2_completion_remains'
);
SELECT public.assert_true(
  (SELECT count(*)=1 FROM hl_control.events
    WHERE task_id='legacy_queue' AND event_type='task_completed'),
  'legacy_unfenced_completion_audit_retained'
);

-- Never claim any outside impact or real model acceptance from synthetic DB.
SELECT 'FENCED_CANONICAL_LEASE_SQL_TESTS_PASSED' AS result;
