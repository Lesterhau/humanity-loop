"""Real SIGKILL of an owned synthetic subprocess on a disposable local filesystem.
No network, live model, real recipient, host shutdown, power-loss or deployment.
"""
import json
import os
import select
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime,timedelta,timezone
from pathlib import Path

import review_journal as j
from review_envelope import digest,run
from review_retention import RetentionHold
from test_review_packet import packet


def at(fn,*args,now,**kwargs):
    # Test-only clock substitution; no public time argument.
    with patch('review_journal._wall_clock',return_value=now):
        return fn(*args,**kwargs)

CHILD = r"""
import json,signal,sys
from datetime import datetime,timedelta
from pathlib import Path
import review_journal as j
import review_retention as r
from review_envelope import digest,run
from test_review_packet import packet
root,bid,certpath,when,mode=sys.argv[1:]
now=datetime.fromisoformat(when)
j._wall_clock=lambda: now if mode.endswith('store') else now+timedelta(hours=1)
def stop():
    print('CHECKPOINT',flush=True)
    while True: signal.pause()
if mode in ('before_store','after_store'):
    original=j.store
    def intercepted(*a,**kw):
        if mode=='after_store': original(*a,**kw)
        stop()
    j.store=intercepted
elif mode=='partial_store':
    original=r.write_file
    def intercepted(fd,name,data):
        original(fd,name,data)
        if name=='review.cms': stop()
    r.write_file=intercepted
elif mode in ('before_delete','after_delete'):
    original=j.remove
    def intercepted(*a,**kw):
        if mode=='after_delete': original(*a,**kw)
        stop()
    j.remove=intercepted
else: raise SystemExit('unknown synthetic checkpoint')
if mode.endswith('store'):
    cert=Path(certpath).read_bytes()
    data=json.dumps(packet()).encode()
    j.retain(root,bid,data,cert,digest(run(['x509','-outform','DER'],cert)),digest(data),
        ttl_hours=1,storage_authorized=True)
else:
    j.cleanup(root,[bid],deletion_authorized=True)
raise SystemExit('checkpoint was not reached')
"""

@unittest.skipUnless(sys.platform.startswith('linux'),'Linux process-termination rehearsal only')
class JournalProcessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys=tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.keys.cleanup)
        cls.key=Path(cls.keys.name)/'key.pem'
        cls.certpath=Path(cls.keys.name)/'cert.pem'
        run(['req','-x509','-newkey','rsa:3072','-nodes','-keyout',str(cls.key),'-out',str(cls.certpath),'-days','1','-subj','/CN=synthetic-process-test'])
        cls.key.chmod(0o600)
        cls.cert=cls.certpath.read_bytes()
        cls.cpin=digest(run(['x509','-outform','DER'],cls.cert))
        cls.data=json.dumps(packet()).encode()
        cls.ppin=digest(cls.data)

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.bid='review-process-01'
        self.now=datetime(2026,11,24,23,0,tzinfo=timezone.utc)
        self.expiry=self.now+timedelta(hours=1)
        (self.root/'sentinel').write_text('unrelated')

    def retain(self):
        return at(j.retain,self.root,self.bid,self.data,self.cert,self.cpin,self.ppin,
            now=self.now,ttl_hours=1,storage_authorized=True)

    def kill_at(self,mode):
        # Only the child created here is ever signaled; no PID discovery or external process.
        proc=subprocess.Popen([sys.executable,'-c',CHILD,str(self.root),self.bid,
            str(self.certpath),self.now.isoformat(),mode],
            cwd=str(Path(__file__).resolve().parent),
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            env={'PATH':'/usr/bin:/bin','LANG':'C','PYTHONDONTWRITEBYTECODE':'1'})
        try:
            self.assertTrue(select.select([proc.stdout],[],[],20)[0],'checkpoint timeout')
            self.assertEqual(proc.stdout.readline(),b'CHECKPOINT\n','child failed before checkpoint')
            # The real operating-system lock must exclude a separate process.
            with self.assertRaisesRegex(RetentionHold,'journal_busy'):
                j.state(self.root,self.bid)
            proc.kill()
            self.assertEqual(proc.wait(timeout=5),-signal.SIGKILL)
        finally:
            if proc.poll() is None:
                proc.kill();proc.wait(timeout=5)
            proc.stdout.close();proc.stderr.close()
        self.assertEqual((self.root/'sentinel').read_text(),'unrelated')

    def test_sigkill_before_store(self):
        self.kill_at('before_store')
        self.assertEqual(j.state(self.root,self.bid)['state'],'storing')
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.now),'hold')
        self.assertFalse((self.root/self.bid).exists())

    def test_sigkill_after_ciphertext_before_manifest(self):
        self.kill_at('partial_store')
        self.assertTrue((self.root/self.bid/'review.cms').is_file())
        self.assertFalse((self.root/self.bid/'manifest.json').exists())
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.now),'hold')
        self.assertEqual(at(j.cleanup,self.root,[self.bid],now=self.expiry,deletion_authorized=True)['results'][0]['status'],'hold')
        self.assertTrue((self.root/self.bid/'review.cms').exists())

    def test_sigkill_after_complete_storage(self):
        self.kill_at('after_store')
        s=j.state(self.root,self.bid)
        self.assertEqual(s['state'],'storing')
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.now),'retained')
        m=s['manifest']
        clear,summary=at(j.recover,self.root,self.bid,self.cert,self.cpin,self.key,self.ppin,m['envelope_sha256'],now=self.now)
        self.assertEqual(clear,self.data)
        self.assertFalse(summary['independent_review_completed'])

    def test_sigkill_before_deletion(self):
        self.retain()
        self.kill_at('before_delete')
        self.assertEqual(j.state(self.root,self.bid)['state'],'deleting')
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.expiry),'hold')
        self.assertTrue((self.root/self.bid/'review.cms').exists())

    def test_sigkill_after_deletion(self):
        self.retain()
        self.kill_at('after_delete')
        self.assertFalse((self.root/self.bid).exists())
        self.assertEqual(j.state(self.root,self.bid)['state'],'deleting')
        self.assertEqual(at(j.reconcile,self.root,self.bid,now=self.expiry),'hold')
        self.assertNotIn('deleted',[t['state'] for t in j.state(self.root,self.bid)['transitions']])
