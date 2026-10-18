#!/usr/bin/env python3
"""Rigidity check of a gen_straight2 DRIVE sketch, straight from the emitted .bas:
points from LoadPoints, segments seg(i) = P(i)->P(i+1) (last = closing line on the axis), automatic H/V constraints,
origin coincidence, and every Dim_* call in the DRIVE block. Builds the constraint Jacobian numerically and reports
rank vs unknowns (fully defined <=> rank == 2*npts and no redundant constraints)."""
import re, sys, math
import numpy as np

def parse(path):
    t = open(path).read()
    arr = re.search(r'v = Array\((.*?)\)\n', t, re.S).group(1)
    nums = [float(x) for x in re.findall(r'-?\d+\.\d+', arr)]
    P = np.array([(nums[i], nums[i + 1]) for i in range(0, len(nums), 2)])
    blk = t.split('================= 1. DRIVE sketch')[1].split('swFeat.Name = "DRIVE"')[0]
    dims = re.findall(r'Call (Dim_\w+|Collinear)\(([^)]*)\)', blk)
    return P, dims

def check(path, verbose=False):
    P, dims = parse(path); n = len(P)
    segs = [(i, (i + 1) % n) for i in range(n)]
    # the closing segment runs from P[n-1] to P[0] along the axis (P[n-1].y = 0 in the model)
    cons = []   # functions of flat coords -> residual
    def X(q, i): return q[2 * i]
    def Y(q, i): return q[2 * i + 1]
    # origin
    cons.append(('origin x', lambda q: X(q, 0))); cons.append(('origin y', lambda q: Y(q, 0)))
    for k, (a, b) in enumerate(segs):
        ya, yb = P[a][1], P[b][1]; xa, xb = P[a][0], P[b][0]
        if k == n - 1: ya = P[n - 1][1]; yb = 0.0
        if abs(ya - yb) < 1e-9: cons.append((f'H seg{k}', lambda q, a=a, b=b: Y(q, a) - Y(q, b)))
        elif abs(xa - xb) < 1e-9: cons.append((f'V seg{k}', lambda q, a=a, b=b: X(q, a) - X(q, b)))
    def seglen(q, k):
        a, b = segs[k]; return math.hypot(X(q, b) - X(q, a), Y(q, b) - Y(q, a))
    def segang(q, k):
        a, b = segs[k]; return math.atan2(Y(q, b) - Y(q, a), X(q, b) - X(q, a))
    for name, args in dims:
        a = [x.strip() for x in args.split(',')]
        if name == 'Dim_pair':
            i, j = int(a[0]), int(a[1])
            cons.append((f'pair {a[2]}', lambda q, i=i, j=j: X(q, segs[i][0]) - X(q, segs[j][0])))
        elif name == 'Dim_rad':
            i = int(a[0]); cons.append((f'rad {a[1]}', lambda q, i=i: Y(q, segs[i][0])))
        elif name == 'Dim_len':
            i = int(a[0])
            if i == -1: cons.append((f'len {a[1]}', lambda q: X(q, segs[n - 2][1]) - X(q, 0)))
            else: cons.append((f'len {a[1]}', lambda q, i=i: seglen(q, i)))
        elif name == 'Dim_ptline':
            sp, ue, sl = int(a[0]), a[1] == 'True', int(a[2])
            pt = segs[sp][1] if ue else segs[sp][0]
            a0, b0 = segs[sl]
            def dist(q, pt=pt, a0=a0, b0=b0, sl=sl):
                x1, y1 = X(q, a0), Y(q, a0)
                x2, y2 = (X(q, b0), Y(q, b0))
                if sl == n - 1: y2 = Y(q, a0)   # closing line
                dx, dy = x2 - x1, y2 - y1; L_ = math.hypot(dx, dy)
                return ((X(q, pt) - x1) * dy - (Y(q, pt) - y1) * dx) / L_
            cons.append((f'ptline {a[3]}', dist))
        elif name == 'Dim_ang':
            i, j = int(a[0]), int(a[1])
            cons.append((f'ang {a[2]}', lambda q, i=i, j=j: math.sin(segang(q, i) - segang(q, j)) if j != n - 1 else math.sin(segang(q, i))))
        elif name == 'Collinear':
            i, j = int(a[0]), int(a[1])     # two horizontal lines made collinear -> same radius
            a0, b0 = segs[i]
            if abs(P[a0][1] - P[b0][1]) < 1e-9:      # horizontal lines -> same radius
                cons.append((f'collinear {i},{j}', lambda q, i=i, j=j: Y(q, segs[i][0]) - Y(q, segs[j][0])))
            else:                                      # vertical lines -> same axial position
                cons.append((f'collinear {i},{j}', lambda q, i=i, j=j: X(q, segs[i][0]) - X(q, segs[j][0])))
        else:
            raise ValueError(name)
    q0 = P.flatten().astype(float)
    J = np.zeros((len(cons), len(q0)))
    h = 1e-7
    for c, (nm, f) in enumerate(cons):
        for k in range(len(q0)):
            qp = q0.copy(); qm = q0.copy(); qp[k] += h; qm[k] -= h
            J[c, k] = (f(qp) - f(qm)) / (2 * h)
    rank = np.linalg.matrix_rank(J, tol=1e-6)
    unknowns = len(q0)
    # also check the closing segment endpoint P[n-1] lies on the axis
    res = dict(points=n, unknowns=unknowns, constraints=len(cons), rank=int(rank), dims=len(dims),
               fully=rank == unknowns, redundant=len(cons) - rank, apex_on_axis=abs(P[n - 1][1]) < 1e-9)
    if verbose and rank < unknowns:
        # which coordinates are free: null space
        u, s, vt = np.linalg.svd(J)
        ns = vt[rank:]
        free = sorted({(k // 2, 'xy'[k % 2]) for v in ns for k in np.where(abs(v) > 1e-3)[0]})
        res['free'] = free
    return res

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p.split('/')[-1], check(p, verbose=True))
