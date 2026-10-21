#!/usr/bin/env python3
"""dofcheck_bent.py (2026-10-21, group D): rigidity check of the gen_bent.py sketches, straight from the emitted .bas (reference
configuration): numerical constraint Jacobian, fully defined <=> rank == unknowns and no redundant constraint.
  DRIVE   the JIC end piece chain - dofcheck_straight.check with the bent macro's DRIVE block marker
  PATH / PATHX   construction line + line + arc + line (+ the hub-head face extension pe): 18 (22) unknowns
  HEADSK  the flange head half-section (8 lines, or 10 with the braze hub) + centre line, anchored on the PATH end / face extension
The swivel sketch SWSK (6701) is not covered (unchanged code; checked fully defined in the 2026-10-15 SolidWorks dry run).
    python dofcheck_bent.py <Build_*.bas> ...
"""
import math, os, re, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dofcheck_straight as ds

IN = 0.0254


def parse_drive(path):
    t = open(path).read()
    arr = re.search(r'v = Array\((.*?)\)\n', t, re.S).group(1)
    nums = [float(x) for x in re.findall(r'-?\d+\.\d+', arr)]
    P = np.array([(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)])
    blk = t.split('================= 1. DRIVE: JIC end piece')[1].split('swFeat.Name = "DRIVE"')[0]
    dims = re.findall(r'Call (Dim_\w+|Collinear)\(([^)]*)\)', blk)
    return P, dims


def nums(s):
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:[eE]-?\d+)?', s)]


def rank_report(cons, q0, extra=None):
    J = np.zeros((len(cons), len(q0)))
    h = 1e-8
    for c, (nm, f) in enumerate(cons):
        for k in range(len(q0)):
            qp = q0.copy(); qm = q0.copy(); qp[k] += h; qm[k] -= h
            J[c, k] = (f(qp) - f(qm)) / (2 * h)
    resid = max(abs(f(q0)) for _, f in cons) if cons else 0.0
    rank = int(np.linalg.matrix_rank(J, tol=1e-7))
    r = dict(unknowns=len(q0), constraints=len(cons), rank=rank, fully=rank == len(q0), redundant=len(cons) - rank,
             max_residual=float(f'{resid:.2e}'))
    r.update(extra or {})
    return r


def path_block(t, name):
    b = t.split(f'================= {name}: tube centre line')[1].split(f'swFeat.Name = "{name}"')[0]
    L = {}
    for var in ('pc', 'p1', 'p2', 'pe'):
        m = re.search(rf'Set {var} = swSkMgr\.CreateLine\(([^)]*)\)', b)
        if m:
            v = nums(m.group(1)); L[var] = [(v[0], v[1]), (v[3], v[4])]
    m = re.search(r'Set pa = swSkMgr\.CreateArc\(([^)]*)\)', b)
    v = nums(m.group(1)); L['pa'] = [(v[0], v[1]), (v[3], v[4]), (v[6], v[7])]       # centre, start, end
    pd = re.search(r'PathDims pc, p1, pa, p2, ([^\n]*)', b).group(1)
    vals = [x.strip() for x in pd.split(',')]
    dims = dict(S=float(vals[1]), T=float(vals[3]), R=float(vals[5]), X=float(vals[7]), Y=float(vals[9]))
    ext = re.search(r'PathExtension p2, pe, "(\w+)", ([-\d.]+)', b)
    return L, dims, (float(ext.group(2)) if ext else None), b


