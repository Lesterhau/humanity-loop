import { normalizeRiskPermissions, type PublicRiskPermission } from "./risk-permissions";

import { gatewayUrl } from "./gateway-config";

async function callGateway(
  body: Record<string, unknown>,
  nodeToken?: string,
) {
  const gateway = gatewayUrl();
  if (!gateway) throw new Error("Contributor gateway is not configured in this environment; no request was sent.");
  const response = await fetch(gateway, {
    redirect: "error",
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
    if (body.action === "register") {
      if (response.status === 503 && data?.error === "admission_capacity_unavailable") {
        throw new Error("Humanity Loop's current pilot cohort is full or closed. No node was admitted by this request. Stop; do not retry automatically or create another identity. Wait for a new invitation.");
      }
      throw new Error("Registration was not confirmed. Stop and ask the pilot maintainer to reconcile the result; do not retry or create another identity.");
    }
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
  risk_permissions?: PublicRiskPermission[];
  /** Legacy compatibility only. Prefer risk_permissions. */
  allow_tier1_review?: boolean;
}) {
  return callGateway({
    action: "register",
    ...input,
    risk_permissions: normalizeRiskPermissions(input.risk_permissions, input.allow_tier1_review),
  });
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
