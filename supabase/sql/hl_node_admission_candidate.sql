-- REVIEW CANDIDATE ONLY. NOT a deployment migration.
-- Apply only to the disposable synthetic database in the named rehearsal.
-- Total admitted records, not concurrent leases or distinct human operators.
BEGIN;
LOCK TABLE hl_control.contributor_nodes IN ACCESS EXCLUSIVE MODE;
CREATE TABLE hl_control.admission_budget_candidate (
  singleton boolean PRIMARY KEY CHECK(singleton),
  approved_total integer NOT NULL CHECK(approved_total BETWEEN 0 AND 20000),
  admitted_total integer NOT NULL CHECK(admitted_total BETWEEN 0 AND 20000),
  CHECK(admitted_total <= approved_total)
);
ALTER TABLE hl_control.admission_budget_candidate ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON hl_control.admission_budget_candidate FROM PUBLIC, anon, authenticated, service_role;
-- Closed by default: preserve preexisting rows; explicit admin increase only.
INSERT INTO hl_control.admission_budget_candidate
SELECT true, count(*)::integer, count(*)::integer FROM hl_control.contributor_nodes;
CREATE FUNCTION hl_control.enforce_admission_candidate() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,pg_temp
AS $$
BEGIN
  UPDATE hl_control.admission_budget_candidate
  SET admitted_total=admitted_total+1
  WHERE singleton IS TRUE AND admitted_total<approved_total;
  IF NOT FOUND THEN RAISE EXCEPTION USING ERRCODE='P0001', MESSAGE='admission_capacity_unavailable'; END IF;
  RETURN NEW;
END;
$$;
REVOKE ALL ON FUNCTION hl_control.enforce_admission_candidate() FROM PUBLIC,anon,authenticated,service_role;
-- AFTER INSERT counts only an actual inserted row; a failed/rolled back
-- insertion rolls back the budget increment. Do not use TRUNCATE or disable
-- triggers, or grant worker/admin bypass. Cumulative cap never auto-refills.
CREATE TRIGGER admission_capacity_candidate AFTER INSERT ON hl_control.contributor_nodes
FOR EACH ROW EXECUTE FUNCTION hl_control.enforce_admission_candidate();
COMMIT;