def check_path(t, name):
    L, d, ext, _ = path_block(t, name)
    order = [('pc', 2), ('p1', 2), ('pa', 3), ('p2', 2)] + ([('pe', 2)] if 'pe' in L else [])
    idx, q0 = {}, []
    for var, k in order:
        for j in range(k):
            idx[(var, j)] = len(q0) // 2
            q0 += list(L[var][j])
    q0 = np.array(q0, float)
    Pt = lambda q, var, j: (q[2 * idx[(var, j)]], q[2 * idx[(var, j)] + 1])
    cons = []
    def same(a, b):
        cons.append((f'{a}={b} x', lambda q: Pt(q, *a)[0] - Pt(q, *b)[0])); cons.append((f'{a}={b} y', lambda q: Pt(q, *a)[1] - Pt(q, *b)[1]))
    cons.append(('pc start = origin x', lambda q: Pt(q, 'pc', 0)[0])); cons.append(('pc start = origin y', lambda q: Pt(q, 'pc', 0)[1]))
    cons.append(('pc horizontal', lambda q: Pt(q, 'pc', 1)[1] - Pt(q, 'pc', 0)[1]))
    same(('pc', 1), ('p1', 0)); same(('p1', 1), ('pa', 1)); same(('pa', 2), ('p2', 0))
    cons.append(('p1 horizontal', lambda q: Pt(q, 'p1', 1)[1] - Pt(q, 'p1', 0)[1]))
    cons.append(('arc start / end radius equal', lambda q: math.dist(Pt(q, 'pa', 1), Pt(q, 'pa', 0)) - math.dist(Pt(q, 'pa', 2), Pt(q, 'pa', 0))))
    def tang(line, at):
        def f(q):
            a, b = Pt(q, line, 0), Pt(q, line, 1); c = Pt(q, 'pa', 0); p = Pt(q, 'pa', at)
            dx, dy = b[0] - a[0], b[1] - a[1]
            return (dx * (p[0] - c[0]) + dy * (p[1] - c[1])) / math.hypot(dx, dy)
        return f
    cons.append(('p1 tangent arc', tang('p1', 1))); cons.append(('arc tangent p2', tang('p2', 2)))
    cons.append(('dim start (pc length)', lambda q: math.dist(Pt(q, 'pc', 0), Pt(q, 'pc', 1)) - d['S']))
    cons.append(('dim T1X', lambda q: Pt(q, 'p1', 1)[0] - d['T']))
    cons.append(('dim RB', lambda q: math.dist(Pt(q, 'pa', 1), Pt(q, 'pa', 0)) - d['R']))
    cons.append(('dim FX', lambda q: Pt(q, 'p2', 1)[0] - d['X']))
    cons.append(('dim FY', lambda q: Pt(q, 'p2', 1)[1] - d['Y']))
    if 'pe' in L:
        same(('p2', 1), ('pe', 0))
        def par(q):
            a, b, c, e = Pt(q, 'p2', 0), Pt(q, 'p2', 1), Pt(q, 'pe', 0), Pt(q, 'pe', 1)
            u = (b[0] - a[0], b[1] - a[1]); v = (e[0] - c[0], e[1] - c[1])
            return (u[0] * v[1] - u[1] * v[0]) / (math.hypot(*u) * math.hypot(*v))
        cons.append(('pe parallel p2', par))
        cons.append(('dim FACEEXT', lambda q: math.dist(Pt(q, 'pe', 0), Pt(q, 'pe', 1)) - ext))
    return rank_report(cons, q0, dict(sketch=name, face_extension=('pe' in L)))


