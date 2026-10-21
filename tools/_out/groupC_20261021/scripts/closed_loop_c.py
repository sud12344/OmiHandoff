"""closed_loop_c.py (group C, 2026-10-21): OCP closed loop of the compression roots of the staged toolset (tools_c).

Every generated configuration is rebuilt from the generator's OWN geometry - straights: the DRIVE vertex chain (checks/allcfg_check.straight_chain
= what the macro draws) revolved about X, common with the hex prism (HEXB across flats), the tube sockets (POCKET_A / _B: SOCKDIA x DEPTH from the
tip face), the bores (BORECUT_A / _B per bore mode), the female NPTF pocket (TAPDRILLB x DEPTH@POCKETCUT_B); forged roots: every bite leg = its
revolved LEG profile (socket inside it) minus its BORECUT cylinder (tip to crossing). Threads are not modelled (THD_* stay suppressed).
The rebuilt solid is read back with point-membership probes (BRepClass3d) - an extractor independent of the generator - and must return the SW2
row (thread major, thread length to the ramp, neck dia / length, hex face, socket dia / depth, bore, overall length / leg length; nut: countersink,
minor, cone start, tube hole, length). The same extractor reads the ten Brennan -08 STEPs (the features the fused nut does not hide) and must
return the record / library values. Writes closed_loop/closed_loop.txt + closed_loop.json."""
import os, sys, json, math
H = os.path.dirname(os.path.abspath(__file__)); STAGE = os.path.dirname(H); T = os.path.join(STAGE, 'tools_c')
ROOT = os.path.normpath(os.path.join(STAGE, '..', '..', '..'))
for p_ in (os.path.join(T, 'generators'), os.path.join(T, 'checks'), os.path.join(T, 'measure'), T): sys.path.insert(0, p_)
os.environ.setdefault('GS_OUT', os.path.join(STAGE, 'scratch')); os.environ.setdefault('GT_OUT', os.path.join(STAGE, 'scratch'))
import gen_straight2 as G
import gen_tee as GT
from allcfg_check import straight_chain
from model_nutcap import revolve, hex_prism, vol, nsolids, MM
from section import load
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN

TOL = 0.0012
OUT = os.path.join(STAGE, 'closed_loop'); os.makedirs(OUT, exist_ok=True)


def cyl(x0, dirx, r, h):
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x0 * MM, 0, 0), gp_Dir(dirx, 0, 0)), r * MM, h * MM).Shape()


class Probe:
    """membership probes of a solid in a leg frame: point(a, r) = O + a*u + r*v (inches)"""
    def __init__(self, S, O=(0, 0, 0), u=(1, 0, 0), v=(0, 0, 1)):
        self.c = BRepClass3d_SolidClassifier(S); self.O, self.u, self.v = O, u, v
    def inside(self, a, r):
        p = [self.O[k] + a * self.u[k] + r * self.v[k] for k in range(3)]
        self.c.Perform(gp_Pnt(*[q * MM for q in p]), 1e-7); return self.c.State() == TopAbs_IN
    def edge(self, f, lo, hi, n=60):
        """first switch of predicate f between lo and hi (coarse scan, then bisection) - None if none"""
        prev = f(lo); step = (hi - lo) / n; x = lo
        for k in range(1, n + 1):
            x2 = lo + step * k; cur = f(x2)
            if cur != prev:
                a, b = x, x2
                for _ in range(40):
                    m = (a + b) / 2
                    if f(m) == prev: a = m
                    else: b = m
                return (a + b) / 2
            x, prev = x2, cur
        return None
    def _first_switch(self, a, r0, step=0.01, rmax=3.0):
        f = lambda r: self.inside(a, r); prev = f(r0); r = r0
        while r < rmax:
            r2 = r + step; cur = f(r2)
            if cur != prev:
                lo, hi = r, r2
                for _ in range(30):
                    m = (lo + hi) / 2
                    if f(m) == prev: lo = m
                    else: hi = m
                return (lo + hi) / 2
            r = r2
        return None
    def inner_r(self, a):
        return self._first_switch(a, 1e-4)
    def outer_r(self, a, r0):
        return self._first_switch(a, r0)


