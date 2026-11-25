-- Synthetic service only; verify fresh database before creating any object.
DO $$ BEGIN
 IF current_database() <> 'foundry_ci' OR current_user <> 'postgres' OR
 current_setting('server_version_num')::int NOT BETWEEN 170000 AND 179999 OR
 inet_server_addr() IS NULL OR inet_client_addr() IS NULL OR
 EXISTS(SELECT 1 FROM pg_namespace WHERE nspname IN ('hl_control','hl_foundry_test','hl_g3_rehearsal')) OR
 EXISTS(SELECT 1 FROM pg_roles WHERE rolname IN ('anon','authenticated','service_role','hl_g3_rehearsal_a','hl_g3_rehearsal_b','hl_g3_rehearsal_unbound'))
 THEN RAISE EXCEPTION 'not a fresh synthetic test database'; END IF;
END $$;
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE service_role NOLOGIN BYPASSRLS;
CREATE SCHEMA hl_control;
CREATE SCHEMA hl_foundry_test;
CREATE TABLE hl_control.events (event_id bigint PRIMARY KEY, payload jsonb);
CREATE TABLE hl_foundry_test.tasks (task_id text PRIMARY KEY, payload jsonb);
INSERT INTO hl_control.events VALUES (1, '{"sentinel":"existing"}');
INSERT INTO hl_foundry_test.tasks VALUES ('baseline', '{"sentinel":"existing"}');
ALTER TABLE hl_control.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE hl_foundry_test.tasks ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON SCHEMA hl_control,hl_foundry_test FROM PUBLIC,anon,authenticated,service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO anon,authenticated,service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO anon,authenticated,service_role;
