import os, sys, subprocess
T = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\wave2\tee_elbow\test'
C = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\puckfix_20261009\tools_new\checks\allcfg_check.py'
roots = '1501 2501 2505 2602 2606 2609 2611 5502 5504 5604'.split()
for s, r in (('test', 'root'), ('untouched', 'root_untouched')):
    g = os.path.join(T, f'gen_{s}', 'tee')
    env = dict(os.environ, OMI_ROOT=os.path.join(T, r), GT_OUT=g, GS_OUT=os.path.join(T, f'gen_{s}', 'straight'))
    p = subprocess.run([sys.executable, '-I', '-B', C, 't'] + roots, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    open(os.path.join(T, 'checks', f'allcfg_{s}.txt'), 'w', encoding='utf-8').write(p.stdout + p.stderr)
    print(s, p.returncode); print(p.stdout[-3000:], p.stderr[-2000:])