def bite_read(P, rM_hint, EL_hint, visible_from=0.0):
    """read a bite end in the frame (a = 0 at the tip, increasing into the body): socket, bore, thread major, thread end, neck, hex face.
    visible_from: on a Brennan STEP the nut is fused over the tip region; outer readings start there."""
    g = {}
    g['rS'] = P.inner_r(0.01)
    g['K'] = P.edge(lambda a: P.inner_r(a) < g['rS'] - 0.01, 0.005, EL_hint, 30)
    g['rb'] = P.inner_r(g['K'] + 0.03)
    a_t = max(visible_from + 0.02, 0.02)
    g['rM'] = P.outer_r(a_t, g['rS'] + 0.02)
    g['rN'] = P.outer_r(EL_hint - 0.02, g['rS'] + 0.02)
    # the ramp is read at two levels between the thread major and the neck and extrapolated to both (its angle is reported, not assumed)
    q = lambda a: P.outer_r(a, g['rS'] + 0.02)
    l1, l2 = g['rM'] - 0.25 * (g['rM'] - g['rN']), g['rM'] - 0.75 * (g['rM'] - g['rN'])
    a1 = P.edge(lambda a: q(a) < l1, a_t, EL_hint - 0.005, 30); a2 = P.edge(lambda a: q(a) < l2, a_t, EL_hint - 0.005, 30)
    if a1 is not None and a2 is not None and a2 > a1:
        sl = (a2 - a1) / (l1 - l2)
        g['TZ'] = a1 - (g['rM'] - l1) * sl; g['neck0'] = a2 + (l2 - g['rN']) * sl; g['RAMPANG'] = math.degrees(math.atan2(l1 - l2, a2 - a1))
    else: g['TZ'] = g['neck0'] = None
    g['EL'] = P.edge(lambda a: P.outer_r(a, g['rS'] + 0.02) > g['rN'] + 0.01, g['neck0'] + 0.005, EL_hint + 0.08, 40) if g['neck0'] else None
    g['NL'] = g['EL'] - g['neck0'] if g['EL'] and g['neck0'] else None
    return g


def bite_expect(e, bore):
    rM = e['TM'] / 2; rN = e['ND'] / 2
    return dict(rS=e['A'] / 2, K=e['K'], rb=bore / 2, rM=rM, TZ=e['EL'] - e['NL'] - (rM - rN) / math.tan(math.radians(G.BITE_RAMPANG)), rN=rN, EL=e['EL'],
                NL=e['NL'], RAMPANG=G.BITE_RAMPANG)


def cmp(exp, got, tag, keys=None):
    bad = []
    for k in (keys or exp):
        if got.get(k) is None or abs(exp[k] - got[k]) > (0.1 if k.endswith('ANG') else TOL): bad.append(f'{tag} {k}: expect {exp[k]:.4f} got {got.get(k)}')
    return bad


# ------------------------------------------------------------------ straights
def build_straight(cols, EA, EB, L, hexb, rB, mode):
    S = revolve(straight_chain(EA, EB, L, rB))
    S = BRepAlgoAPI_Common(S, hex_prism(hexb, -0.1, L + 0.1)).Shape()
    for E_, sfx in ((EA, 'A'), (EB, 'B')):
        if E_['kind'] == 'BITEM':
            K_ = cols[f'DEPTH@POCKETCUT_{sfx}']; R_ = cols[f'SOCKDIA@POCKET_{sfx}'] / 2
            S = BRepAlgoAPI_Cut(S, cyl(-0.01, 1, R_, K_ + 0.01) if sfx == 'A' else cyl(L + 0.01, -1, R_, K_ + 0.01)).Shape()
    if EB['kind'] == 'NPTFF':
        S = BRepAlgoAPI_Cut(S, cyl(L + 0.01, -1, cols['TAPDRILLB@POCKET_B'] / 2, cols['DEPTH@POCKETCUT_B'] + 0.01)).Shape()
    if 'DA@BORE_A' in cols and cols['DA@BORE_A']:
        S = BRepAlgoAPI_Cut(S, cyl(-0.01, 1, cols['DA@BORE_A'] / 2, cols['DEPTH@BORECUT_A'] + 0.01 * (mode != 'cnut_thru'))).Shape()
    if 'DB@BORE_B' in cols and cols['DB@BORE_B']:
        S = BRepAlgoAPI_Cut(S, cyl(L + 0.01, -1, cols['DB@BORE_B'] / 2, cols['DEPTH@BORECUT_B'] + 0.01)).Shape()
    return S


def nut_read(P, L, cone_drop=0.0):
    g = {}
    g['rcs'] = P.inner_r(0.0005)
    g['rmin'] = P.inner_r(0.1)
    # the 45deg cone read at two levels and extrapolated to the minor (model) / to cone_top (the Brennan -08 STEP: its cone starts at the 0.6724
    # counterbore, 0.005 radial below the minor - not in the record, not modelled)
    l1, l2 = g['rmin'] - 0.02, g['rmin'] - 0.04
    a1 = P.edge(lambda a: P.inner_r(a) < l1, 0.1, L - 0.01, 40); a2 = P.edge(lambda a: P.inner_r(a) < l2, 0.1, L - 0.01, 40)
    sl = (a2 - a1) / (l1 - l2); top = g['rmin'] - (cone_drop or 0.0)
    g['E'] = a1 - (top - l1) * sl; g['CONEANG'] = math.degrees(math.atan2(l1 - l2, a2 - a1))
    g['rD'] = P.inner_r(L - 0.01)
    g['L'] = P.edge(lambda a: P.inside(a, g['rD'] + 0.02), L - 0.1, L + 0.1, 40)
    return g


