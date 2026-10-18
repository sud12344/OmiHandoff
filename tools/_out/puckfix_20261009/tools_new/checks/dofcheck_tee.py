import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import re, sys, math
import numpy as np
def legs(path):
    t = open(path).read()
    ld = t.split('Sub LoadLeg(i As Long)')[1].split('End Sub')[0]
    arrs = re.findall(r'If i = (\d+) Then v = Array\( _\n(.*?)\)\n', ld, re.S)
    out = {}
    for i, a in arrs:
        nums = [float(x) for x in re.findall(r'-?\d+\.\d+', a)]
        out[int(i)] = np.array([(nums[k], nums[k + 1]) for k in range(0, len(nums), 2)])
    dims = {}
    for i in out:
        blk = t.split(f'stepName = "LEG{i} sketch"')[1].split(f'swFeat.Name = "LEG{i}"')[0]
        dims[i] = re.findall(r'Call (Dim_\w+|Collinear|DimLenU|DimRadU)\(([^)]*)\)', blk)
    return out, dims
def check(P, dims):
    n = len(P); segs = [(i, (i + 1) % n) for i in range(n)]
    X = lambda q, i: q[2 * i]; Y = lambda q, i: q[2 * i + 1]
    cons = [('ox', lambda q: X(q, 0)), ('oy', lambda q: Y(q, 0))]
    for k, (a, b) in enumerate(segs):
        ya, yb = P[a][1], (P[b][1] if k < n - 1 else 0.0); xa, xb = P[a][0], P[b][0]
        if k == n - 1: ya = P[n - 1][1]
        if abs(ya - yb) < 1e-9: cons.append((f'H{k}', lambda q, a=a, b=b: Y(q, a) - Y(q, b)))
        elif abs(xa - xb) < 1e-9: cons.append((f'V{k}', lambda q, a=a, b=b: X(q, a) - X(q, b)))
    def seglen(q, k):
        a, b = segs[k]; return math.hypot(X(q, b) - X(q, a), Y(q, b) - Y(q, a))
    def segang(q, k):
        a, b = segs[k]; return math.atan2(Y(q, b) - Y(q, a), X(q, b) - X(q, a))
    for name, args in dims:
        a = [x.strip() for x in args.split(',')]
        if name == 'Dim_pair': i, j = int(a[0]), int(a[1]); cons.append((a[2], lambda q, i=i, j=j: X(q, segs[i][0]) - X(q, segs[j][0])))
        elif name in ("Dim_rad", "DimRadU"): i = int(a[0]); cons.append((a[1], lambda q, i=i: Y(q, segs[i][0])))
        elif name in ("Dim_len", "DimLenU"):
            i = int(a[0])
            if i == -1: cons.append((a[1], lambda q: X(q, segs[n - 2][1]) - X(q, 0)))
            else: cons.append((a[1], lambda q, i=i: seglen(q, i)))
        elif name == 'Dim_ptline':
            sp_, ue, sl = int(a[0]), a[1] == 'True', int(a[2]); pt = segs[sp_][1] if ue else segs[sp_][0]; a0, b0 = segs[sl]
            def dist(q, pt=pt, a0=a0, b0=b0, sl=sl):
                x1, y1 = X(q, a0), Y(q, a0); x2, y2 = X(q, b0), Y(q, b0)
                if sl == n - 1: y2 = Y(q, a0)
                if abs(x2 - x1) + abs(y2 - y1) < 1e-12: x2 = x1 + 1.0
                dx, dy = x2 - x1, y2 - y1; L_ = math.hypot(dx, dy)
                return ((X(q, pt) - x1) * dy - (Y(q, pt) - y1) * dx) / L_
            cons.append((a[3], dist))
        elif name == 'Dim_ang':
            i, j = int(a[0]), int(a[1]); cons.append((a[2], lambda q, i=i, j=j: math.sin(segang(q, i) - (segang(q, j) if j != n - 1 else 0.0))))
        elif name == 'Collinear':
            i, j = int(a[0]), int(a[1]); cons.append(('col', lambda q, i=i, j=j: Y(q, segs[i][0]) - Y(q, segs[j][0])))
    q0 = P.flatten().astype(float); J = np.zeros((len(cons), len(q0))); h = 1e-7
    for c, (nm, f) in enumerate(cons):
        for k in range(len(q0)):
            qp = q0.copy(); qm = q0.copy(); qp[k] += h; qm[k] -= h; J[c, k] = (f(qp) - f(qm)) / (2 * h)
    r = np.linalg.matrix_rank(J, tol=1e-6)
    return dict(n=n, unknowns=len(q0), cons=len(cons), rank=int(r), fully=bool(r == len(q0)), redundant=len(cons) - int(r))
