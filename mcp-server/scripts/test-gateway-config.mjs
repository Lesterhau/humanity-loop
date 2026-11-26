import assert from 'node:assert/strict';
import { resolveGateway } from '../lib/gateway-config.ts';
const live='https://jxtcccrlnhkcjfnwlfea.supabase.co/functions/v1/contributor-node';
const local='http://127.0.0.1:54321/functions/v1/contributor-node';
assert.equal(resolveGateway(undefined, undefined, false), null);
assert.equal(resolveGateway('fixture', live, true), null);
assert.equal(resolveGateway('production', live, false), null);
assert.equal(resolveGateway('production', live, true), live);
assert.equal(resolveGateway('production', local, true), null);
assert.equal(resolveGateway('fixture', local, false), local);
for (const target of [
 'http://localhost:54321/functions/v1/contributor-node',
 'http://127.0.0.1:65536/functions/v1/contributor-node',
 local+'?redirect=live',
 local+'#fragment',
 'http://127.0.0.1:54321@evil.example/functions/v1/contributor-node',
 'https://127.0.0.1:54321/functions/v1/contributor-node',
 'http://127.0.0.1:80/functions/v1/contributor-node',
]) assert.equal(resolveGateway('fixture', target, false), null);
console.log('GATEWAY_CONFIG_ISOLATION_PASSED (no HTTP requests)');