def check_head(t):
    if 'HEADSK: flange head half-section' not in t:
        return None
    b = t.split('================= HEADSK: flange head half-section')[1].split('swFeat.Name = "HEADSK"')[0]
    segs = {}
    for m in re.finditer(r'Set hs\((\d+)\) = swSkMgr\.CreateLine\(([^)]*)\)', b):
        v = nums(m.group(2)); segs[int(m.group(1))] = [(v[0], v[1]), (v[3], v[4])]
    N = len(segs); ax = N - 1
    m = re.search(r'Set hcl = swSkMgr\.CreateCenterLine\(([^)]*)\)', b); v = nums(m.group(1)); hcl = [(v[0], v[1]), (v[3], v[4])]
    # the anchor: PATH's end (p2) or its face extension (pe) end point, and p2's direction - fixed (PATH is fully defined)
    anchor = re.search(r'Set pl2 = (\w+): Set hl1 = hs\(0\)', b).group(1)
    L, _, _, _ = path_block(t, 'PATH')
    Fp = L[anchor][1]; p2d = (L['p2'][1][0] - L['p2'][0][0], L['p2'][1][1] - L['p2'][0][1])
    q0 = []
    for i in range(N):
        q0 += list(segs[i][0]) + list(segs[i][1])
    q0 += list(hcl[0]) + list(hcl[1])
    q0 = np.array(q0, float)
    S = lambda q, i, j: (q[4 * i + 2 * j], q[4 * i + 2 * j + 1])
    C = lambda q, j: (q[4 * N + 2 * j], q[4 * N + 2 * j + 1])
    cons = []
    for i in range(N):
        k = (i + 1) % N
        cons.append((f'merge {i}/{k} x', lambda q, i=i, k=k: S(q, i, 1)[0] - S(q, k, 0)[0]))
        cons.append((f'merge {i}/{k} y', lambda q, i=i, k=k: S(q, i, 1)[1] - S(q, k, 0)[1]))
    for j in (0, 1):
        cons.append((f'hcl {j} x', lambda q, j=j: C(q, j)[0] - S(q, ax, j)[0])); cons.append((f'hcl {j} y', lambda q, j=j: C(q, j)[1] - S(q, ax, j)[1]))
    cons.append(('A0 on anchor x', lambda q: S(q, 0, 0)[0] - Fp[0])); cons.append(('A0 on anchor y', lambda q: S(q, 0, 0)[1] - Fp[1]))
    dirv = lambda q, i: (S(q, i, 1)[0] - S(q, i, 0)[0], S(q, i, 1)[1] - S(q, i, 0)[1])
    def crs(u, v): return (u[0] * v[1] - u[1] * v[0]) / (math.hypot(*u) * math.hypot(*v))
    def dot(u, v): return (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
    cons.append(('axis parallel p2', lambda q: crs(dirv(q, ax), p2d)))
    for m in re.finditer(r'HRel (\d+), (\d+), "(\w+)"', b):
        i, j, rel = int(m.group(1)), int(m.group(2)), m.group(3)
        if rel == 'sgPERPENDICULAR':
            cons.append((f'{i} perp {j}', lambda q, i=i, j=j: dot(dirv(q, i), dirv(q, j))))
        elif rel == 'sgPARALLEL':
            cons.append((f'{i} par {j}', lambda q, i=i, j=j: crs(dirv(q, i), dirv(q, j))))
        elif rel == 'sgCOLINEAR':
            cons.append((f'{i} col {j} dir', lambda q, i=i, j=j: crs(dirv(q, i), dirv(q, j))))
            def onl(q, i=i, j=j):
                a = S(q, j, 0); u = dirv(q, j); p = S(q, i, 0)
                return ((p[0] - a[0]) * u[1] - (p[1] - a[1]) * u[0]) / math.hypot(*u)
            cons.append((f'{i} col {j} on', onl))
        else:
            raise ValueError(rel)
    nd = 0
    for m in re.finditer(r'HDist (\d+), (\d+), "(\w+)", ([-\d.eE]+)', b):
        i, j, nm, val = int(m.group(1)), int(m.group(2)), m.group(3), float(m.group(4)); nd += 1
        def dist(q, i=i, j=j, val=val):
            a = S(q, j, 0); u = dirv(q, j); p = S(q, i, 0)
            return abs(((p[0] - a[0]) * u[1] - (p[1] - a[1]) * u[0]) / math.hypot(*u)) - val
        cons.append((f'dist {nm}', dist))
    return rank_report(cons, q0, dict(sketch='HEADSK', lines=N, anchor=anchor, dims=nd))


def check(path):
    t = open(path).read()
    ds.parse = parse_drive
    out = {'DRIVE': ds.check(path)}
    out['PATH'] = check_path(t, 'PATH')
    out['PATHX'] = check_path(t, 'PATHX')
    h = check_head(t)
    if h:
        out['HEADSK'] = h
    return out


if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        r = check(p)
        for k, v in r.items():
            ok = v['fully'] and v['redundant'] == 0 and v.get('max_residual', 0) < 1e-6
            bad += not ok
            print(f'{os.path.basename(p):26} {k:7} {"OK " if ok else "BAD"} {v}')
    sys.exit(1 if bad else 0)