def trims(path):
    """2026-10-01 (6802-E45): the corner neck trim sketches ORBTRIMi_SK of a 45 deg adjustable-ORB elbow - a CLOSED loop drawn by DrawLoopAx
    (corners merged, horizontal / vertical relations as drawn) plus an axis centreline from the origin along +X (horizontal, fixed length)"""
    t = open(path).read(); out = {}
    for m in re.finditer(r'stepName = "(ORBTRIM\d+) sketch"(.*?)swFeat\.Name = "\1_SK"', t, re.S):
        blk = m.group(2)
        a = re.search(r'DrawLoopAx Array\(([^)]*)\), (-?\d+\.\d+), "(\w+)"', blk)
        nums = [float(x) for x in a.group(1).split(',')]
        out[m.group(1)] = (np.array([(nums[k], nums[k + 1]) for k in range(0, len(nums), 2)]), float(a.group(2)),
                           re.findall(r'Call (Dim_\w+|DimSegOrigin)\(((?:seg\(\d+\)|[^)])*)\)', blk))
    return out
def check_loop(P, axl, dims):
    n = len(P); segs = [(i, (i + 1) % n) for i in range(n)]; c = 2 * n          # unknowns: the n loop points, then the centreline start / end
    X = lambda q, i: q[2 * i]; Y = lambda q, i: q[2 * i + 1]
    def ldist(q, px, py, a, b):            # signed distance of (px, py) from the line through loop points a, b
        x1, y1, x2, y2 = X(q, a), Y(q, a), X(q, b), Y(q, b); L_ = math.hypot(x2 - x1, y2 - y1)
        return ((px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)) / L_
    def cldist(q, px, py):                 # signed distance from the centreline
        x1, y1, x2, y2 = q[c], q[c + 1], q[c + 2], q[c + 3]; L_ = math.hypot(x2 - x1, y2 - y1)
        return ((px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)) / L_
    cons = [('CL start x', lambda q: q[c], 0.0), ('CL start y', lambda q: q[c + 1], 0.0), ('CL horizontal', lambda q: q[c + 3] - q[c + 1], 0.0),
            ('CL length', lambda q: math.hypot(q[c + 2] - q[c], q[c + 3] - q[c + 1]), axl)]
    for k, (a, b) in enumerate(segs):
        if abs(P[a][1] - P[b][1]) < 1e-9: cons.append((f'H{k}', lambda q, a=a, b=b: Y(q, a) - Y(q, b), 0.0))
        elif abs(P[a][0] - P[b][0]) < 1e-9: cons.append((f'V{k}', lambda q, a=a, b=b: X(q, a) - X(q, b), 0.0))
    for name, args in dims:
        a = [x.strip().strip('"') for x in args.split(',')]
        if name == 'DimSegOrigin':
            i = int(re.search(r'seg\((\d+)\)', a[0]).group(1)); v = float(a[2])
            cons.append((a[1], lambda q, i=i: abs(ldist(q, 0.0, 0.0, *segs[i])), v))
        elif name == 'Dim_len':
            i = int(a[0]); cons.append((a[1], lambda q, i=i: math.hypot(X(q, segs[i][1]) - X(q, segs[i][0]), Y(q, segs[i][1]) - Y(q, segs[i][0])), float(a[2])))
        elif name == 'Dim_rad':        # line-to-centreline distance (SP3: the radius); the drawn line is parallel to the centreline
            i = int(a[0]); cons.append((a[1], lambda q, i=i: abs(cldist(q, X(q, segs[i][0]), Y(q, segs[i][0]))), float(a[2])))
        elif name == 'Dim_pair':       # distance between two parallel lines
            i, j = int(a[0]), int(a[1]); cons.append((a[2], lambda q, i=i, j=j: abs(ldist(q, X(q, segs[j][0]), Y(q, segs[j][0]), *segs[i])), float(a[3])))
        else: raise ValueError(f'trim sketch: unknown dimension call {name}')
    q0 = np.concatenate([P.flatten(), [0.0, 0.0, axl, 0.0]]).astype(float); J = np.zeros((len(cons), len(q0))); h = 1e-7
    for k_, (nm, f, v) in enumerate(cons):
        for k in range(len(q0)):
            qp = q0.copy(); qm = q0.copy(); qp[k] += h; qm[k] -= h; J[k_, k] = (f(qp) - f(qm)) / (2 * h)
    r = np.linalg.matrix_rank(J, tol=1e-6)
    bad = [f'{nm} {f(q0):.9f} vs {v:.9f}' for nm, f, v in cons if abs(f(q0) - v) > 1e-8]      # the drawn loop must carry the dimension values
    return dict(n=n, unknowns=len(q0), cons=len(cons), rank=int(r), fully=bool(r == len(q0)), redundant=len(cons) - int(r), value_mismatch=bad)
