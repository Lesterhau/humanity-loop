DO $$ DECLARE r text; t record; f record; p text; BEGIN
 FOREACH r IN ARRAY ARRAY['anon','authenticated','service_role','hl_g3_rehearsal_a','hl_g3_rehearsal_b','hl_g3_rehearsal_unbound'] LOOP
  IF r LIKE 'hl_g3_rehearsal_%' THEN
   IF EXISTS(SELECT 1 FROM pg_roles WHERE rolname=r AND (rolsuper OR rolbypassrls OR rolcreaterole OR rolcreatedb OR rolinherit OR rolreplication)) THEN RAISE EXCEPTION 'unsafe executor role attributes: %',r; END IF;
   IF EXISTS(SELECT 1 FROM pg_auth_members m JOIN pg_roles u ON u.oid=m.member WHERE u.rolname=r) THEN RAISE EXCEPTION 'executor role membership: %',r; END IF;
   IF has_database_privilege(r,current_database(),'TEMP') THEN RAISE EXCEPTION 'executor TEMP allowed: %',r; END IF;
  END IF;
  IF has_schema_privilege(r,'hl_g3_rehearsal','CREATE') THEN RAISE EXCEPTION 'schema CREATE allowed: %',r; END IF;
  IF r IN ('anon','authenticated','service_role') AND has_schema_privilege(r,'hl_g3_rehearsal','USAGE') THEN RAISE EXCEPTION 'API schema USAGE allowed: %',r; END IF;
  FOR t IN SELECT c.oid,c.relrowsecurity,c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='hl_g3_rehearsal' AND c.relkind IN ('r','p') LOOP
   IF NOT t.relrowsecurity THEN RAISE EXCEPTION 'RLS missing: %',t.relname; END IF;
   FOREACH p IN ARRAY ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER','MAINTAIN'] LOOP
    IF has_table_privilege(r,t.oid,p) THEN RAISE EXCEPTION 'direct table grant: % % %',r,t.relname,p; END IF;
   END LOOP;
   FOREACH p IN ARRAY ARRAY['SELECT','INSERT','UPDATE','REFERENCES'] LOOP
    IF has_any_column_privilege(r,t.oid,p) THEN RAISE EXCEPTION 'direct column grant: % % %',r,t.relname,p; END IF;
   END LOOP;
  END LOOP;
  FOR t IN SELECT c.oid,c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='hl_g3_rehearsal' AND c.relkind='S' LOOP
   FOREACH p IN ARRAY ARRAY['SELECT','UPDATE','USAGE'] LOOP
    IF has_sequence_privilege(r,t.oid,p) THEN RAISE EXCEPTION 'sequence grant: % % %',r,t.relname,p; END IF;
   END LOOP;
  END LOOP;
  FOR f IN SELECT p.oid,p.proname,p.proconfig,p.prosecdef FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='hl_g3_rehearsal' LOOP
   IF f.proname NOT IN ('assert_true','assert_rejected') THEN
    IF NOT coalesce(f.proconfig @> ARRAY['search_path=pg_catalog, pg_temp'],false) THEN RAISE EXCEPTION 'unsafe function path: %',f.proname; END IF;
    IF f.prosecdef IS DISTINCT FROM (f.proname LIKE 'fenced_executor_%' OR f.proname='fenced_bound_identity_v1') THEN RAISE EXCEPTION 'unexpected function security mode: %',f.proname; END IF;
   END IF;
   IF has_function_privilege(r,f.oid,'EXECUTE') AND NOT (r IN ('hl_g3_rehearsal_a','hl_g3_rehearsal_b') AND f.proname IN ('fenced_executor_claim_v1','fenced_executor_advance_v1','fenced_executor_renew_v1','fenced_executor_abort_v1') OR r='hl_g3_rehearsal_unbound' AND f.proname='fenced_executor_claim_v1') THEN
    RAISE EXCEPTION 'unexpected EXECUTE: % %',r,f.proname;
   END IF;
  END LOOP;
 END LOOP;
END $$;
