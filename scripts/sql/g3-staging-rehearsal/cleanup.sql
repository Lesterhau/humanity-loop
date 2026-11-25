DROP SCHEMA hl_g3_rehearsal CASCADE;
DROP ROLE hl_g3_rehearsal_a,hl_g3_rehearsal_b,hl_g3_rehearsal_unbound;
DO $$ BEGIN
 IF to_regnamespace('hl_g3_rehearsal') IS NOT NULL OR EXISTS(SELECT 1 FROM pg_roles WHERE rolname IN ('hl_g3_rehearsal_a','hl_g3_rehearsal_b','hl_g3_rehearsal_unbound')) THEN RAISE EXCEPTION 'rehearsal residue'; END IF;
 IF (SELECT count(*) FROM hl_control.events)<>1 OR NOT EXISTS(SELECT 1 FROM hl_control.events WHERE event_id=1 AND payload='{"sentinel":"existing"}'::jsonb) OR (SELECT count(*) FROM hl_foundry_test.tasks)<>1 OR NOT EXISTS(SELECT 1 FROM hl_foundry_test.tasks WHERE task_id='baseline' AND payload='{"sentinel":"existing"}'::jsonb) THEN RAISE EXCEPTION 'baseline changed'; END IF;
END $$;
