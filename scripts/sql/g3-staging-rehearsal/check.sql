DO $$ DECLARE r text; t record; f record; p text; BEGIN
 FOREACH r IN ARRAY ARRAY['anon','authenticated','service_role','hl_g3_rehearsal_a','hl_g3_rehearsal_b','hl_g3_rehearsal_unbound'] LOOP
  IF has_schema_privilege(r,'hl_g3_rehearsal','CREATE') THEN RAISE EXCEPTION 'schema CREATE allowed: %',r; END IF;
  IF r IN ('anon','authenticated','service_role') AND has_schema_privilege(r,'hl_g3_rehearsal','USAGE') THEN RAISE EXCEPTION 'API schema USAGE allowed: %',r; END IF;
  FOR t IN SELECT c.oid,c.relrowsecurity,c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='hl_g3_rehearsal' AND c.relkind IN ('r','p') LOOP
   IF NOT t.relrowsecurity THEN RAISE EXCEPTION 'RLS missing: %',t.relname; END IF;
   FOREACH p IN ARRAY ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER','MAINTAIN'] LOOP
    IF has_table_privilege(r,t.oid,p) THEN RAISE EXCEPTION 'direct table grant: % % %',r,t.relname,p; END IF;
   END LOOP;
  END LOOP;
  FOR t IN SELECT c.oid,c.relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='hl_g3_rehearsal' AND c.relkind='S' LOOP
   FOREACH p IN ARRAY ARRAY['SELECT','UPDATE','USAGE'] LOOP
    IF has_sequence_privilege(r,t.oid,p) THEN RAISE EXCEPTION 'sequence grant: % % %',r,t.relname,p; END IF;
   END LOOP;
  END LOOP;
  FOR f IN SELECT p.oid,p.proname FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='hl_g3_rehearsal' LOOP
   IF has_function_privilege(r,f.oid,'EXECUTE') AND NOT (r IN ('hl_g3_rehearsal_a','hl_g3_rehearsal_b') AND f.proname IN ('fenced_executor_claim_v1','fenced_executor_advance_v1','fenced_executor_renew_v1','fenced_executor_abort_v1') OR r='hl_g3_rehearsal_unbound' AND f.proname='fenced_executor_claim_v1') THEN
    RAISE EXCEPTION 'unexpected EXECUTE: % %',r,f.proname;
   END IF;
  END LOOP;
 END LOOP;
END $$;
