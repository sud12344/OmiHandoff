"""decode_families.py (2026-10-21): map each Brennan CAD family's record letter codes to measured geometry, using the Brennan STEPs on
disk (09_STEP_FILES) whose records we have (../pc_results_repo_steps.csv + ../cache.json).

Per STEP, every feature value is measured (inches):
  CYL_D   cylinder diameter              TOR_R  torus major radius (bend)        TOR_r  torus minor radius x2 (tube dia)
  CONE_A  cone half-angle (deg)          GAP    distance between two parallel planes (lengths, hex A/F, flange thickness)
  AX_PL   distance from a cylinder axis to a plane parallel to it (elbow / tee leg lengths, hex A/F about the axis)
  AX_AX   distance between two parallel cylinder axes             BOX  bounding-box extents
Each numeric record code is then matched (|code - feature| <= TOL, inch values; also code in mm / 25.4) and the kinds that match are
counted over all STEPs of the family. A code is DECODED when one kind matches on every STEP of the family that has the code, and the
match is not trivially ambiguous (it is reported with how many features of that kind gave the value). One STEP only -> "1 of 1"
(weaker: tell apart by the next download). Non-geometric codes (DN, MAT, FONTSIZE, WEIGHT, PITCH, thread texts, ...) are skipped.
Writes decode_<family>.txt per family and family_codes.csv (family, code, kind, matched_on, of, example values)."""
import os, sys, re, csv, json, math, collections, itertools
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Torus
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

H = os.path.dirname(os.path.abspath(__file__)); PC = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(PC, '..', '..', '..'))
TOL = 0.0015
SKIP = re.compile(r'^(DN|OD|MAT\d?|MAT1|MATALG|FONTSIZE|WEIGHT|PITCH|PLATING|WBVAR|TT[LR]?|THD\d?|ATXT|BTXT|A\d?|B\d?|A\dOD|A2OD1|B1|FL1|'
                  r'GX|LINEID|EXT)$')
MM = 25.4


def load(path):
    r = STEPControl_Reader()
    if r.ReadFile(path) != IFSelect_RetDone:
        raise RuntimeError('cannot read ' + path)
    r.TransferRoots(); return r.OneShape()


def unit(v):
    n = math.sqrt(sum(c * c for c in v)); v = [c / n for c in v]
    # sign-normalise: first non-zero component positive
    for c in v:
        if abs(c) > 1e-9:
            return tuple(round(x * (1 if c > 0 else -1), 6) for x in v)
    return tuple(v)


def features(path):
    s = load(path)
    planes, cyls, out = [], [], collections.defaultdict(set)
    ex = TopExp_Explorer(s, TopAbs_FACE)
    while ex.More():
        a = BRepAdaptor_Surface((getattr(TopoDS, "Face", None) or TopoDS.Face_s)(ex.Current()))   # OCP 8 (Face) and 7.x (Face_s)
        t = a.GetType()
        if t == GeomAbs_Plane:
            pl = a.Plane(); n = pl.Axis().Direction(); p = pl.Location()
            u = unit((n.X(), n.Y(), n.Z())); d = (u[0] * p.X() + u[1] * p.Y() + u[2] * p.Z()) / MM
            planes.append((u, d))
        elif t == GeomAbs_Cylinder:
            c = a.Cylinder(); ax = c.Axis(); dr = ax.Direction(); lo = ax.Location()
            out['CYL_D'].add(round(2 * c.Radius() / MM, 4))
            cyls.append((unit((dr.X(), dr.Y(), dr.Z())), (lo.X() / MM, lo.Y() / MM, lo.Z() / MM)))
        elif t == GeomAbs_Cone:
            out['CONE_A'].add(round(math.degrees(a.Cone().SemiAngle()), 2))
        elif t == GeomAbs_Torus:
            tor = a.Torus(); out['TOR_R'].add(round(tor.MajorRadius() / MM, 4)); out['TOR_r'].add(round(2 * tor.MinorRadius() / MM, 4))
        ex.Next()
    byn = collections.defaultdict(set)
    for u, d in planes:
        byn[u].add(round(d, 5))
    for u, ds in byn.items():
        for d1, d2 in itertools.combinations(sorted(ds), 2):
            out['GAP'].add(round(abs(d2 - d1), 4))
    cyl_u = {}
    for u, p in cyls:
        cyl_u.setdefault((u, tuple(round(x, 4) for x in p)), (u, p))
    for (u, p) in cyl_u.values():
        for n, ds in byn.items():
            if abs(sum(a * b for a, b in zip(u, n))) < 1e-4:          # axis parallel to the plane
                pd = sum(a * b for a, b in zip(n, p))
                for d in ds:
                    out['AX_PL'].add(round(abs(d - pd), 4))
    axes = list(cyl_u.values())
    for (u1, p1), (u2, p2) in itertools.combinations(axes, 2):
        if all(abs(a - b) < 1e-4 for a, b in zip(u1, u2)):
            w = [b - a for a, b in zip(p1, p2)]; cr = sum(a * b for a, b in zip(w, u1))
            dist = math.sqrt(max(0.0, sum(x * x for x in w) - cr * cr))
            if dist > 1e-4:
                out['AX_AX'].add(round(dist, 4))
    b = Bnd_Box(); BRepBndLib.Add_s(s, b)
    lo, hi = b.CornerMin(), b.CornerMax()
    for v in (hi.X() - lo.X(), hi.Y() - lo.Y(), hi.Z() - lo.Z()):
        out['BOX'].add(round(v / MM, 4))
    return out


