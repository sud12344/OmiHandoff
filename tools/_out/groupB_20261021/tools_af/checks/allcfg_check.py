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
        V = [(0.0, 0.0)] + (EA['V'] if EA['V'] else []) + ([] if EA.get('cap') else [(EA['endlen'], rB)])   # 2026-10-02 (PLUGS): capped NPTF cone ends on the body line
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

def faceoff_issues(T, sp, b, i, Lg):
    """2026-10-09 (wave 2, HOSEB, DESIGN 4.11): the face-off of hose leg i in THIS configuration, from its SW2 values - an independent, denser
    numpy sampling (not the generator's faceoff_geo): depth > 0; the cut ends 0.02 before the bead; bore/2 + 0.005 <= rin <= rS - 0.005; cut and
    refill share plane / rin / depth; the stub ring rin..rS lies inside the cut region; every forged-corner point (30deg puck and the other leg's
    hex arm, surface AND interior) past the hose hex face and outside the stub lies inside the cut region; no point of the other leg beyond its
    hex arm (its revolved profile incl. the locknut envelope, surface and interior) lies strictly inside the cut region.
    Returns (problems, number of corner points past the face)."""
    import numpy as np
    c = b['cols']; BR, AC = b['BR'], b['AC']; e45 = bool(sp.get('e45')); bad = []
    sh = c[f'D1@HFPLN{i}']; dep = c[f'DEPTH@HOSEFACE{i}']; rin = c[f'HF{i}_DIN@HOSEFACE{i}_SK'] / 2; rS = c[f'SF{i}_DOUT@STUBFILL{i}_SK'] / 2
    if abs(c[f'SF{i}_DIN@STUBFILL{i}_SK'] / 2 - rin) > 1e-9 or abs(c[f'DEPTH@STUBFILL{i}'] - dep) > 1e-9: bad.append('refill ring / depth differ from the cut')
    if abs(rS - Lg['rS']) > 1e-9 or abs(sh - Lg['hexl']) > 1e-9: bad.append('plane offset / stub radius differ from the hose leg')
    if not dep > 0: bad.append(f'depth {dep}')
    if not sh + dep <= Lg['bead'][0] - 0.02 + 1e-9: bad.append(f'cut end {sh + dep:.4f} vs bead start {Lg["bead"][0]:.4f}')
    if not (Lg['bore'] / 2 + 0.005 <= rin + 1e-9 and rin <= rS - 0.005 + 1e-9): bad.append(f'rin {rin} vs bore radius {Lg["bore"] / 2} / stub radius {rS}')
    ax = []
    for k in (1, 2):
        a_, s_ = T.place(sp)[k]; ax.append(np.array((T.UXV, T.UYV) if a_ == 'U' else (float(s_), 0.0) if a_ == 0 else (0.0, float(s_))))
    u = ax[i - 1]; n = np.array((-u[1], u[0])); uo = ax[2 - i]; no = np.array((-uo[1], uo[0])); O = b['legs'][2 - i]
    if e45:
        rout = c[f'HF{i}_DOUT@HOSEFACE{i}_SK'] / 2
        if not rS < rout: bad.append('stub ring outside the cut ring')
        def inreg(a, t, z, e):
            r = np.hypot(t, z); return (a >= sh + e) & (a <= sh + dep - e) & (r >= rin + e) & (r <= rout - e)
    else:
        ylo, ytop, zh, zh2 = (c[f'HF{i}_{k}@HOSEFACE{i}_SK'] for k in ('YLO', 'YTOP', 'ZH', 'ZH2'))
        if abs(zh - zh2) > 1e-9 or not rS < min(ylo, ytop, zh): bad.append('stub ring not inside the cut rectangle')
        def inreg(a, t, z, e):
            return (a >= sh + e) & (a <= sh + dep - e) & (t >= -ylo + e) & (t <= ytop - e) & (np.abs(z) <= zh - e) & (np.hypot(t, z) >= rin + e)
    T30 = math.tan(math.radians(30)); P = []
    zz = np.linspace(-BR, BR, 81); th = np.linspace(0, 2 * math.pi, 720, endpoint=False)
    for f in (1.0, 0.9, 0.75, 0.5, 0.25):                    # the puck: double cone about Z, surface + interior
        R = (AC - np.abs(zz) * T30)[:, None] * f
        P.append(np.stack([(R * np.cos(th)).ravel(), (R * np.sin(th)).ravel(), np.repeat(zz, th.size)], 1))
    pp, qz = np.meshgrid(np.linspace(-AC, AC, 61), np.linspace(-BR, BR, 41)); pp, qz = pp.ravel(), qz.ravel()
    hx = (np.abs(qz) <= BR + 1e-12) & (np.abs(pp) * math.sqrt(3) / 2 + np.abs(qz) / 2 <= BR + 1e-12); pp, qz = pp[hx], qz[hx]
    for ao in np.linspace(0, O['hexl'], 81):                   # the other leg's hex arm, flats normal to Z, crossing .. its hexl
        P.append(np.stack([ao * uo[0] + pp * no[0], ao * uo[1] + pp * no[1], qz], 1))
    P = np.concatenate(P); a = P[:, 0] * u[0] + P[:, 1] * u[1]; t = P[:, 0] * n[0] + P[:, 1] * n[1]
    past = (a > sh + 1e-6) & (np.hypot(t, P[:, 2]) > rS + 1e-6)
    out_ = past & ~inreg(a, t, P[:, 2], -1e-6)
    if out_.any():
        k = np.argmax(np.hypot(t, P[:, 2]) * out_); bad.append(f'{int(out_.sum())} corner points past the hose hex face outside the cut region (e.g. a {a[k]:.4f}, t {t[k]:.4f}, z {P[k, 2]:.4f})')
    E = []; ph = np.linspace(0, 2 * math.pi, 144, endpoint=False)
    for (a1, r1), (a2, r2) in zip(O['V'], O['V'][1:]):       # the other leg beyond its hex arm: revolved profile, surface + interior
        for s_ in np.linspace(0, 1, 41):
            ao = a1 + (a2 - a1) * s_; ro = r1 + (r2 - r1) * s_
            if ao <= O['hexl'] + 1e-9: continue
            for f in (1.0, 0.75, 0.5, 0.25):
                E.append(np.stack([ao * uo[0] + f * ro * np.cos(ph) * no[0], ao * uo[1] + f * ro * np.cos(ph) * no[1], f * ro * np.sin(ph)], 1))
    if E:
        E = np.concatenate(E); a = E[:, 0] * u[0] + E[:, 1] * u[1]; t = E[:, 0] * n[0] + E[:, 1] * n[1]
        hit = inreg(a, t, E[:, 2], 1e-6)
        if hit.any(): bad.append(f'{int(hit.sum())} points of the other leg\'s end inside the cut region')
    return bad, int(past.sum())


