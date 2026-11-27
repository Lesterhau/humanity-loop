-- Only disposable database. Simulated backend caller, not the real deployed RPC.
DO $$
BEGIN
  BEGIN
    INSERT INTO hl_control.contributor_nodes(token_hash) VALUES ('closed');
    RAISE EXCEPTION 'closed cap failed';
  EXCEPTION WHEN SQLSTATE 'P0001' THEN
    IF SQLERRM <> 'admission_capacity_unavailable' THEN RAISE; END IF;
  END;
  IF (SELECT admitted_total FROM hl_control.admission_budget_candidate)<>1 THEN RAISE EXCEPTION 'initial accounting'; END IF;
  IF pg_catalog.has_table_privilege('service_role','hl_control.admission_budget_candidate','UPDATE') OR
     pg_catalog.has_function_privilege('anon','hl_control.enforce_admission_candidate()','EXECUTE') OR
     pg_catalog.has_function_privilege('authenticated','hl_control.enforce_admission_candidate()','EXECUTE')
  THEN RAISE EXCEPTION 'privilege failure'; END IF;
END $$;
UPDATE hl_control.admission_budget_candidate SET approved_total=5;
-- Actual failed insert and conflict no-op cannot consume capacity.
BEGIN;
INSERT INTO hl_control.contributor_nodes(token_hash) VALUES ('rolled-back');
ROLLBACK;
INSERT INTO hl_control.contributor_nodes(token_hash) VALUES ('existing-fixture') ON CONFLICT DO NOTHING;
DO $$ BEGIN
 IF (SELECT admitted_total FROM hl_control.admission_budget_candidate)<>1 THEN RAISE EXCEPTION 'rollback or conflict consumed capacity'; END IF;
END $$;
CREATE FUNCTION public.synthetic_try_admission(v text) RETURNS text
LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
BEGIN
 INSERT INTO hl_control.contributor_nodes(token_hash) VALUES(v) ON CONFLICT DO NOTHING;
 IF FOUND THEN RETURN 'admitted'; END IF;
 RETURN 'duplicate';
EXCEPTION WHEN SQLSTATE 'P0001' THEN
 IF SQLERRM='admission_capacity_unavailable' THEN RETURN 'deferred'; END IF;
 RAISE;
END $$;
REVOKE ALL ON FUNCTION public.synthetic_try_admission(text) FROM PUBLIC,anon,authenticated,service_role;
