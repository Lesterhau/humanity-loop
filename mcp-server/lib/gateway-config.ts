// Fail closed in unspecified builds, previews, and test environments.
// The public URL is not a credential. Never place secrets in NEXT_PUBLIC_*.
const PRODUCTION_GATEWAY = "https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node";
const PRODUCTION_ORIGIN = "https://humanity-loop.vercel.app";

export function resolveGateway(mode: string | undefined, target: string | undefined, productionAllowed: boolean): string | null {
  if (!target) return null;
  if (mode === "production") return productionAllowed && target === PRODUCTION_GATEWAY ? target : null;
  // Only an explicit IPv4 loopback endpoint, no redirects, auth, query or path ambiguity.
  if (mode !== "fixture" || !/^http:\/\/127\.0\.0\.1:[1-9][0-9]{0,4}\/functions\/v1\/contributor-node$/.test(target)) return null;
  try { const u = new URL(target); return u.port && Number(u.port) <= 65535 ? target : null; }
  catch { return null; }
}

export function gatewayUrl(): string | null {
  const productionAllowed = typeof window === "undefined"
    ? process.env.VERCEL_ENV === "production"
    : window.location.origin === PRODUCTION_ORIGIN;
  return resolveGateway(process.env.NEXT_PUBLIC_HL_GATEWAY_MODE,
    process.env.NEXT_PUBLIC_HL_GATEWAY_URL, productionAllowed);
}
