# per-configuration outline check: rebuild the DRIVE vertex chain of EVERY configuration (the macro only carries the reference one)
# and test it for self-intersection / zero-length segments. Straights: the emit() chain; tees/elbows: every leg profile.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, os, math, importlib
os.environ.setdefault('GS_OUT', OP.SCRATCH); os.environ.setdefault('GT_OUT', OP.SCRATCH)

def inter(a, b, c, d):
    def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (o(a, b, c) * o(a, b, d) < -1e-12) and (o(c, d, a) * o(c, d, b) < -1e-12)

def poly_issues(V):
    poly = list(V)
    if abs(poly[-1][1]) > 1e-9 or abs(poly[0][1]) > 1e-9: pass
    n = len(poly); bad = []
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if math.hypot(b[0] - a[0], b[1] - a[1]) < 1e-5: bad.append(f'zero segment {i}')
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1: continue
            if inter(poly[i], poly[(i + 1) % n], poly[j], poly[(j + 1) % n]): bad.append(f'segments {i}x{j}')
    return bad

def straight_chain(EA, EB, L, rB):
    swA = EA['kind'] == 'JICSW'
    if swA:
        V = [(x, r) for (x, r) in EA['VG'][::-1]]; V += [(x, r) for (x, r) in EA['VO']]; V += [(EA['endlen'], rB)]
    else:
        V = [(0.0, 0.0)] + (EA['V'] if EA['V'] else []) + [(EA['endlen'], rB)]
    V += [(L - EB['endlen'], rB)]
    if EB.get('cav') and EB['kind'] in ('JICSW', 'NPSMSW'):
        V += [(L - x, r) for (x, r) in EB['VO'][::-1]]; V += [(L - x, r) for (x, r) in EB['VG']]
    elif EB.get('cav'):
        V += [(L - x, r) for (x, r) in EB['VG']]
    else:
        V += [(L - x, r) for (x, r) in EB['V']][::-1]; V += [(L, 0.0)]
    return V

def check_straights(roots):
    import gen_straight2 as G
    for r in roots:
        built, skipped = G.build_rows(r)
        ok = [b for b in built if not b[7]]
        probs = []
        for cols, EA, EB, L, hexb, rB, body, chk in ok:
            V = straight_chain(EA, EB, L, rB)
            iss = poly_issues(V)
            if iss: probs.append((cols['$PRP@PartNo'], iss[:3]))
        print(f'{r:6} {len(ok):3} configs  outline problems: {len(probs)}', probs[:4])

def check_tees(roots):
    import gen_tee as T
    for r in roots:
        built, skipped = T.build_rows(r)
        ok = [b for b in built if not b['chk']]
        probs = []; nturn = 0
        for b in ok:
            for i, Lg in enumerate(b['legs'], 1):
                iss = poly_issues(Lg['V'])
                if iss: probs.append((b['pn'], i, iss[:3]))
                t = Lg.get('trim')
                if t:
                    # 2026-10-01 (NECK-6502): the neck turn rings of THIS configuration - on the neck line, positive length, rin < neck < rout,
                    # the ring rin..neck solid before the cut (above the swivel profile's own cavity in the slab) and kept by the bore,
                    # rout past every forged-corner point of the slab
                    nturn += 1; V = Lg['V']; bad = []
                    if abs(t['a0'] - V[3][0]) > 1e-6 or abs(t['a0'] + t['len'] - V[4][0]) > 1e-6: bad.append('turn not on the neck line')
                    if abs(t['r'] - V[3][1]) > 1e-9: bad.append('fill radius != neck radius')
                    if not (t['len'] > 0.01): bad.append(f'turn length {t["len"]}')
                    if not (0 < t['rin'] < t['r'] - 0.01 and t['rout'] > t['r'] + 0.01): bad.append(f'radii {t["rin"]} {t["r"]} {t["rout"]}')
                    if not (t['rin'] > t['cav'] + 0.005 and t['rin'] > Lg['bore'] / 2 + 0.005): bad.append(f'rin {t["rin"]} vs slab cavity {t["cav"]} / bore radius {Lg["bore"] / 2}')
                    if not (t['rout'] > t['reach'] + 0.02): bad.append(f'rout {t["rout"]} vs corner reach {t["reach"]}')
                    if bad: probs.append((b['pn'], i, bad))
        # 2026-10-01 (6802-E45): the corner neck trim loop (ORBTRIMi_SK) of every configuration whose table carries it - the design table
        # drives this closed loop in every configuration (live or suppressed): no zero segment, no self-intersection, off the axis
        tl = [(b['pn'], i, Lg) for b in ok for i, Lg in enumerate(b['legs'], 1) if f'$STATE@ORBTRIM{i}' in b['cols']]
        for pn, i, Lg in tl:
            iss = poly_issues(Lg['nwo_trim_pts']) + (['loop touches the axis'] if min(r_ for _, r_ in Lg['nwo_trim_pts']) < 1e-4 else [])
            if iss: probs.append((pn, f'ORBTRIM{i}', iss[:3]))
        # integration 2026-10-01: one summary line carrying both counters (corner neck trim loops of 6802-E45, neck turns of NECK-6502)
        print(f'{r:6} {len(ok):3} configs  leg outline problems: {len(probs)}', probs[:4], *([f'(corner neck trim loops checked: {len(tl)})'] if tl else []),
              *([f'(neck turns checked: {nturn})'] if nturn else []))

if __name__ == '__main__':
    kind = sys.argv[1]
    (check_straights if kind == 's' else check_tees)(sys.argv[2:])
