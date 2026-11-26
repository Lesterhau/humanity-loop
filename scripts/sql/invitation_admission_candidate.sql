-- DISPOSABLE fixture only. Not a deployed schema or migration.
-- Run after the original cap and interest rehearsals. No real invitation or token.
BEGIN;
ALTER TABLE hl_control.contributor_nodes ADD COLUMN invitation_hash text UNIQUE;
CREATE TABLE hl_control.invitation_candidate (
  invitation_hash text PRIMARY KEY CHECK(invitation_hash ~ '^[0-9a-f]{64}$'),
  expires_at timestamptz NOT NULL,
  node_id uuid UNIQUE REFERENCES hl_control.contributor_nodes(node_id),
  token_hash text CHECK(token_hash ~ '^[0-9a-f]{64}$'),
  CHECK((node_id IS NULL)=(token_hash IS NULL))
);
ALTER TABLE hl_control.invitation_candidate ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON hl_control.invitation_candidate FROM PUBLIC,anon,authenticated,service_role;

-- Issuance reserves one of the remaining approved cumulative slots.
-- The budget row is the first lock in issuance, redemption, and the cap trigger.
-- All functions are fixture-owner-only invokers, not public RPCs.
CREATE FUNCTION hl_control.issue_invitation_candidate(h text, expiry timestamptz) RETURNS void
LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
DECLARE remaining integer;
BEGIN
 IF h IS NULL OR h !~ '^[0-9a-f]{64}$' OR expiry IS NULL OR
    expiry<=clock_timestamp() OR expiry>clock_timestamp()+interval '1 day'
 THEN RAISE EXCEPTION 'invitation_unavailable'; END IF;
 SELECT approved_total-admitted_total INTO STRICT remaining
 FROM hl_control.admission_budget_candidate WHERE singleton FOR UPDATE;
 IF remaining <= (SELECT count(*) FROM hl_control.invitation_candidate
                  WHERE node_id IS NULL AND expires_at>clock_timestamp())
 THEN RAISE EXCEPTION 'invitation_capacity_unavailable'; END IF;
 INSERT INTO hl_control.invitation_candidate(invitation_hash,expires_at) VALUES(h,expiry);
END $$;

-- This AFTER INSERT fires after the existing admission_capacity_candidate
-- trigger (alphabetical ordering). Any rejection rolls back the INSERT and
-- counter increment; ON CONFLICT DO NOTHING never consumes an invitation.
CREATE FUNCTION hl_control.enforce_invitation_candidate() RETURNS trigger
LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
BEGIN
 UPDATE hl_control.invitation_candidate SET node_id=NEW.node_id,token_hash=NEW.token_hash
 WHERE invitation_hash=NEW.invitation_hash AND node_id IS NULL
       AND expires_at>clock_timestamp();
 IF NOT FOUND THEN RAISE EXCEPTION 'invitation_unavailable'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER admission_invitation_candidate AFTER INSERT ON hl_control.contributor_nodes
FOR EACH ROW EXECUTE FUNCTION hl_control.enforce_invitation_candidate();

-- Caller generates and securely retains the same high-entropy token before
-- the initial request. Only its hash reaches this SQL; never re-key a node.
-- An identical retry returns the same active node ID until invitation expiry.
CREATE FUNCTION hl_control.redeem_invitation_candidate(h text,t text) RETURNS uuid
LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
DECLARE inv hl_control.invitation_candidate%ROWTYPE; result uuid;
BEGIN
 IF h IS NULL OR t IS NULL OR h !~ '^[0-9a-f]{64}$' OR t !~ '^[0-9a-f]{64}$'
 THEN RAISE EXCEPTION 'invitation_unavailable'; END IF;
 PERFORM 1 FROM hl_control.admission_budget_candidate WHERE singleton FOR UPDATE;
 SELECT * INTO inv FROM hl_control.invitation_candidate WHERE invitation_hash=h FOR UPDATE;
 IF NOT FOUND OR inv.expires_at<=clock_timestamp() THEN RAISE EXCEPTION 'invitation_unavailable'; END IF;
 IF inv.node_id IS NOT NULL THEN
   IF inv.token_hash<>t OR NOT EXISTS(SELECT 1 FROM hl_control.contributor_nodes
       WHERE node_id=inv.node_id AND token_hash=t AND status='active')
   THEN RAISE EXCEPTION 'invitation_unavailable'; END IF;
   RETURN inv.node_id;
 END IF;
 INSERT INTO hl_control.contributor_nodes(token_hash,invitation_hash)
 VALUES(t,h) RETURNING node_id INTO result;
 RETURN result;
END $$;
REVOKE ALL ON FUNCTION hl_control.issue_invitation_candidate(text,timestamptz),
 hl_control.enforce_invitation_candidate(),hl_control.redeem_invitation_candidate(text,text)
 FROM PUBLIC,anon,authenticated,service_role;
COMMIT;
