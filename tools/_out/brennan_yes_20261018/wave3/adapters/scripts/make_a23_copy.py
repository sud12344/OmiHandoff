"""make a patched COPY of tools/_out/a19_omi_diffs_20261018/a19_diff.py that reads the wave3 adapters test tables (applied) and writes into
wave3/adapters/a23_check (the original folder is not touched)."""
src = open(r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\a19_omi_diffs_20261018\a19_diff.py', encoding='utf-8').read()
a = r'OUT = os.path.join(R, r"tools\_out\a19_omi_diffs_20261018")'
b = r'STAGE = os.path.join(R, r"tools\_out\brennan_yes_20261018\stage\04_DESIGN_TABLES")'
assert a in src and b in src
src = src.replace(a, r'OUT = os.path.join(R, r"tools\_out\brennan_yes_20261018\wave3\adapters\a23_check")')
src = src.replace(b, r'STAGE = os.path.join(R, r"tools\_out\brennan_yes_20261018\wave3\adapters\test\root_applied\04_DESIGN_TABLES")')
src = '# COPY of tools/_out/a19_omi_diffs_20261018/a19_diff.py with OUT / STAGE pointed at the wave3 adapters test (applied tables)\n' + src
open(r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\wave3\adapters\scripts\a23_check_copy_of_a19_diff.py', 'w', encoding='utf-8').write(src)
