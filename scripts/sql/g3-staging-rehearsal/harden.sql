REVOKE ALL ON SCHEMA hl_g3_rehearsal FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON ALL TABLES IN SCHEMA hl_g3_rehearsal FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA hl_g3_rehearsal FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA hl_g3_rehearsal FROM PUBLIC,anon,authenticated,service_role;
DO $$ DECLARE t record; BEGIN
 FOR t IN SELECT tablename FROM pg_tables WHERE schemaname='hl_g3_rehearsal' LOOP
  EXECUTE format('ALTER TABLE hl_g3_rehearsal.%I ENABLE ROW LEVEL SECURITY',t.tablename);
 END LOOP;
END $$;
