"""Batch 17 paperwork (2026-10-20): copy every paperwork file BEFORE it is edited to old_files/paperwork/ and
_to_delete/superseded_20261021/batch19_replaced/paperwork/ (MANIFEST_paperwork.txt in both)."""
import glob, hashlib, os, shutil

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
files = ['01_MASTER_DATA/OMi_Fitting_Library_MasterData_v1.xlsx', '00_DOCS/OMi_Coverage_2026-09-24.xlsx', '00_DOCS/PROJECT_STATUS.md',
         'CLAUDE.md', '00_DOCS/NEXT_SESSION_PROMPT_2026-10-20.md']
files += [os.path.relpath(p, R).replace(os.sep, '/') for p in glob.glob(os.path.join(R, 'tools', 'coverage', 'work', '*')) if os.path.isfile(p)]
man = []
for f in files:
    h = hashlib.sha256(open(os.path.join(R, f), 'rb').read()).hexdigest()
    for base in ('tools/_out/batch19_20261021/merge/old_files/paperwork', '_to_delete/superseded_20261021/batch19_replaced/paperwork'):
        d = os.path.join(R, base, f)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(R, f), d)
        assert hashlib.sha256(open(d, 'rb').read()).hexdigest() == h
    man.append(f'{h}  {f}')
for base in ('tools/_out/batch19_20261021/merge/old_files', '_to_delete/superseded_20261021/batch19_replaced'):
    open(os.path.join(R, base, 'MANIFEST_paperwork.txt'), 'w', encoding='utf-8').write(
        'Batch 19 (2026-10-21): paperwork files BEFORE the batch-19 paperwork (copies under paperwork/; sha256  path)\n' + '\n'.join(man) + '\n')
print('\n'.join(man))