def check_tees(roots):
    import gen_tee as T
    for r in roots:
        built, skipped = T.build_rows(r)
        ok = [b for b in built if not b['chk']]
        probs = []; nturn = 0; nface = 0; npast_ = 0
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
                if Lg.get('faceoff'):       # 2026-10-09 (wave 2, HOSEB): the face-off region of this configuration
                    bad, npast = faceoff_issues(T, T.SPEC[r], b, i, Lg); nface += 1; npast_ += npast
                    if bad: probs.append((b['pn'], f'HOSEFACE{i}', bad))
        # 2026-10-01 (6802-E45): the corner neck trim loop (ORBTRIMi_SK) of every configuration whose table carries it - the design table
        # drives this closed loop in every configuration (live or suppressed): no zero segment, no self-intersection, off the axis
        tl = [(b['pn'], i, Lg) for b in ok for i, Lg in enumerate(b['legs'], 1) if f'$STATE@ORBTRIM{i}' in b['cols']]
        for pn, i, Lg in tl:
            iss = poly_issues(Lg['nwo_trim_pts']) + (['loop touches the axis'] if min(r_ for _, r_ in Lg['nwo_trim_pts']) < 1e-4 else [])
            if iss: probs.append((pn, f'ORBTRIM{i}', iss[:3]))
        # 2026-10-21 (group B): the female ORB port mouth loop (ORBMOUTHi_SK) of every configuration: no zero segment, no self-intersection, off
        # the axis, its bottom inside the port drill (rin < drill radius) and above the pocket bottom (the mouth must not cut below the drilled pocket)
        ml = [(b['pn'], i, Lg) for b in ok for i, Lg in enumerate(b['legs'], 1) if Lg.get('orbmouth')]
        for pn, i, Lg in ml:
            om = Lg['orbmouth']; pts = om['pts']; M_ = Lg['V'][-1][0]
            iss = poly_issues(pts) + (['loop touches the axis'] if min(r_ for _, r_ in pts) < 1e-4 else [])
            if not (om['rin'] < om['rmin'] - 1e-6): iss.append('mouth bottom not inside the port drill')
            if not (M_ - pts[0][0] < Lg['pocket'] - 0.02): iss.append(f'mouth depth {M_ - pts[0][0]:.4f} reaches the pocket depth {Lg["pocket"]:.4f}')
            if iss: probs.append((pn, f'ORBMOUTH{i}', iss[:3]))
        # integration 2026-10-01: one summary line carrying both counters (corner neck trim loops of 6802-E45, neck turns of NECK-6502)
        print(f'{r:6} {len(ok):3} configs  leg outline problems: {len(probs)}', probs[:4], *([f'(corner neck trim loops checked: {len(tl)})'] if tl else []),
              *([f'(neck turns checked: {nturn})'] if nturn else []), *([f'(ORB port mouth loops checked: {len(ml)})'] if ml else []),
              *([f'(hose face-offs checked: {nface}, forged-corner sample points past the hose hex face: {npast_}, all inside the cut region)'] if nface and not
                [p_ for p_ in probs if str(p_[1]).startswith('HOSEFACE')] else [f'(hose face-offs checked: {nface})'] if nface else []))

if __name__ == '__main__':
    kind = sys.argv[1]
    (check_straights if kind == 's' else check_tees)(sys.argv[2:])
