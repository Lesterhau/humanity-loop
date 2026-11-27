-- Disposable PostgreSQL test only. Read-only: asserts the exact ownership,
-- namespace and privilege shape of the fenced lease candidate and raises on
-- the first deviation. It changes nothing.
--
-- Required psql variables:
--   hl_schema       schema holding the candidate objects
--   hl_role_prefix  prefix of the three test executor logins
--                   (<prefix>a, <prefix>b, <prefix>unbound)
--   hl_definer      NOLOGIN role that owns the SECURITY DEFINER wrappers
--
-- Every non-superuser role in the cluster is audited, not a fixed list, so a
-- grant to a role nobody thought of is still found. Privileges reached through
-- PUBLIC or inherited membership count. A hosted database with other objects
-- in the schema needs its own reviewed allowlist before this check applies.
\if :{?hl_allow_public_temp}
\else
\set hl_allow_public_temp false
\endif
SELECT pg_catalog.set_config('hl_check.allow_public_temp', :'hl_allow_public_temp', false) AS hl_check_temp \gset
SELECT pg_catalog.set_config('hl_check.schema', :'hl_schema', false) AS hl_check_1,
       pg_catalog.set_config('hl_check.role_prefix', :'hl_role_prefix', false) AS hl_check_2,
       pg_catalog.set_config('hl_check.definer', :'hl_definer', false) AS hl_check_3 \gset

DO $check$
DECLARE
  v_schema   pg_catalog.text := pg_catalog.current_setting('hl_check.schema');
  v_prefix   pg_catalog.text := pg_catalog.current_setting('hl_check.role_prefix');
  v_definer  pg_catalog.text := pg_catalog.current_setting('hl_check.definer');
  v_ns        pg_catalog.oid;
  v_ns_owner  pg_catalog.oid;
  v_definer_oid pg_catalog.oid;
  v_exec      pg_catalog.text[] := ARRAY[v_prefix || 'a', v_prefix || 'b', v_prefix || 'unbound'];
  v_bound     pg_catalog.text[] := ARRAY[v_prefix || 'a', v_prefix || 'b'];
  v_safe_path pg_catalog.text[] := ARRAY['search_path=pg_catalog, pg_temp'];
  v_table_privs pg_catalog.text[] := ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER'];
  v_column_privs pg_catalog.text[] := ARRAY['SELECT','INSERT','UPDATE','REFERENCES'];
  v_task_update_cols pg_catalog.text[] := ARRAY['attempts','completed_at','current_stage','fenced_epoch',
    'fenced_token','lease_expires_at','lease_owner','stage_results','status','updated_at'];
  v_agent_select_cols pg_catalog.text[] := ARRAY['agent_id','expires_at','permissions','status'];
  r record; c record; f record; x record;
  v_priv pg_catalog.text; v_kind pg_catalog.text; v_ident pg_catalog.text;
  v_allowed boolean; v_cols pg_catalog.text[]; v_seen pg_catalog.text[] := '{}';
  v_is_definer boolean;
