-- Humanity Loop public **aggregate-only** pilot counts, 2026-11-08.
-- Designed to be called only by the private service_role behind Edge.
-- Does not return identifiers, emails, tokens, raw submitted evidence,
-- visit session data, reviewer identities or individual work records.
-- A SECURITY DEFINER function is required because the private hl_control
-- schema has no SELECT/USAGE grants for service_role; restrict EXECUTE.
BEGIN;
CREATE OR REPLACE FUNCTION public.hl_node_pilot_counts_v1()
RETURNS jsonb
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path TO ''
AS $function$
  SELECT pg_catalog.jsonb_build_object(
    'registered_nodes', (SELECT pg_catalog.count(*) FROM hl_control.contributor_nodes),
    'submissions', (SELECT pg_catalog.count(*) FROM hl_control.node_submissions),
    'awaiting_review', (SELECT pg_catalog.count(*) FROM hl_control.node_submissions WHERE status = 'quarantined'),
    'accepted', (SELECT pg_catalog.count(*) FROM hl_control.node_submissions WHERE status = 'accepted'),
    'available_tasks', (SELECT pg_catalog.count(*) FROM hl_control.node_work_items WHERE status = 'open' AND risk_tier = 0 AND expires_at > pg_catalog.now()),
    'checked_at', pg_catalog.now()
  );
$function$;
REVOKE ALL ON FUNCTION public.hl_node_pilot_counts_v1() FROM PUBLIC, anon, authenticated;
GRANT EXECUTE ON FUNCTION public.hl_node_pilot_counts_v1() TO service_role;
COMMIT;

-- Postdeployment acceptance, read-only:
-- SELECT has_function_privilege('anon',
--          'public.hl_node_pilot_counts_v1()', 'EXECUTE') = false,
--        has_function_privilege('authenticated',
--          'public.hl_node_pilot_counts_v1()', 'EXECUTE') = false,
--        has_function_privilege('service_role',
--          'public.hl_node_pilot_counts_v1()', 'EXECUTE') = true;
-- SELECT public.hl_node_pilot_counts_v1();
--
-- Rollback only AFTER gateway public_status branch is disabled:
-- DROP FUNCTION public.hl_node_pilot_counts_v1();
