-- Disposable PostgreSQL fixture only, NOT deployed schema parity.
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE ROLE service_role NOLOGIN;
CREATE SCHEMA hl_control;
CREATE TABLE hl_control.contributor_nodes(node_id uuid PRIMARY KEY DEFAULT gen_random_uuid(), token_hash text UNIQUE NOT NULL, status text NOT NULL DEFAULT 'active' CHECK(status IN ('active','paused','revoked')));
ALTER TABLE hl_control.contributor_nodes ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON SCHEMA hl_control FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON hl_control.contributor_nodes FROM PUBLIC,anon,authenticated,service_role;
-- Existing registrations are preserved without granting new ones.
INSERT INTO hl_control.contributor_nodes(token_hash) VALUES ('existing-fixture');
