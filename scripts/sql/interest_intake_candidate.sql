-- Offline PostgreSQL candidate ONLY. No public RPC, gateway grants or collection.
-- Hash of a participant-held random 256-bit interest ticket, not a node token.
BEGIN;
CREATE SCHEMA hl_interest_candidate;
REVOKE ALL ON SCHEMA hl_interest_candidate FROM PUBLIC,anon,authenticated,service_role;
CREATE TABLE hl_interest_candidate.budget(
 singleton boolean PRIMARY KEY CHECK(singleton),
 capacity integer NOT NULL CHECK(capacity BETWEEN 0 AND 10000),
 occupied integer NOT NULL CHECK(occupied BETWEEN 0 AND capacity)
);
INSERT INTO hl_interest_candidate.budget VALUES(true,0,0);
CREATE TABLE hl_interest_candidate.tickets(
 ticket_hash text PRIMARY KEY CHECK(ticket_hash ~ '^[0-9a-f]{64}$'),
 consent_version text NOT NULL CHECK(consent_version='interest-v1'),
 created_at timestamptz NOT NULL,
 expires_at timestamptz NOT NULL CHECK(expires_at=created_at+interval '30 days')
);
CREATE INDEX ON hl_interest_candidate.tickets(expires_at);
ALTER TABLE hl_interest_candidate.budget ENABLE ROW LEVEL SECURITY;
ALTER TABLE hl_interest_candidate.tickets ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON ALL TABLES IN SCHEMA hl_interest_candidate FROM PUBLIC,anon,authenticated,service_role;
-- Every mutation serializes on the one budget row. Expired entries count
-- against capacity until an explicitly authorized bounded purge.
CREATE FUNCTION hl_interest_candidate.record_interest(h text, consent boolean, version text)
RETURNS text LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
DECLARE old_expiry timestamptz; cap integer; used integer; t timestamptz;
BEGIN
 IF h IS NULL OR h !~ '^[0-9a-f]{64}$' OR consent IS DISTINCT FROM true OR version IS DISTINCT FROM 'interest-v1'
 THEN RETURN 'invalid'; END IF;
 SELECT capacity,occupied INTO cap,used FROM hl_interest_candidate.budget WHERE singleton FOR UPDATE;
 IF NOT FOUND THEN RETURN 'closed'; END IF;
 t:=clock_timestamp();
 SELECT expires_at INTO old_expiry FROM hl_interest_candidate.tickets WHERE ticket_hash=h;
 IF FOUND THEN
   IF old_expiry<=t THEN RETURN 'expired'; END IF;
   RETURN 'already_recorded';
 END IF;
 IF used>=cap THEN RETURN 'closed'; END IF;
 INSERT INTO hl_interest_candidate.tickets VALUES(h,version,t,t+interval '30 days');
 UPDATE hl_interest_candidate.budget SET occupied=occupied+1 WHERE singleton;
 RETURN 'recorded';
END $$;
CREATE FUNCTION hl_interest_candidate.withdraw_interest(h text)
RETURNS text LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
BEGIN
 IF h IS NULL OR h !~ '^[0-9a-f]{64}$' THEN RETURN 'invalid'; END IF;
 PERFORM 1 FROM hl_interest_candidate.budget WHERE singleton FOR UPDATE;
 IF NOT FOUND THEN RETURN 'closed'; END IF;
 DELETE FROM hl_interest_candidate.tickets WHERE ticket_hash=h;
 IF FOUND THEN
   UPDATE hl_interest_candidate.budget SET occupied=occupied-1 WHERE singleton;
 END IF;
 RETURN 'withdrawn_or_absent';
END $$;
CREATE FUNCTION hl_interest_candidate.purge_expired(batch integer)
RETURNS integer LANGUAGE plpgsql SECURITY INVOKER SET search_path=pg_catalog,pg_temp AS $$
DECLARE removed integer;
BEGIN
 IF batch IS NULL OR batch NOT BETWEEN 1 AND 500 THEN RAISE EXCEPTION 'invalid purge batch'; END IF;
 PERFORM 1 FROM hl_interest_candidate.budget WHERE singleton FOR UPDATE;
 IF NOT FOUND THEN RAISE EXCEPTION 'missing budget'; END IF;
 WITH due AS (
   SELECT ticket_hash FROM hl_interest_candidate.tickets
   WHERE expires_at<=clock_timestamp() ORDER BY expires_at,ticket_hash LIMIT batch
 )
 DELETE FROM hl_interest_candidate.tickets t USING due WHERE t.ticket_hash=due.ticket_hash;
 GET DIAGNOSTICS removed=ROW_COUNT;
 UPDATE hl_interest_candidate.budget SET occupied=occupied-removed WHERE singleton;
 RETURN removed;
END $$;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA hl_interest_candidate FROM PUBLIC,anon,authenticated,service_role;
COMMIT;
