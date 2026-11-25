-- Disposable PostgreSQL test only. Assert exact function catalog configuration.
DO $check$
DECLARE n integer;
BEGIN
 SELECT count(*) INTO n FROM pg_proc p JOIN pg_namespace s ON s.oid=p.pronamespace
 WHERE s.nspname='hl_control';
 IF n<>16 THEN RAISE EXCEPTION 'unexpected candidate function count: %',n; END IF;
 IF EXISTS(SELECT 1 FROM pg_proc p JOIN pg_namespace s ON s.oid=p.pronamespace
   WHERE s.nspname='hl_control' AND NOT coalesce(p.proconfig @> ARRAY['search_path=pg_catalog, pg_temp'],false))
 THEN RAISE EXCEPTION 'candidate function namespace configuration invalid'; END IF;
 IF EXISTS(SELECT 1 FROM pg_class c JOIN pg_namespace s ON s.oid=c.relnamespace
   WHERE s.nspname='hl_control' AND c.relkind IN ('r','p') AND NOT c.relrowsecurity)
 THEN RAISE EXCEPTION 'candidate relation RLS missing'; END IF;
 IF EXISTS(SELECT 1 FROM pg_roles r WHERE r.rolname IN ('hl_test_executor_a','hl_test_executor_b','hl_test_executor_unbound')
   AND (r.rolsuper OR r.rolbypassrls OR r.rolcreaterole OR r.rolcreatedb OR r.rolreplication OR r.rolinherit
        OR has_database_privilege(r.oid,current_database(),'TEMP')
        OR EXISTS(SELECT 1 FROM pg_auth_members m WHERE m.member=r.oid)))
 THEN RAISE EXCEPTION 'executor attributes or database privilege invalid'; END IF;
END $check$;
SELECT 'CANDIDATE_NAMESPACE_AND_PRIVILEGE_CHECK_PASSED';