def neck_rings(path):
    # 2026-10-01 (NECK-6502): the swivel neck turn sketches, Set ... = NeckRing("NAME", "PFX", a0, len, r0, r1, isCut) in the build body
    t = open(path).read()
    return [(m.group(1), m.group(2), *[float(x) for x in m.group(3, 4, 5, 6)]) for m in
            re.finditer(r'NeckRing\("(\w+)", "(\w+)", (-?[\d.]+)#?, (-?[\d.]+)#?, (-?[\d.]+)#?, (-?[\d.]+)#?, (?:True|False)\)', t)]
def check_ring(a0, ln, r0, r1):
    """mirror of the VBA Function NeckRing: P0 (a0,r0) P1 (a1,r0) P2 (a1,r1) P3 (a0,r1) joined by merged lines s0..s3, centreline C0-C1.
    Relations: s0, s2, centreline horizontal; s1, s3 vertical; C0 coincident with the origin; C1 vertical-points with P1.
    Dims: origin-to-s3 (A0), length of s0 (LEN), origin-to-s0 (RIN), origin-to-s2 (ROUT)."""
    a1 = a0 + ln
    q0 = np.array([a0, r0, a1, r0, a1, r1, a0, r1, 0.0, 0.0, a1, 0.0])
    X = lambda q, k: q[2 * k]; Y = lambda q, k: q[2 * k + 1]
    def dist(q, i, j):        # signed distance from the origin to the line through points i, j
        dx, dy = X(q, j) - X(q, i), Y(q, j) - Y(q, i); L_ = math.hypot(dx, dy)
        return (X(q, i) * dy - Y(q, i) * dx) / L_
    cons = [lambda q: Y(q, 0) - Y(q, 1), lambda q: Y(q, 2) - Y(q, 3), lambda q: X(q, 1) - X(q, 2), lambda q: X(q, 3) - X(q, 0),
            lambda q: Y(q, 4) - Y(q, 5), lambda q: X(q, 4), lambda q: Y(q, 4), lambda q: X(q, 5) - X(q, 1),
            lambda q: dist(q, 3, 0), lambda q: math.hypot(X(q, 1) - X(q, 0), Y(q, 1) - Y(q, 0)), lambda q: dist(q, 2, 3), lambda q: dist(q, 0, 1)]
    J = np.zeros((len(cons), len(q0))); h = 1e-7
    for c, f in enumerate(cons):
        for k in range(len(q0)):
            qp = q0.copy(); qm = q0.copy(); qp[k] += h; qm[k] -= h; J[c, k] = (f(qp) - f(qm)) / (2 * h)
    r = np.linalg.matrix_rank(J, tol=1e-6)
    return dict(unknowns=len(q0), cons=len(cons), rank=int(r), fully=bool(r == len(q0)), redundant=len(cons) - int(r))
IN_ = 0.0254
for p in sys.argv[1:]:
    L, D = legs(p)
    for i in sorted(L): print(p.split('/')[-1], 'LEG', i, check(L[i], D[i]))
    for nm, (P_, axl_, d_) in sorted(trims(p).items()): print(p.split('/')[-1], nm, check_loop(P_, axl_, d_))
    rings = neck_rings(p)
    for nm, pfx, a0, ln, r0, r1 in rings:
        res = check_ring(a0, ln, r0, r1)
        # the turn must sit exactly on the LEG1 neck line (vertices 3 -> 4 of the reference profile): body face to nut rear face; the cut
        # ring (TRIM) runs from inside the neck to beyond it, the boss ring (FILL) from the same inner radius exactly to the neck radius
        P = L[1]; face, nutr, neck = P[3][0], P[4][0], P[3][1]
        geo = abs(a0 - face) < 1e-8 and abs(a0 + ln - nutr) < 1e-8 and 0 < r0 < neck - 1e-6
        geo = geo and ((neck + 1e-6 < r1) if pfx == 'TRIM' else (abs(r1 - neck) < 1e-8))
        geo = geo and all(abs(r0 - q[4]) < 1e-8 for q in rings)          # TRIM and FILL share the inner radius
        res['on_neck_line'] = bool(geo)
        print(p.split('/')[-1], nm, f'(a0 {a0 / IN_:.4f}, len {ln / IN_:.4f}, r {r0 / IN_:.4f}..{r1 / IN_:.4f}, neck {neck / IN_:.4f})', res)
