export default function Home() {
  return (
    <main style={{maxWidth: 860, margin: "64px auto", padding: 24, fontFamily: "system-ui"}}>
      <h1>Humanity Loop MCP</h1>
      <p>Vendor-neutral, read-only gateway to Humanity Loop's public protocol, action ledger, project cards, replication prompt, and dead-end ledger.</p>
      <p><strong>MCP endpoint:</strong> <code>/api/mcp</code></p>
      <p><strong>JSON fallback:</strong> <code>/api/v1?tool=get_protocol</code></p>
      <p>Source of truth: <a href="https://github.com/Lesterhau/humanity-loop">github.com/Lesterhau/humanity-loop</a></p>
    </main>
  );
}
