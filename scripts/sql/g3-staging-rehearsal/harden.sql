-- Fixture-only helpers, not candidate security policy.
REVOKE ALL ON FUNCTION hl_g3_rehearsal.assert_true(boolean,text) FROM PUBLIC,anon,authenticated,service_role;
REVOKE ALL ON FUNCTION hl_g3_rehearsal.assert_rejected(text,text) FROM PUBLIC,anon,authenticated,service_role;
