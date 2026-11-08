
const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const secretKeysRaw = Deno.env.get("SUPABASE_SECRET_KEYS");
const legacyServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
const secretKey = secretKeysRaw ? JSON.parse(secretKeysRaw)["default"] : legacyServiceKey;

if (!SUPABASE_URL || !secretKey) {
  throw new Error("Missing Supabase backend credentials");
}

const encoder = new TextEncoder();

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "content-type, x-node-token",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Content-Type": "application/json",
    "Cache-Control": "no-store",
  };
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: corsHeaders() });
}

function clampArray(value: unknown, max = 25): string[] {
  if (!Array.isArray(value)) return [];
  return value
    .filter((v) => typeof v === "string")
    .map((v) => v.trim().slice(0, 80))
    .filter(Boolean)
    .slice(0, max);
}

function cleanString(value: unknown, max = 500): string | null {
  if (typeof value !== "string") return null;
  const s = value.trim().slice(0, max);
  return s || null;
}

async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", encoder.encode(value));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function hmac(value: string) {
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secretKey),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, encoder.encode(value));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function fingerprint(req: Request) {
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim()
    || req.headers.get("cf-connecting-ip")
    || "unknown";
  return hmac("registration:" + ip);
}

function clientSurface(req: Request) {
  const ua = req.headers.get("user-agent") || "";
  if (!ua) return "unknown";
  return /Mobi|Android|iPhone|iPad|iPod/i.test(ua) ? "mobile" : "desktop";
}

function randomToken() {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  const b64 = btoa(String.fromCharCode(...bytes))
    .replaceAll("+", "-")
    .replaceAll("/", "_")
    .replaceAll("=", "");
  return "hl_node_" + b64;
}

