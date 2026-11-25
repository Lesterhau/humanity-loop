-- Disposable PostgreSQL test only. Candidate schema as applied by the canonical
-- lease workflow; the assertions live in one shared file.
\set hl_schema hl_control
\set hl_role_prefix hl_test_executor_
\set hl_definer hl_fenced_definer
\ir check_fenced_candidate_acl.sql
