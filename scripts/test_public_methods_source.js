'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const {EventEmitter}=require('node:events');
const {PassThrough}=require('node:stream');
const m=require('./public_methods_source');

const content='# Reversible Agent Work\n\nPublic synthetic example.\n';
const hash=crypto.createHash('sha1')
 .update(Buffer.from('blob '+Buffer.byteLength(content,'utf8')+'\0'))
 .update(Buffer.from(content)).digest('hex');

function mockGet(body,status=200){
 return (url,opts,handler)=>{
  assert.equal(url.hostname,'raw.githubusercontent.com');
  assert.equal(url.pathname,'/'+m.RELEASE.repository+'/'+m.RELEASE.commit+'/'+m.RELEASE.path);
  const req=new EventEmitter();
  req.setTimeout=()=>{};
  req.destroy=e=>req.emit('error',e);
  process.nextTick(()=>{
   const resp=new PassThrough(); resp.statusCode=status;
   handler(resp);resp.end(Buffer.from(body));
  });
  return req;
 };
}

test('approved public release is commit-pinned to a known Git blob',()=>{
 assert.equal(m.RELEASE.repository,'Lesterhau/morrow-methods');
 assert.match(m.RELEASE.commit,/^[0-9a-f]{40}$/);
 assert.match(m.RELEASE.blobSha,/^[0-9a-f]{40}$/);
 assert.match(m.SOURCE,/^https:\/\/raw\.githubusercontent\.com\//);
 assert.ok(!m.SOURCE.includes('morrow-engine'));
});

test('verified synthetic Git blob integrity and provenance are reported',()=>{
 const r=m.verifyText(content,hash);
 assert.equal(r.verifiedBlobSha,hash);
 assert.equal(r.status,'verified');
 assert.equal(r.means.includes('not authorization'),true);
 assert.equal(r.bytes,Buffer.byteLength(content));
});

test('tampered, oversized and invalid UTF8 source fail closed',()=>{
 assert.throws(()=>m.verifyText(content+' changed',hash),/mismatch/);
 assert.throws(()=>m.verifyText('# Wrong title',crypto.createHash('sha1')
  .update('blob 13\0# Wrong title').digest('hex')),/Unexpected/);
 assert.throws(()=>m.verifyText('x'.repeat(m.MAX_BYTES+1)),/size/);
 assert.throws(()=>m.verifyText(null),/UTF-8/);
});

test('mock transport fetches from approved PUBLIC location only',async()=>{
 assert.equal(await m.readText(mockGet(content)),content);
});

test('public non-200 responses do not create a verified source',async()=>{
 await assert.rejects(m.verifyPublishedMethods(mockGet('not found',404)),/HTTP status/);
});

test('changed external file cannot be treated as approved',async()=>{
 await assert.rejects(m.verifyPublishedMethods(mockGet(content)),/mismatch/);
});
