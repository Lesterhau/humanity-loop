import assert from "node:assert/strict";
import { normalizeRiskPermissions } from "../lib/risk-permissions.ts";

assert.deepEqual(normalizeRiskPermissions(), ["tier0", "tier1", "tier2-review"]);
assert.deepEqual(normalizeRiskPermissions(["tier0"]), ["tier0"]);
assert.deepEqual(normalizeRiskPermissions(["tier0", "tier1-auto", "tier2-review"]), ["tier0", "tier1", "tier2-review"]);
assert.deepEqual(normalizeRiskPermissions(["tier0", "tier1-auto", "tier1-auto"]), ["tier0", "tier1"]);
assert.deepEqual(normalizeRiskPermissions(undefined, true), ["tier0", "tier2-review"]);
assert.deepEqual(normalizeRiskPermissions([], true), ["tier0", "tier2-review"]);
console.log("Permission vocabulary tests passed");