def straights(lines, res):
    nb = nc = 0
    for root in ('C2402', 'C2403', 'C2405', 'C0318'):
        sp = G.SPEC[root]; built, _ = G.build_rows(root); ok = [b for b in built if not b[7]]
        for cols, EA, EB, L, hexb, rB, body, chk in ok:
            pn = cols['$PRP@PartNo']; S = build_straight(cols, EA, EB, L, hexb, rB, sp['bore'][0]); bad = []
            if nsolids(S) != 1: bad.append(f'{nsolids(S)} solids')
            if root == 'C0318':
                P = Probe(S, v=(0, 1, 0)); got = nut_read(P, L)
                exp = dict(rcs=EA['rcs'] - 0.0005, rmin=EA['rmin'], E=EB['E'], rD=EB['rD'], L=L, CONEANG=45)
                bad += cmp(exp, got, 'nut'); nc += len(exp)
                Pz = Probe(S, v=(0, 0, 1)); af = Pz.outer_r(L / 2, EA['rmin'] + 0.01) * 2
                if abs(af - hexb) > TOL: bad.append(f'hex flats {af:.4f} vs {hexb}')
                nc += 1
            else:
                for E_, sfx in ((EA, 'A'), (EB, 'B')):
                    if E_['kind'] != 'BITEM': continue
                    P = Probe(S, O=(0 if sfx == 'A' else L, 0, 0), u=(1 if sfx == 'A' else -1, 0, 0), v=(0, 0, 1))
                    bore = cols['DA@BORE_A'] if sfx == 'A' else cols['DB@BORE_B']
                    got = bite_read(P, E_['rM'], E_['e']['EL']); exp = bite_expect(E_['e'], bore)
                    bad += cmp(exp, got, f'End {sfx}'); nc += len(exp)
                Pl = Probe(S, v=(0, 0, 1))
                Lm = Pl.edge(lambda a: Pl.inside(a, EB['V'][0][1] - 0.01 if EB['V'] else (EB['td'] / 2 + 0.15 * EB['thread']['pitch'] + hexb / 2) / 2), L - 0.2, L + 0.05, 50)   # port face: between the port and the flats
                if Lm is None or abs(Lm - L) > TOL: bad.append(f'overall {Lm} vs L {L}')
                nc += 1
            nb += len(bad)
            res.append(dict(root=root, pn=pn, bad=bad)); lines.append(f'{pn:24} ' + ('OK' if not bad else 'BAD ' + '; '.join(bad)))
    return nb, nc


# ------------------------------------------------------------------ forged legs
def leg_solid(L_):
    S = revolve(L_['V'])
    return BRepAlgoAPI_Cut(S, cyl(L_['Mtip'] + 0.01, -1, L_['bore'] / 2, L_['Mtip'] + 0.02)).Shape()


def forged(lines, res):
    nb = nc = 0
    for root in ('C2500', 'C2501', 'C2502', 'C2601', 'C6801'):
        built, _ = GT.build_rows(root)
        for b in built:
            if b['chk']: continue
            bad = []
            for i, L_ in enumerate(b['legs'], 1):
                if L_['kind'] != 'BITEM': continue
                S = leg_solid(L_); M = L_['Mtip']
                P = Probe(S, O=(M, 0, 0), u=(-1, 0, 0), v=(0, 0, 1))
                got = bite_read(P, L_['rM'], L_['e']['EL']); exp = bite_expect(L_['e'], L_['bore'])
                bad += cmp(exp, got, f'leg {i}'); nc += len(exp)
                c_ = b['cols']; col_ = [k for k in c_ if k.startswith(f'M{i}@LEG{i}')]
                if not col_ or abs(c_[col_[0]] - M) > 1e-9: bad.append(f'leg {i} length column {col_} vs {M}')
                nc += 1
            nb += len(bad); res.append(dict(root=root, pn=b['pn'], bad=bad))
            lines.append(f'{b["pn"]:24} ' + ('OK' if not bad else 'BAD ' + '; '.join(bad)))
    return nb, nc


