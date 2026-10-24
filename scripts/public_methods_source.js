'use strict';
// Verify an owner-approved PUBLIC release. No auth, private repositories or writes.
const https=require('node:https');
const crypto=require('node:crypto');

const RELEASE=Object.freeze({
 repository:'Lesterhau/morrow-methods',
 commit:'f6fd07bac3eb42c5068d6d9c8e9dcc1e8e623109',
 path:'METHODS.md',
 blobSha:'b5378330d38a1e2d622d2270b8a457ad2924897c'
});
const SOURCE='https://raw.githubusercontent.com/'+RELEASE.repository+'/'+RELEASE.commit+'/'+RELEASE.path;
const MAX_BYTES=32768;

function verifyText(text,expectedSha=RELEASE.blobSha) {
 if(typeof text!=='string')throw new TypeError('UTF-8 methods text required');
 const raw=Buffer.from(text,'utf8');
 if(raw.length===0||raw.length>MAX_BYTES)throw new Error('Published methods content outside bounded size');
 const blob=crypto.createHash('sha1').update(Buffer.from('blob '+raw.length+'\0')).update(raw).digest('hex');
 if(blob!==expectedSha)throw new Error('Published methods Git blob SHA mismatch');
 if(!text.startsWith('# Reversible Agent Work'))throw new Error('Unexpected approved methods document');
 return {status:'verified',source:SOURCE,repository:RELEASE.repository,commit:RELEASE.commit,
         path:RELEASE.path,verifiedBlobSha:blob,bytes:raw.length,
         means:'Public document integrity only, not authorization, code execution or outcome'};
}

function readText(request=https.get) {
 return new Promise((resolve,reject)=>{
   const url=new URL(SOURCE);
   if(url.protocol!=='https:'||url.hostname!=='raw.githubusercontent.com')
     return reject(new Error('Nonallowlisted origin'));
   const req=request(url,{headers:{'User-Agent':'HumanityLoop-Methods-Audit/0.1'}},response=>{
     if(response.statusCode!==200){response.resume?.();return reject(new Error('Public source HTTP status '+response.statusCode));}
     const chunks=[];let bytes=0;let closed=false;
     response.on('data',chunk=>{
       bytes+=chunk.length;
       if(bytes>MAX_BYTES){closed=true;req.destroy(new Error('Methods source exceeds 32KiB'));return;}
       chunks.push(chunk);
     });
     response.on('end',()=>{
       if(!closed)resolve(Buffer.concat(chunks).toString('utf8'));
     });
     response.on('error',reject);
   });
   req.on('error',reject);
   req.setTimeout?.(8000,()=>req.destroy(new Error('Methods fetch timed out')));
 });
}
async function verifyPublishedMethods(request) {
 const text=await readText(request);
 return verifyText(text);
}
module.exports={RELEASE,SOURCE,MAX_BYTES,verifyText,readText,verifyPublishedMethods};
