const NODE_GATEWAY =
  "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node";

async function callGateway(
  body: Record<string, unknown>,
  nodeToken?: string,
) {
  const response = await fetch(NODE_GATEWAY, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(nodeToken ? { "x-node-token": nodeToken } : {}),
    },
    body: JSON.stringify(body),
    cache: "no-store",
  });

  const data = await response.json().catch(() => ({
    error: "invalid_gateway_response",
  }));

  if (!response.ok) {
    throw new Error(
      typeof data?.detail === "string"
        ? data.detail
        : typeof data?.error === "string"
          ? data.error
          : `Contributor gateway failed: ${response.status}`,
    );
  }

  return data;
}

export function registerContributorNode(input: {
  capabilities?: string[];
  languages?: string[];
  host?: string;
  user_agent_label?: string;
  email?: string;
  setup_email_consent?: boolean;
  risk_permissions?: Array<"tier0" | "tier1-auto" | "tier2-review">;
  /** Legacy compatibility only. Prefer risk_permissions. */
  risk_permissions?: Array<"tier0" | "tier1-auto" | "tier2-review">;
  /** Legacy compatibility only. Prefer risk_permissions. */
  allow_tier1_review?: boolean;
}) {
  return callGateway({ action: "register", ...input });
}

export function contributorCheckin(
  nodeToken: string,
  input: {
    capabilities?: string[];
    languages?: string[];
    host?: string;
    user_agent_label?: string;
  } = {},
) {
  return callGateway({ action: "checkin", ...input }, nodeToken);
}

export function submitContributorResult(
  nodeToken: string,
  input: {
    work_id: string;
    result: Record<string, unknown>;
    evidence?: unknown[];
    uncertainty?: string;
    failure_modes?: unknown[];
  },
) {
  return callGateway({ action: "submit", ...input }, nodeToken);
}

export function setContributorNodeStatus(
  nodeToken: string,
  status: "pause" | "resume" | "revoke",
) {
  return callGateway({ action: status }, nodeToken);
}
