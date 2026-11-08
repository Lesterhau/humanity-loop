import assert from "node:assert/strict";
import { normalizeRiskPermissions } from "../lib/risk-permissions.ts";

assert.deepEqual(normalizeRiskPermissions(), ["tier0"]);
assert.deepEqual(normalizeRiskPermissions(["tier0"]), ["tier0"]);
assert.deepEqual(normalizeRiskPermissions(["tier0", "tier1-auto", "tier2-review"]), ["tier0", "tier1", "tier2-review"]);
assert.deepEqual(normalizeRiskPermissions(["tier0", "tier1-auto", "tier1-auto"]), ["tier0", "tier1"]);
assert.deepEqual(normalizeRiskPermissions(undefined, true), ["tier0"]);
assert.deepEqual(normalizeRiskPermissions(["tier0"], true), ["tier0"]);
assert.deepEqual(normalizeRiskPermissions(["tier2-review"]), ["tier2-review"]);
assert.throws(() => normalizeRiskPermissions([]), /At least one risk permission/);
assert.throws(() => normalizeRiskPermissions([], true), /At least one risk permission/);
assert.deepEqual(normalizeRiskPermissions(undefined, false), ["tier0"]);
assert.ok(!normalizeRiskPermissions().includes("tier1"));
assert.ok(!normalizeRiskPermissions(undefined, true).includes("tier2-review"));
console.log("Twelve permission vocabulary tests passed");
