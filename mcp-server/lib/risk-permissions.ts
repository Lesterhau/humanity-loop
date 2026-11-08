/** Tier-0 is the only implicit permission. Tier-1 requires a deliberate explicit risk_permissions selection. */
export type PublicRiskPermission = "tier0" | "tier1-auto" | "tier2-review";
export type StoredRiskPermission = "tier0" | "tier1" | "tier2-review";

export function normalizeRiskPermissions(
  requested?: readonly PublicRiskPermission[],
  allowTier1Review = false,
): StoredRiskPermission[] {
  if (requested && requested.length === 0) {
    throw new Error("At least one risk permission is required.");
  }

  // Legacy allow_tier1_review must never silently elevate a new registration.
  void allowTier1Review;
  const selected = requested ?? (["tier0"] as const);

  return [...new Set(selected.map((permission) =>
    permission === "tier1-auto" ? "tier1" : permission,
  ))];
}
