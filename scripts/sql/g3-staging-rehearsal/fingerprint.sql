-- Read-only fingerprint of selected persistent catalog state, not a full cluster backup.
-- Only disposable fixture; never print raw output or inspect credentials.
SELECT jsonb_build_object(
 'database',(SELECT jsonb_build_array(datname,datdba,datacl) FROM pg_database WHERE datname=current_database()),
 'roles',(SELECT jsonb_agg(to_jsonb(r) ORDER BY rolname) FROM pg_roles r),
 'members',(SELECT jsonb_agg(to_jsonb(m) ORDER BY roleid,member,grantor) FROM pg_auth_members m),
 'defaults',(SELECT jsonb_agg(to_jsonb(a) ORDER BY oid) FROM pg_default_acl a),
 'schemas',(SELECT jsonb_agg(jsonb_build_array(oid,nspname,nspowner,nspacl) ORDER BY oid) FROM pg_namespace WHERE nspname !~ '^pg_(temp|toast_temp)'),
 'relations',(SELECT jsonb_agg(jsonb_build_array(c.oid,c.relname,c.relkind,c.relowner,c.relacl,c.relrowsecurity,c.relforcerowsecurity) ORDER BY c.oid) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname IN ('public','hl_control','hl_foundry_test','hl_g3_rehearsal')),
 'columns',(SELECT jsonb_agg(jsonb_build_array(c.oid,a.attnum,a.attname,a.atttypid,a.attnotnull,a.attacl) ORDER BY c.oid,a.attnum) FROM pg_attribute a JOIN pg_class c ON c.oid=a.attrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname IN ('public','hl_control','hl_foundry_test','hl_g3_rehearsal') AND a.attnum>0 AND NOT a.attisdropped),
 'functions',(SELECT jsonb_agg(jsonb_build_array(p.oid,p.proname,p.proowner,p.proacl,p.prosecdef,p.proconfig,pg_get_functiondef(p.oid)) ORDER BY p.oid) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname IN ('public','hl_control','hl_foundry_test','hl_g3_rehearsal') AND p.prokind IN ('f','p','w')),
 'policies',(SELECT jsonb_agg(to_jsonb(p) ORDER BY schemaname,tablename,policyname) FROM pg_policies p WHERE schemaname IN ('public','hl_control','hl_foundry_test','hl_g3_rehearsal')),
 'events',(SELECT jsonb_agg(to_jsonb(e) ORDER BY event_id) FROM hl_control.events e),
 'other_tasks',(SELECT jsonb_agg(to_jsonb(t) ORDER BY task_id) FROM hl_foundry_test.tasks t),
 'nodes',(SELECT jsonb_agg(to_jsonb(n) ORDER BY node_id) FROM hl_control.contributor_nodes n)
);
