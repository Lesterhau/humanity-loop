-- Disposable rehearsal only. Same assertions as the canonical lease workflow,
-- applied to the renamed rehearsal schema and roles.
\set hl_schema hl_g3_rehearsal
\set hl_role_prefix hl_g3_rehearsal_
\set hl_definer hl_g3_rehearsal_definer
\ir ../check_fenced_candidate_acl.sql