def record(kv_text):
    kv = {}
    for item in kv_text.split(';'):
        if '=' in item:
            k, v = item.split('=', 1); kv[k.strip()] = v.strip()
    return kv


def num(v):
    try:
        return float(v)
    except ValueError:
        return None


rows = [r for r in csv.DictReader(open(os.path.join(PC, 'pc_results_repo_steps.csv'), encoding='utf-8')) if r['found'] == 'yes']
fams = collections.defaultdict(list)
for r in rows:
    fams[r['family']].append(r)
only = set(sys.argv[1:])
summary = []
for fam, rs in sorted(fams.items()):
    if only and fam.split('/')[-1] not in only:
        continue
    per_code = collections.defaultdict(lambda: collections.defaultdict(int))   # code -> kind -> STEPs matched
    seen = collections.Counter(); vals = collections.defaultdict(list); log = []
    null = collections.defaultdict(collections.Counter)
    for r in rs:
        path = os.path.join(ROOT, '09_STEP_FILES', f"BRENNAN_{r['part']}.stp")
        try:
            F = features(path)
        except Exception as e:
            log.append(f"{r['part']}: {e}"); continue
        kv = record(r['params'])
        log.append(f"== {r['part']} (record {r['pn']})")
        for k, v in kv.items():
            x = num(v)
            if SKIP.match(k) or x is None or x <= 0:
                continue
            seen[k] += 1; vals[k].append(v)
            hits = []
            for scale, tag in ((1.0, ''), (1 / MM, ' (mm)')):      # mm only when no inch feature matches
                for kind, fs in F.items():
                    if any(abs(f - x * scale) <= (0.05 if kind == 'CONE_A' else TOL) for f in fs):
                        hits.append(kind + tag)
                if hits:
                    break
            for h in set(hits):
                per_code[k][h] += 1
            # chance test: the same value shifted by +0.037 / -0.029 in - a kind that also 'matches' those is not evidence
            for sh in (0.037, -0.029):
                for kind, fs in F.items():
                    if kind != 'CONE_A' and any(abs(f - (x + sh)) <= TOL for f in fs):
                        null[k][kind] += 1
            log.append(f"  {k:8} {v:>10}  -> {', '.join(sorted(set(hits))) or '-'}")
    lines = [f'# {fam}: {len(rs)} STEP(s): ' + ' '.join(r['part'] for r in rs), '']
    for k in sorted(seen):
        kinds = sorted(per_code[k].items(), key=lambda t: -t[1])
        best = [f'{kd} {n}/{seen[k]} (chance {null[k][kd.replace(" (mm)", "")]}/{2 * seen[k]})' for kd, n in kinds]
        # a kind counts only if it matched on every STEP and the shifted values hit it on at most a quarter of the tries
        full = [kd for kd, n in kinds if n == seen[k] and null[k][kd.replace(' (mm)', '')] <= 0.5 * seen[k]]
        weak = [kd for kd, n in kinds if n == seen[k]] and not full
        status = 'DECODED' if full else ('AMBIGUOUS' if weak else ('PARTIAL' if kinds else 'NO MATCH'))
        lines.append(f'{k:8} {status:8} {", ".join(best) or "-"}   values: {", ".join(vals[k][:4])}')
        summary.append(dict(family=fam, code=k, status=status, kinds=' | '.join(full) if full else ' | '.join(best),
                            steps=seen[k], values=' '.join(vals[k][:6])))
    open(os.path.join(H, 'decode_' + fam.split('/')[-1] + '.txt'), 'w').write('\n'.join(lines + [''] + log) + '\n')
    print(fam, len(rs), 'STEPs:', collections.Counter(s['status'] for s in summary if s['family'] == fam), flush=True)
with open(os.path.join(H, 'family_codes.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['family', 'code', 'status', 'kinds', 'steps', 'values']); w.writeheader(); w.writerows(summary)
