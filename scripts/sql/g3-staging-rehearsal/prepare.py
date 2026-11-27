"""Generate reviewed, pinned synthetic rehearsal copies. Never run against hosted DB."""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

PIN = '3eb9b7f16ab3294854780acdcfdc58959032c8d1'
SCHEMA = 'hl_g3_rehearsal'
# Exercise candidate SQL from the exact checked-out commit, not the superseded baseline.
CANDIDATES = {
    'supabase/sql/hl_control_fenced_tasks_candidate_v1.sql',
    'supabase/sql/hl_fenced_executor_restricted_candidate_v1.sql',
}
SOURCES = {
    'scripts/sql/fenced_task_test_fixture.sql': 'e58132df8c7e31fc43654d41ce251fef34a98bed',
    # Candidates are read from the checked-out commit (see CANDIDATES); no blob pin applies.
    'supabase/sql/hl_control_fenced_tasks_candidate_v1.sql': None,
    'supabase/sql/hl_fenced_executor_restricted_candidate_v1.sql': None,
    'scripts/sql/test_fenced_canonical_lease.sql': '447f13adde8d9a57fcb8635b3ed11d856b6b47d3',
    'scripts/sql/test_restricted_fenced_executor.sql': '0998f331a60d9e6fa48da925711575080396c400',
    'scripts/sql/test_fenced_authenticated_login.sh': '87e9936d97c376b5d318d051d824e709da3beaaa',
    'scripts/sql/test_fenced_concurrent_claim.sh': '7f4064805a5b74922b71177a914e866419a4f948',
}

def transform(path, source):
    s = re.sub(r'\bhl_control\b', SCHEMA, source)
    s = re.sub(r'\bpublic\.(assert_true|assert_rejected)\b', rf'{SCHEMA}.\1', s)
    s = re.sub(r'\bhl_test_executor_(a|b|unbound)\b', r'hl_g3_rehearsal_\1', s)
    s = re.sub(r'\bhl_fenced_definer\b', 'hl_g3_rehearsal_definer', s)
    if path.endswith('fenced_task_test_fixture.sql'):
        s, n = re.subn(r'^CREATE ROLE (anon|authenticated|service_role) NOLOGIN;[ \t]*$', '', s, flags=re.M)
        if n != 3:
            raise ValueError('Unexpected fixture role declarations')
    if re.search(r'\bhl_control\b|\bpublic\.|\bhl_test_executor_(?:a|b|unbound)\b|\bhl_fenced_definer\b', s):
        raise ValueError(f'Unexpected original schema/role or public reference: {path}')
    if re.search(r'^\s*CREATE ROLE (anon|authenticated|service_role)\b', s, flags=re.M|re.I):
        raise ValueError('Existing API role creation detected')
    return s

def main():
    root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if out.exists() or out == root or root in out.parents:
        raise ValueError('Output must be new and outside repository')
    results = {}
    for path, expected in SOURCES.items():
        candidate = path in CANDIDATES
        commit = 'HEAD' if candidate else PIN
        data = subprocess.check_output(['git', '-C', str(root), 'show', f'{commit}:{path}'])
        actual = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        if candidate:
            if (root / path).read_bytes() != data:
                raise ValueError(f'Candidate working tree mismatch: {path}')
        elif actual != expected:
            raise ValueError(f'Pinned fixture blob mismatch: {path}')
        results[Path(path).name] = transform(path, data.decode('utf-8'))
    out.mkdir(mode=0o700)
    for name, content in results.items():
        (out / name).write_text(content, encoding='utf-8')
    print(f'Prepared {len(results)} pinned synthetic rehearsal files')

if __name__ == '__main__':
    main()