BEGIN
  IF pg_catalog.current_setting('server_version_num')::pg_catalog.int4 >= 170000 THEN
    v_table_privs := v_table_privs || 'MAINTAIN'::pg_catalog.text;
  END IF;

  SELECT n.oid, n.nspowner INTO v_ns, v_ns_owner
  FROM pg_catalog.pg_namespace n WHERE n.nspname = v_schema;
  IF v_ns IS NULL THEN RAISE EXCEPTION 'ACL_CHECK schema missing: %', v_schema; END IF;
  SELECT o.oid INTO v_definer_oid FROM pg_catalog.pg_roles o WHERE o.rolname = v_definer;
  IF v_definer_oid IS NULL THEN RAISE EXCEPTION 'ACL_CHECK wrapper owner role missing: %', v_definer; END IF;

  -- 1. Role attributes and membership.
  FOR r IN SELECT * FROM pg_catalog.pg_roles o WHERE o.rolname = ANY (v_exec || v_definer) LOOP
    IF r.rolsuper OR r.rolbypassrls OR r.rolcreaterole OR r.rolcreatedb OR r.rolreplication OR r.rolinherit THEN
      RAISE EXCEPTION 'ACL_CHECK unsafe role attributes: %', r.rolname;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_catalog.pg_auth_members m WHERE m.member = r.oid) THEN
      RAISE EXCEPTION 'ACL_CHECK role is a member of another role: %', r.rolname;
    END IF;
    -- A creator's bare ADMIN OPTION row is tolerated; the ability to assume or inherit is not.
    IF EXISTS (SELECT 1 FROM pg_catalog.pg_auth_members m
               WHERE m.roleid = r.oid AND (m.set_option OR m.inherit_option)) THEN
      RAISE EXCEPTION 'ACL_CHECK another role can assume or inherit: %', r.rolname;
    END IF;
    -- Only the explicitly selected disposable hosted-shaped test permits TEMP.
    -- CREATE on the database remains forbidden; canonical checks remain strict.
    IF (pg_catalog.current_setting('hl_check.allow_public_temp') <> 'true'
        AND pg_catalog.has_database_privilege(r.oid, pg_catalog.current_database(), 'TEMP'))
       OR pg_catalog.has_database_privilege(r.oid, pg_catalog.current_database(), 'CREATE') THEN
      RAISE EXCEPTION 'ACL_CHECK database TEMP or CREATE allowed: %', r.rolname;
    END IF;
    IF r.rolname = v_definer AND r.rolcanlogin THEN
      RAISE EXCEPTION 'ACL_CHECK wrapper owner role can log in: %', r.rolname;
    END IF;
  END LOOP;
  IF (SELECT pg_catalog.count(*) FROM pg_catalog.pg_roles o WHERE o.rolname = ANY (v_exec)) <> 3 THEN
    RAISE EXCEPTION 'ACL_CHECK expected three test executor roles with prefix %', v_prefix;
  END IF;

  -- 2. Schema privileges and default privileges.
  FOR r IN SELECT o.oid, o.rolname FROM pg_catalog.pg_roles o
           WHERE NOT o.rolsuper AND o.rolname !~ '^pg_' AND o.oid <> v_ns_owner LOOP
    IF pg_catalog.has_schema_privilege(r.oid, v_ns, 'CREATE') THEN
      RAISE EXCEPTION 'ACL_CHECK schema CREATE allowed: %', r.rolname;
    END IF;
    IF pg_catalog.has_schema_privilege(r.oid, v_ns, 'USAGE')
       AND NOT (r.rolname = ANY (v_exec) OR r.rolname = v_definer) THEN
      RAISE EXCEPTION 'ACL_CHECK schema USAGE allowed: %', r.rolname;
    END IF;
  END LOOP;
  IF EXISTS (SELECT 1 FROM pg_catalog.pg_default_acl d WHERE d.defaclnamespace = v_ns) THEN
    RAISE EXCEPTION 'ACL_CHECK default privileges are defined for schema %', v_schema;
  END IF;

  -- 3. Relations: kinds, row level security, table, column and sequence privileges.
  FOR c IN SELECT k.oid, k.relname, k.relkind, k.relowner, k.relrowsecurity
           FROM pg_catalog.pg_class k
           WHERE k.relnamespace = v_ns AND k.relkind IN ('r','p','v','m','f','S') LOOP
    IF c.relkind IN ('v','m','f') THEN
      RAISE EXCEPTION 'ACL_CHECK unexpected relation kind % for %', c.relkind, c.relname;
    END IF;
    IF c.relkind IN ('r','p') THEN
      IF c.relname NOT IN ('agents','tasks','events','dead_letters','fenced_executor_bindings') THEN
        RAISE EXCEPTION 'ACL_CHECK unexpected table: %', c.relname;
      END IF;
      IF NOT c.relrowsecurity THEN RAISE EXCEPTION 'ACL_CHECK row level security missing: %', c.relname; END IF;
      IF EXISTS (SELECT 1 FROM pg_catalog.pg_policy p
                 WHERE p.polrelid = c.oid AND p.polroles <> ARRAY[v_definer_oid]) THEN
        RAISE EXCEPTION 'ACL_CHECK policy applies to a role other than the wrapper owner: %', c.relname;
      END IF;
    END IF;
    FOR r IN SELECT o.oid, o.rolname FROM pg_catalog.pg_roles o
             WHERE NOT o.rolsuper AND o.rolname !~ '^pg_' AND o.oid <> c.relowner LOOP
      v_is_definer := (r.rolname = v_definer);
      IF c.relkind = 'S' THEN
        FOREACH v_priv IN ARRAY ARRAY['SELECT','UPDATE','USAGE'] LOOP
          v_allowed := v_is_definer AND v_priv = 'USAGE' AND EXISTS (
            SELECT 1 FROM pg_catalog.pg_depend d JOIN pg_catalog.pg_class t ON t.oid = d.refobjid
            WHERE d.objid = c.oid AND d.deptype = 'a' AND t.relname IN ('events','dead_letters'));
          IF pg_catalog.has_sequence_privilege(r.oid, c.oid, v_priv) AND NOT v_allowed THEN
            RAISE EXCEPTION 'ACL_CHECK sequence privilege: % % %', r.rolname, c.relname, v_priv;
          END IF;
        END LOOP;
        CONTINUE;
      END IF;
      FOREACH v_priv IN ARRAY v_table_privs LOOP
        v_allowed := v_is_definer AND (
             (v_priv = 'SELECT' AND c.relname IN ('tasks','fenced_executor_bindings'))
          OR (v_priv = 'INSERT' AND c.relname IN ('events','dead_letters')));
        IF pg_catalog.has_table_privilege(r.oid, c.oid, v_priv) IS DISTINCT FROM v_allowed THEN
          RAISE EXCEPTION 'ACL_CHECK table privilege differs from expected: % % % (expected %)',
            r.rolname, c.relname, v_priv, v_allowed;
        END IF;
      END LOOP;
      FOREACH v_priv IN ARRAY v_column_privs LOOP
        SELECT COALESCE(pg_catalog.array_agg(a.attname::pg_catalog.text ORDER BY a.attname::pg_catalog.text COLLATE "C"), '{}')
          INTO v_cols
        FROM pg_catalog.pg_attribute a
        WHERE a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
          AND pg_catalog.has_column_privilege(r.oid, c.oid, a.attnum, v_priv)
          AND NOT pg_catalog.has_table_privilege(r.oid, c.oid, v_priv);
        IF v_is_definer AND c.relname = 'tasks' AND v_priv = 'UPDATE' THEN
          IF v_cols <> v_task_update_cols THEN
            RAISE EXCEPTION 'ACL_CHECK wrapper owner UPDATE columns differ from expected: %', v_cols;
          END IF;
        ELSIF v_is_definer AND c.relname = 'agents' AND v_priv = 'SELECT' THEN
          IF v_cols <> v_agent_select_cols THEN
            RAISE EXCEPTION 'ACL_CHECK wrapper owner SELECT columns differ from expected: %', v_cols;
          END IF;
        ELSIF v_cols <> '{}' THEN
          RAISE EXCEPTION 'ACL_CHECK column privilege: % % % %', r.rolname, c.relname, v_priv, v_cols;
        END IF;
      END LOOP;
    END LOOP;
  END LOOP;

  -- 4. Functions: exact set, owner, security mode, pinned path and EXECUTE.
  FOR f IN SELECT p.oid, p.proname, p.proowner, p.prosecdef, p.proconfig,
                  p.proname || '(' || pg_catalog.oidvectortypes(p.proargtypes) || ')' AS ident
           FROM pg_catalog.pg_proc p WHERE p.pronamespace = v_ns LOOP
    v_kind := CASE f.ident
      WHEN 'fenced_bound_identity_v1()' THEN 'facade_internal'
      WHEN 'fenced_executor_claim_v1(text, text, integer)' THEN 'facade_claim'
      WHEN 'fenced_executor_advance_v1(text, bigint, uuid, text, jsonb, text, boolean)' THEN 'facade_bound'
      WHEN 'fenced_executor_renew_v1(text, bigint, uuid, integer)' THEN 'facade_bound'
      WHEN 'fenced_executor_abort_v1(text, bigint, uuid, text)' THEN 'facade_bound'
      WHEN 'claim_fenced_task_v1(text, text, text, integer)' THEN 'core'
      WHEN 'advance_fenced_stage_v1(text, text, bigint, uuid, text, jsonb, text, boolean)' THEN 'core'
      WHEN 'renew_fenced_lease_v1(text, text, bigint, uuid, integer)' THEN 'core'
      WHEN 'fail_fenced_task_v1(text, text, bigint, uuid, text)' THEN 'core'
      WHEN 'expire_fenced_task_v1(text)' THEN 'private'
      WHEN 'claim_next_task(text, integer)' THEN 'private'
      WHEN 'advance_task_stage(text, text, text, jsonb, text, boolean)' THEN 'private'
      WHEN 'advance_task_stage_v2(text, text, text, text, jsonb, text, boolean)' THEN 'private'
      WHEN 'renew_task_lease(text, text, integer)' THEN 'private'
      WHEN 'fail_task(text, text, text, jsonb)' THEN 'private'
      WHEN 'release_expired_leases()' THEN 'private'
      -- Test-only assertion helpers that the rehearsal copies into its schema.
      WHEN 'assert_true(boolean, text)' THEN 'fixture'
      WHEN 'assert_rejected(text, text)' THEN 'fixture'
      ELSE NULL END;
    IF v_kind IS NULL THEN RAISE EXCEPTION 'ACL_CHECK unexpected function: %', f.ident; END IF;
    IF v_kind <> 'fixture' THEN v_seen := v_seen || f.ident; END IF;
    IF f.prosecdef IS DISTINCT FROM (v_kind LIKE 'facade%') THEN
      RAISE EXCEPTION 'ACL_CHECK unexpected security mode: %', f.ident;
    END IF;
    IF v_kind LIKE 'facade%' AND f.proowner <> v_definer_oid THEN
      RAISE EXCEPTION 'ACL_CHECK wrapper not owned by %: %', v_definer, f.ident;
    END IF;
    IF v_kind NOT LIKE 'facade%' AND f.proowner <> v_ns_owner THEN
      RAISE EXCEPTION 'ACL_CHECK function not owned by the schema owner: %', f.ident;
    END IF;
    IF v_kind <> 'fixture' AND f.proconfig IS DISTINCT FROM v_safe_path THEN
      RAISE EXCEPTION 'ACL_CHECK function search_path is not pinned: %', f.ident;
    END IF;
    FOR r IN SELECT o.oid, o.rolname FROM pg_catalog.pg_roles o
             WHERE NOT o.rolsuper AND o.rolname !~ '^pg_' AND o.oid <> f.proowner LOOP
      v_allowed := CASE v_kind
        WHEN 'facade_claim' THEN r.rolname = ANY (v_exec)
        WHEN 'facade_bound' THEN r.rolname = ANY (v_bound)
        WHEN 'core' THEN r.rolname = v_definer
        ELSE false END;
      IF pg_catalog.has_function_privilege(r.oid, f.oid, 'EXECUTE') AND NOT v_allowed THEN
        RAISE EXCEPTION 'ACL_CHECK unexpected EXECUTE: % %', r.rolname, f.ident;
      END IF;
    END LOOP;
  END LOOP;
  IF pg_catalog.cardinality(v_seen) <> 16 THEN
    RAISE EXCEPTION 'ACL_CHECK expected 16 candidate functions, found %', pg_catalog.cardinality(v_seen);
  END IF;
END $check$;
SELECT 'CANDIDATE_NAMESPACE_AND_PRIVILEGE_CHECK_PASSED';