# ------------------------------------------------------------------ Brennan -08 STEPs (frames from measure/measure_c.txt)
STEPS = [  # file, frame origin, leg axis u (tip -> body), radial probe v, what the frame is, the bore of that end
    ('C2403-08-08', (0.711, 0, 0), (-1, 0, 0), (0, 0, 1), 'end A (+X)', 0.422),
    ('C2403-08-08', (-0.711, 0, 0), (1, 0, 0), (0, 0, 1), 'end B (-X)', 0.422),
    ('C2402-08-08', (-0.562, 0, 0), (1, 0, 0), (0, 0, 1), 'bite end (-X)', 0.391),
    ('C2405-08-06', (-0.562, 0, 0), (1, 0, 0), (0, 0, 1), 'bite end (-X)', 0.422),
    ('C2500-08-08-FG', (-1.25, 0, 0), (1, 0, 0), (0, 0, 1), 'leg -X', 0.422),
    ('C2500-08-08-FG', (0, 1.25, 0), (0, -1, 0), (0, 0, 1), 'leg +Y', 0.422),
    ('C2501-08-06-FG', (-1.25, 0, 0), (1, 0, 0), (0, 0, 1), 'bite leg -X', 0.422),
    ('C2502-08-06-FG', (-1.23, 0, 0), (1, 0, 0), (0, 0, 1), 'bite leg -X', 0.422),
    ('C2601-08-08-08-FG', (1.35, 0, 0), (-1, 0, 0), (0, 0, 1), 'run leg +X', 0.422),
    ('C2601-08-08-08-FG', (-1.35, 0, 0), (1, 0, 0), (0, 0, 1), 'run leg -X', 0.422),
    ('C6801-08-08-NWO-FG', (-1.25, 0, 0), (1, 0, 0), (0, 0, 1), 'bite leg -X', 0.422),
]


def brennan(lines, res):
    nb = nc = 0; e = G.BITE_MEAS[8]; mb = 0.318     # nut face to body tip at -08 (record MB1): the thread is visible from there
    exp = bite_expect(e, 0)
    for pn, O, u, v, what, bore in STEPS:
        S = load(os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp')); P = Probe(S, O, u, v)
        got = bite_read(P, exp['rM'], e['EL'], visible_from=mb); ex_ = dict(exp, rb=bore / 2)
        bad = cmp(ex_, got, what)
        if pn == 'C2402-08-08' and got.get('K') is not None and abs(got['K'] - 0.318) < TOL:
            # KNOWN: on this STEP a 0.505 x 0.013 ring sits between the 0.391 bore and the 0.514 x 0.305 socket - not modelled (SPEC C2402 note)
            bad = [x for x in bad if ' K:' not in x]; got['K_note'] = 'socket 0.305 + 0.013 ring (0.505) = 0.318, ring not modelled'
        nb += len(bad); nc += len(ex_)
        res.append(dict(root='BRENNAN', pn=pn + ' ' + what, bad=bad, got={k: (round(v_, 4) if isinstance(v_, float) else v_) for k, v_ in got.items() if v_ is not None}))
        lines.append(f'BRENNAN {pn:20} {what:14} ' + ('OK' if not bad else 'BAD ' + '; '.join(bad)) + '  read ' +
                     ' '.join(f'{k}={v_:.4f}' if isinstance(v_, float) else f'{k}: {v_}' for k, v_ in got.items() if v_ is not None))
    # nut
    S = load(os.path.join(ROOT, '09_STEP_FILES', 'BRENNAN_C0318-08.stp')); P = Probe(S, v=(0, 1, 0)); got = nut_read(P, 0.840, cone_drop=0.005)
    rmin = round((0.75 - 1.082532 / 16) / 2, 5)
    ex_ = dict(rcs=0.755 / 2 - 0.0005, rmin=rmin, E=0.599, rD=0.505 / 2, L=0.840, CONEANG=45)
    bad = cmp(ex_, got, 'C0318-08'); nb += len(bad); nc += len(ex_)
    lines.append('BRENNAN C0318-08 nut              ' + ('OK' if not bad else 'BAD ' + '; '.join(bad)) + '  read ' + ' '.join(f'{k}={v_:.4f}' for k, v_ in got.items()))
    res.append(dict(root='BRENNAN', pn='C0318-08', bad=bad))
    return nb, nc


if __name__ == '__main__':
    lines, res = [], []
    b1, c1 = straights(lines, res); b2, c2 = forged(lines, res); b3, c3 = brennan(lines, res)
    head = (f'closed loop {len([r for r in res if r["root"] != "BRENNAN"])} configurations: straights {c1} checks {b1} off, forged bite legs {c2} checks '
            f'{b2} off; Brennan -08 STEPs {c3} checks {b3} off (tolerance {TOL})')
    print(head); print('\n'.join(l for l in lines if 'BAD' in l or l.startswith('BRENNAN')))
    open(os.path.join(OUT, 'closed_loop.txt'), 'w').write(head + '\n' + '\n'.join(lines) + '\n')
    json.dump(res, open(os.path.join(OUT, 'closed_loop.json'), 'w'), indent=1)
