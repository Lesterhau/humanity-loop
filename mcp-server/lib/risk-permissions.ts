/** Public registration calls use tier1-auto; the current node database stores tier1. */
export type PublicRiskPermission = "tier0" | "tier1-auto" | "tier2-review";
export type StoredRiskPermission = "tier0" | "tier1" | "tier2-review";

export function normalizeRiskPermissions(
  requested?: readonly PublicRiskPermission[],
  allowTier1Review = false,
): StoredRiskPermission[] {
  const selected = requested?.length
    ? requested
    : allowTier1Review
      ? (["tier0", "tier2-review"] as const)
      : (["tier0", "tier1-auto", "tier2-review"] as const);

  return [...new Set(selected.map((permission) =>
    permission === "tier1-auto" ? "tier1" : permission,
  ))];
}
