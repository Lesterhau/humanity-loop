# Contributor Node gateway v5: bounded-body and generic-error proposal

**Status:** TESTED PROPOSAL ONLY — not merged into the deployed Edge Function; no production request or redeployment.  
**Owner:** Humanity Loop Security Review + contributor-gateway maintainer.  
**Related:** [issue #20](https://github.com/Lesterhau/humanity-loop/issues/20).  
**Observed deployed source:** Supabase Edge Function `contributor-node`, version 5, retrieved read-only 2026-10-28 UTC.  
**Tier:** 0 (defensive code review / deterministic local tests); production changes require separate authorized review and rollback.

## INTEND and exact defect

Prepare a minimal, independently testable replacement for two specific deployed-source patterns, without touching production:

1. `Number(content-length || "0") > 65536` followed by `await req.json()` trusts a missing/understated header and does not bound bytes read from a streaming body.
2. The outer exception handler sends `detail: message.slice(0, 300)` to callers, where `message` may contain the upstream RPC response body. This can disclose implementation detail; **no actual secret disclosure has been observed**.

## Proposed helper (drop into the Edge Function, not yet deployed)

```ts
const MAX_BODY_BYTES = 65_536;

class PayloadTooLargeError extends Error {
  constructor() {
    super("payload too large");
    this.name = "PayloadTooLargeError";
  }
}

async function readBoundedJson(req: Request): Promise<unknown> {
  // Header is an optimization only; streaming bytes remain authoritative.
  const declared = req.headers.get("content-length");
  if (declared !== null && /^\d+$/.test(declared) &&
      Number(declared) > MAX_BODY_BYTES) {
    throw new PayloadTooLargeError();
  }
  if (!req.body) throw new SyntaxError("empty request body");

  const reader = req.body.getReader();
  const chunks: Uint8Array[] = [];
  let bytes = 0;
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      if (bytes > MAX_BODY_BYTES) {
        await reader.cancel().catch(() => {});
        throw new PayloadTooLargeError();
      }
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }

  const payload = new Uint8Array(bytes);
  let offset = 0;
  for (const chunk of chunks) {
    payload.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(payload));
}
```

Replace the current header-only check and `await req.json()` with:

```ts
let body: any;
try {
  body = await readBoundedJson(req);
} catch (err) {
  if (err instanceof PayloadTooLargeError) {
    return json({ error: "payload_too_large" }, 413);
  }
  return json({ error: "invalid_json" }, 400);
}
```

Replace the outer exception handler with a fixed client response. Do **not** log raw upstream response text, credentials, token hashes, or user-submitted data:

```ts
} catch (err) {
  const errorClass = err instanceof Error ? err.name : "unknown";
  console.error("node-gateway internal failure", { action, errorClass });
  return json({ error: "request_failed" }, 500);
}
```

**Compatibility note:** A backend failure formerly returned HTTP 400 with a `detail` field; proposed response is HTTP 500 with only `error`. Confirm that the onboarding UI and MCP clients do not rely on the old status/detail. Existing deliberate 400/401/403/429 responses outside this catch remain unchanged.

## Reproducible local validation, not a production acceptance test

Executed a standalone Node.js v22.16.0 `node --test` harness using the same `Request`/`ReadableStream`/TextDecoder logic and a generic-error response assertion. **9/9 passed** on 2026-10-28 UTC:

| Test | Result |
|---|---|
| Normal JSON request | PASS |
| Missing Content-Length with oversized chunked stream | PASS: 413-class exception |
| Understated Content-Length with oversized body | PASS: 413-class exception |
| Declared oversized body | PASS: 413-class exception |
| Exactly 65,536-byte valid JSON | PASS |
| Malformed JSON | PASS: rejected |
| Invalid UTF-8 | PASS: rejected |
| Missing body | PASS: rejected |
| Internal-error response omits backend message | PASS |

These tests exercise a **standalone copy** of the proposed helper, not the live Supabase runtime. They do not prove actual gateway integration, endpoint authentication, CORS behavior, service-role isolation, RPC error classification, or deployment safety.

## Mandatory acceptance before production

1. Implement in the maintained source of the active function; review diff and source provenance. Never paste environment secrets into GitHub.
2. Run deterministic Deno/Edge tests for missing, false, oversized and chunked Content-Length; malformed UTF-8/JSON; exact boundary; upstream RPC error; and no backend details in client-visible responses.
3. Confirm real onboarding UI and authorized `visit`, `register`, `checkin`, `submit`, and `pause` workflows still work, including valid error status handling, without generating fake adoption.
4. Review logging and privacy retention; prepare rollback to version 5; obtain existing production-approval gate.
5. Deploy once through authorized tooling, then independently read back the **new version/source** and run explicitly authorized non-destructive acceptance checks. Do not mark issue #20 fixed until then.

**Accounting:** tested defensive proposal 1; deployed remediation 0; verified external security improvement 0; contributor activation 0; beneficiary effect 0.
