import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const expected = readFileSync("public/.well-known/openai-apps-challenge");
assert.ok(expected.length >= 20 && expected.length <= 256, "Challenge token missing/invalid length");
assert.ok(!expected.includes(0x0a) && !expected.includes(0x0d), "Challenge token includes newline/carriage return");

for (const path of ["/.well-known/openai-apps-challenge", "/openai-apps-challenge"]) {
  const response = await fetch("http://127.0.0.1:3000" + path, { redirect: "manual" });
  assert.equal(response.status, 200, path + ": expected HTTP 200 with no redirect");
  assert.ok((response.headers.get("content-type") || "").startsWith("text/plain"), path + ": expected text/plain");
  const actual = Buffer.from(await response.arrayBuffer());
  assert.equal(actual.length, expected.length, path + ": challenge has extra/missing bytes");
  assert.ok(actual.equals(expected), path + ": challenge token bytes disagree with repo copy");
}
const manifest = JSON.parse(readFileSync("../plugin/humanity-loop/plugin.json", "utf8"));
const cases = manifest?.extensions?.["com.openai"]?.review?.test_cases;
assert.equal(cases?.positive?.length, 5, "Plugin requires five positive review cases");
assert.equal(cases?.negative?.length, 3, "Plugin requires three negative review cases");
console.log("Domain challenge raw bytes and five/three plugin review cases passed (no tokens printed).");
