"""measure_pilots.py - leg sections of the Brennan pilot STEPs of this group (tools/measure section.py / prof.py, OCP).
For every leg (direction in the XY plane, degrees): the Z=0 section in leg coordinates (a along the leg from the origin = the crossing,
r off the axis); prints the tip (largest a), every axis-parallel line (r, a-range) and, for axis-aligned legs, the flats read in the
section normal to the cross axis (hex flats normal to Z appear there at r = A/F / 2).
Validation: the values the catalog prints (legs, A/F) must come out of the same sections before a bore is read (see REPORT.md).
Usage: python -I measure_pilots.py  -> ../evidence/pilot_sections.txt"""
import os, sys, math, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
sys.path.insert(0, os.path.join(ROOT, 'tools', 'measure'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from section import load, section, edges   # noqa: E402

STEP = os.path.join(ROOT, '09_STEP_FILES')
# part -> legs (name, direction deg in XY); 1700 straights are measured by FLANGE62 flange62.py (validated, jsonl) - not here
PILOTS = {
    '1703-24-24-FG': [('flange', -90.0), ('JIC', 135.0)],
    '1704-24-24-FG': [('JIC', 180.0), ('flange', -90.0)],
    '1804-08-08-FG': [('JIC', 180.0), ('flange', -90.0)],
    '4501-08-08-FG': None, '4503-08-08-FG': None, '4601-08-06-NWO-FG': None, '4603-16-16-NWO-FG': None,
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def legsec(sh, ang, n=(0, 0, 1)):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    E = edges(section(sh, n))
    out = []
    for kind, pts in E:
        if n == (0, 0, 1):
            P = [(q[0] * c + q[1] * s, -q[0] * s + q[1] * c) for q in pts]
        else:   # axis-aligned leg, section normal to the in-plane cross axis: r = z
            P = [(q[0] * c + q[1] * s, q[2]) for q in pts]
        out.append((kind, P))
    return out


def summarize(E, label):
    lines = []
    amax = max(a for _, P in E for a, r in P)
    lines.append(f'    {label}: tip a_max = {amax:.4f}')
    par = []
    for kind, P in E:
        (a1, r1), (a2, r2) = P[0], P[-1]
        if kind == 'L' and abs(r1 - r2) < 1e-4 and abs(a2 - a1) > 0.01 and r1 > 0.005:
            par.append((round(r1, 4), round(min(a1, a2), 4), round(max(a1, a2), 4)))
        if isinstance(kind, tuple) or str(kind).startswith('S'):
            rr = [r for a, r in P]
            if max(rr) - min(rr) < 1e-4 and min(rr) > 0.005 and max(a for a, r in P) - min(a for a, r in P) > 0.01:
                par.append((round(rr[0], 4), round(min(a for a, r in P), 4), round(max(a for a, r in P), 4)))
    for r, a1, a2 in sorted(set(par)):
        lines.append(f'      axis-parallel r {r:.4f} (dia {2 * r:.4f})  a {a1:.4f} .. {a2:.4f}')
    return lines, amax, sorted(set(par))


def main():
    out, res = [], {}
    for pn, legs in PILOTS.items():
        p = os.path.join(STEP, f'BRENNAN_{pn}.stp')
        if not os.path.exists(p):
            out.append(f'{pn}: STEP missing'); continue
        out.append(f'== {pn}  {p}  sha256 {sha(p)[:16]}')
        if legs is None:
            out.append('   (shape-only sample: the catalog prints every body size of this family; HOSEB DESIGN s3 read it - not re-measured)')
            continue
        sh = load(p)
        res[pn] = {}
        for name, ang in legs:
            E = [(k, P) for k, P in legsec(sh, ang) if max(r for a, r in P) > -1e-6 and min(r for a, r in P) > -1e-6]
            L, amax, par = summarize(E, f'leg {name} dir {ang:g} deg, Z=0 section (hex corners)')
            out += L
            rec = dict(tip=round(amax, 4), z0_parallel=par)
            if ang in (0.0, 90.0, 180.0, -90.0):
                n = (0, 1, 0) if ang in (0.0, 180.0) else (1, 0, 0)
                E2 = [(k, P) for k, P in legsec(sh, ang, n) if min(r for a, r in P) > -1e-6]
                L2, _, par2 = summarize(E2, f'leg {name}, section normal to {"Y" if n == (0, 1, 0) else "X"} (flats normal to Z at r = A/F/2)')
                out += L2
                rec['flat_parallel'] = par2
            res[pn][name] = rec
    txt = '\n'.join(out) + '\n'
    os.makedirs(os.path.join(HERE, '..', 'evidence'), exist_ok=True)
    open(os.path.join(HERE, '..', 'evidence', 'pilot_sections.txt'), 'w', encoding='utf-8').write(txt)
    json.dump(res, open(os.path.join(HERE, '..', 'evidence', 'pilot_sections.json'), 'w', encoding='utf-8'), indent=1)
    print(txt)


if __name__ == '__main__':
    main()
