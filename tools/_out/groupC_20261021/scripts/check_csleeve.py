"""check_csleeve.py (group C): checks of the CSLEEVE (C0319) master
1. rigidity: the DRIVE sketch as the macro builds it (14 lines with merged ends, the H/V relations CSLEEVE_HV, the construction line origin ->
   P1 vertical, the 19 linear dimensions CSLEEVE_DIMS) - numeric Jacobian rank = unknowns, no redundant constraint; every dimension name
   appears exactly once as NameDim in the emitted macro;
2. every configuration: outline simple, angles as on the STEPs (csleeve_why);
3. closed loop: each configuration's half-section revolved (OCP), written as STEP, read back with the SAME extractor that measured the
   Brennan STEPs (measure_c0319.outline) -> must return its own row AND the Brennan STEP of that size, every point within 0.0005.
   python check_csleeve.py <macro.bas> <SW2.xlsx>"""
import os, sys, math, re
import numpy as np, openpyxl
H = os.path.dirname(os.path.abspath(__file__)); STAGE = os.path.dirname(H)
sys.path.insert(0, os.path.join(STAGE, 'tools_c', 'generators')); sys.path.insert(0, os.path.join(STAGE, 'tools_c', 'measure')); sys.path.insert(0, H)
import gen_ring as GR
from model_nutcap import revolve, write, nsolids
import measure_c0319 as MC

bas, sw2 = sys.argv[1], sys.argv[2]
out = []
# 1. rigidity on the reference row
rows = list(openpyxl.load_workbook(sw2, read_only=True).active.iter_rows(values_only=True)); h = rows[0]
cfg = [dict(zip(h[1:], r[1:])) for r in rows[1:]]
V = GR.csleeve_points(cfg[0]); n = 14
X = lambda q, i: q[2 * i]; Y = lambda q, i: q[2 * i + 1]
cons = []
for i, t in GR.CSLEEVE_HV.items():
    j = (i + 1) % n
    cons.append((lambda q, i=i, j=j: Y(q, i) - Y(q, j)) if t == 'H' else (lambda q, i=i, j=j: X(q, i) - X(q, j)))
for kind, nm, i in GR.CSLEEVE_DIMS:
    if kind == 'cl': cons += [lambda q: X(q, 1), lambda q: Y(q, 1)]          # origin -> P1 vertical: x = 0, length = r1
    elif kind in ('lineo', 'pto'): cons.append(lambda q, i=i: Y(q, i))
    elif kind in ('ptx', 'linex'): cons.append(lambda q, i=i: X(q, i) - X(q, 0))
q0 = np.array([c for p in V for c in p]); eps = 1e-7
J = np.array([[(f(q0 + eps * np.eye(2 * n)[k]) - f(q0 - eps * np.eye(2 * n)[k])) / (2 * eps) for k in range(2 * n)] for f in cons])
rank = np.linalg.matrix_rank(J, tol=1e-6)
out.append(f'rigidity: unknowns {2 * n}, constraints {len(cons)}, rank {rank} -> ' + ('FULLY DEFINED, 0 redundant' if rank == 2 * n == len(cons) else 'NOT OK'))
txt = open(bas).read()
miss = [nm for _, nm, _ in GR.CSLEEVE_DIMS if len(re.findall(rf'NameDim dd, "{nm}",', txt)) != 1]
out.append(f'macro: {len(GR.CSLEEVE_DIMS)} DRIVE dimensions, each named once: ' + ('OK' if not miss else f'MISSING / DOUBLE {miss}'))
# 2 + 3
tmp = os.path.join(STAGE, 'scratch'); os.makedirs(tmp, exist_ok=True); bad = 0
for c in cfg:
    pn = c['$PRP@PartNo']; V = GR.csleeve_points(c); why = GR.csleeve_why(c)
    S = revolve(V); f = os.path.join(tmp, f'{pn}_model.stp'); write(S, f)
    got = MC.outline(f); ref = MC.outline(os.path.join(MC.ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp'))
    d_row = max(math.dist(a, b) for a, b in zip(got, V)); d_step = max(math.dist(a, b) for a, b in zip(got, ref))
    ok = not why and nsolids(S) == 1 and d_row < 5e-4 and d_step < 5e-4
    bad += not ok
    out.append(f'{pn:10} solids {nsolids(S)}  model vs row {d_row:.6f}  model vs Brennan STEP {d_step:.6f}  ' + ('OK' if ok else 'BAD ' + '; '.join(why)))
out.insert(0, f'check_csleeve: {len(cfg)} configurations, {bad} bad (closed loop: every one of the 14 points within 0.0005 of the row and of the Brennan STEP)')
print('\n'.join(out)); open(os.path.join(STAGE, 'checks', 'csleeve_check.txt'), 'w').write('\n'.join(out) + '\n')