async function rpc(name: string, body: Record<string, unknown>) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${name}`, {
    method: "POST",
    headers: {
      "apikey": secretKey,
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(body),
  });
  const text = await res.text();
  if (!res.ok) {
    throw new Error(text || `RPC ${name} failed`);
  }
  return text ? JSON.parse(text) : null;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders() });

  if (req.method === "GET") {
    return json({
      service: "Humanity Loop Contributor Node Gateway",
      version: "0.3.1-stage0",
      automatic_after_opt_in: true,
      note: "Installing Humanity Loop does not self-start an LLM. A person authorizes one recurring task in their host; after that, the node can check in automatically.",
      actions: ["register", "checkin", "submit", "pause", "resume", "revoke"],
      telemetry: "Privacy-safe onboarding funnel telemetry records deduplicated join sessions and bounded node lifecycle events. Raw IP addresses, full user-agent strings, emails, and node tokens are not stored in funnel events.",
      permissions: "Stage-0 registration is Tier-0 only: manual reversible public-source work, no recurring scheduling or external action. Tier-1 and Tier-2 onboarding are on hold pending later authorization. Contributor submissions remain quarantined for review.",
    });
  }

  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const len = Number(req.headers.get("content-length") || "0");
  if (len > 65536) return json({ error: "payload_too_large" }, 413);

  let body: any;
  try {
    body = await req.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }

  const action = cleanString(body?.action, 40);
  if (!action) return json({ error: "missing_action" }, 400);

  try {
    if (action === "visit") {
      const sessionId = cleanString(body.session_id, 200);
      if (!sessionId || sessionId.length < 16) {
        return json({ error: "invalid_session" }, 400);
      }
      const sessionHash = await hmac("join-session:" + sessionId);
      const tracked = await rpc("hl_node_track_join_visit", {
        p_session_hash: sessionHash,
        p_source: cleanString(body.source, 80),
        p_client_surface: clientSurface(req),
      });
      return json({ tracked: tracked === true });
    }

    if (action === "register") {
      const fp = await fingerprint(req);
      const allowed = await rpc("hl_node_registration_gate", {
        p_fingerprint: fp,
        p_window_minutes: 60,
        p_max_attempts: 5,
      });
      if (allowed !== true) return json({ error: "registration_rate_limited" }, 429);

      const email = cleanString(body.email, 254);
      const consent = body.setup_email_consent === true;
      if (email && !consent) {
        return json({ error: "setup_email_requires_explicit_consent" }, 400);
      }
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return json({ error: "invalid_email" }, 400);
      }

      const selectedPermissions = clampArray(body.risk_permissions, 8);
      if (selectedPermissions.some((permission) => permission !== "tier0")) {
        return json({ error: "stage0_tier0_only" }, 403);
      }
      const token = randomToken();
      const tokenHash = await sha256(token);
      const registered = await rpc("hl_node_register", {
        p_token_hash: tokenHash,
        p_capabilities: clampArray(body.capabilities),
        p_languages: clampArray(body.languages, 12),
        p_host: cleanString(body.host, 80),
        p_user_agent_label: cleanString(body.user_agent_label, 120),
        p_email: email,
        p_setup_email_consent: consent,
        p_risk_permissions: ["tier0"],
      });

      const sessionId = cleanString(body.session_id, 200);
      if (sessionId && sessionId.length >= 16 && registered?.node_id) {
        const sessionHash = await hmac("join-session:" + sessionId);
        await rpc("hl_node_attach_registration_session", {
          p_node_id: registered.node_id,
          p_session_hash: sessionHash,
          p_source: cleanString(body.source, 80),
          p_client_surface: clientSurface(req),
        });
      }

      return json({
        ...registered,
        node_token: token,
        token_note: "Shown once. Keep private. Stage-0: one manual Tier-0 assignment only; no automatic scheduling.",
        recurring_prompt: "STAGE-0 IS MANUAL ONLY. Do not schedule this node. With explicit owner consent, check in once, complete one reversible public-source Tier-0 assignment, and submit evidence for quarantine review. Pause or revoke anytime.",
      }, 201);
    }

    const token = cleanString(req.headers.get("x-node-token") || body.node_token, 200);
    if (!token?.startsWith("hl_node_")) return json({ error: "missing_or_invalid_node_token" }, 401);
    const tokenHash = await sha256(token);

    if (action === "checkin") {
      const result = await rpc("hl_node_checkin", {
        p_token_hash: tokenHash,
        p_capabilities: Array.isArray(body.capabilities) ? clampArray(body.capabilities) : null,
        p_languages: Array.isArray(body.languages) ? clampArray(body.languages, 12) : null,
        p_host: cleanString(body.host, 80),
        p_user_agent_label: cleanString(body.user_agent_label, 120),
      });
      return json(result);
    }

    if (action === "submit") {
      const workId = cleanString(body.work_id, 80);
      if (!workId) return json({ error: "missing_work_id" }, 400);
      const resultObj = body.result && typeof body.result === "object" ? body.result : {};
      const evidence = Array.isArray(body.evidence) ? body.evidence.slice(0, 20) : [];
      const failureModes = Array.isArray(body.failure_modes) ? body.failure_modes.slice(0, 20) : [];
      const result = await rpc("hl_node_submit", {
        p_token_hash: tokenHash,
        p_work_id: workId,
        p_result: resultObj,
        p_evidence: evidence,
        p_uncertainty: cleanString(body.uncertainty, 2000),
        p_failure_modes: failureModes,
      });
      return json(result, 202);
    }

    if (["pause", "resume", "revoke"].includes(action)) {
      const status = action === "pause" ? "paused" : action === "resume" ? "active" : "revoked";
      const result = await rpc("hl_node_set_status", {
        p_token_hash: tokenHash,
        p_status: status,
      });
      return json(result);
    }

    return json({ error: "unknown_action" }, 400);
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("node-gateway error", { action, message: message.slice(0, 500) });
    return json({ error: "request_failed", detail: message.slice(0, 300) }, 400);
  }
});
