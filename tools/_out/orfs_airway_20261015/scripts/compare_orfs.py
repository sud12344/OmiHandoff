"""compare_orfs.py (2026-10-15): OMi FS (ORFS) parts - Air-Way dimensions, checked against the Brennan ORFS catalog.

User 2026-10-15: "use airway dimensions, check brennan too". Read-only on every source; writes only into this task folder:
  ../compare_orfs.json   every OMi FS part: Air-Way row, Brennan row, thread check, dimension check, proposed DataStatus + reason
  ../compare_orfs.csv    the same, one line per part
Rules applied (CLAUDE.md, PROJECT_STATUS s5):
  - DIMENSIONS from Air-Way. Brennan only CHECKS (2026-10-08 "You cannot use Brennan data as your own"): Air-Way = Brennan on every
    mapped cell -> VERIFIED (two independent sources); Air-Way only (no Brennan row / column) -> ASSUMED; a real difference -> built to
    Air-Way, ASSUMED, Brennan's value in $COMMENT (PROJECT_STATUS s6 convention, never averaged); no Air-Way row -> MISSING
    (Brennan-only rows stay MISSING).
  - rounding-only differences are equal (user 2026-09-25); the rule is match_ORFS.py's cmp_num (copied below unchanged).
  - -FG (forged) OMi parts are NOT built from Air-Way's non-forged rows (user decision, PROJECT_STATUS s5) -> MISSING ('FG rule'); the
    non-forged Air-Way vs Brennan -FG comparison is reported for information only.
  - pairs are made by connection type (OMi Side n Connection Type / Brennan title / Air-Way thread columns), not by series number:
    OMi FS6402 (MFS x FJS) is NOT Air-Way FF6402 (MORB x FFSS = OMi FS6540); OMi FS6504 (FFSS x MJ) is Air-Way FF7504, not FF6504.
python -I compare_orfs.py"""
import csv, json, os, re, sys, collections
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import load

HERE = load.HERE

# ---------------------------------------------------------------- numbers: user rounding rule (copied from match_ORFS.py, 2026-10-01)
NUM_RE = re.compile(r"^\s*(?:(\d+)\s*[- ]\s*)?(\d+)\s*/\s*(\d+)\s*$")


def parse_num(s):
    if s is None:
        return None
    t = str(s).strip().replace('"', "")
    if t in ("", "NA", "N/A", "-"):
        return None
    m = re.fullmatch(r"(\d*)\.(\d+)|(\d+)", t)
    if m:
        if m.group(3) is not None:
            return Fraction(int(m.group(3))), 0
        return Fraction(Decimal(t)), len(m.group(2))
    m = NUM_RE.match(t)
    if m:
        whole = int(m.group(1) or 0)
        return whole + Fraction(int(m.group(2)), int(m.group(3))), None
    return None


def rnd(x, n, mode):
    return Decimal(x.numerator) / Decimal(x.denominator) if n is None else \
        (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1).scaleb(-n), rounding=mode)


def cmp_num(a, b):
    pa, pb = parse_num(a), parse_num(b)
    if pa is None or pb is None:
        return None
    (va, da), (vb, db) = pa, pb
    if va == vb:
        return "equal"
    decs = [d for d in (da, db) if d is not None]
    if not decs:
        return "different"
    n = min(decs)
    for mode in (ROUND_HALF_UP, ROUND_DOWN):
        if rnd(va, n, mode) == rnd(vb, n, mode):
            return "rounding_only"
    if da == db == n and abs(va - vb) == Fraction(1, 10 ** n):
        mid = (va + vb) / 2
        if (mid * 64).denominator == 1:
            return "rounding_only"
    return "different"


SUFFIX = re.compile(r"\b(UNEF|UNF|UNS|UNC|UN|NPTF|NPFT|NPT|NPSM|BSPP|BSPT|BSP)\b")


def norm_thread(s):
    if s is None:
        return None
    t = str(s).upper().strip()
    if not t:
        return None
    t = SUFFIX.sub("", t).strip()
    t = re.sub(r"\s*-\s*", "-", t)
    t = re.sub(r"(\d)\s+(\d)", r"\1-\2", t)
    return t.strip()


# ---------------------------------------------------------------- part numbers -> dash tuple (+ flags)
def dashes(pn):
    s = re.sub(r'\s+', ' ', str(pn).upper()).strip().split(' ')[0]      # Air-Way appends descriptions after a space
    s = re.sub(r'^(FF|FS)', '', s)
    s = re.sub(r'^(0?\d{3,4}(-[A-Z]{1,2})?)', '', s)                    # series code incl. -C / -L / -LN
    return tuple(int(x) for x in re.findall(r'-(\d{1,2})(?=-|$|[A-Z])', s))


# ---------------------------------------------------------------- the pairs (OMi series -> Air-Way series, Brennan series, maps)
# dims: (Air-Way column, Brennan column, meaning). threads: (Air-Way column, Brennan column). aw_filter: which Air-Way rows count.
PAIRS = {
    'FS0306': dict(aw='FF306', br=['FS0306'], dims=[('h2', 'TT WIDTH', 'nut width'), ('S4', 'B HEX', 'hex')], threads=[('d UN/UNF-2B', 'A THREAD')]),
    'FS0318': dict(aw='FF318', br=['FS0318'], dims=[('h', 'Q WIDTH', 'nut length'), ('S', 'B HEX', 'hex')], threads=[('d UN/UNF-2B', 'A THREAD')]),
    'FS0319': dict(aw='FF319', br=['FS0319'], dims=[('L', 'F LGTH', 'sleeve length'), ('d8', 'A O.D.', 'sleeve OD')], threads=[]),
    'FS2403': dict(aw='FF2403', br=['FS2403'], dims=[('L6', 'FF LGTH', 'overall length'), ('S1', 'H HEX', 'hex')],
                   threads=[('d(1) UN/UNF-2A', 'A1 THREAD'), ('d(2) UN/UNF-2A', 'A2 THREAD')]),
    'FS2404': dict(aw='FF2404', br=['FS2404'], dims=[('L', 'FF LGTH', 'overall length'), ('S1', 'H HEX', 'hex')],
                   threads=[('d UN/UNF-2A', 'A THREAD'), ('A NPTF', 'B THREAD')]),
    'FS2406': dict(aw='FF2407', br=['FS2406'], dims=[('L36', 'L LGTH', 'overall length'), ('NUT S (FF318)', 'C HEX', 'nut hex')],
                   threads=[('d UN/UNF-2A', 'A2 THREAD')],
                   note='Air-Way FF2407 "Reducing Adapter" = OMi FFS x MFS tube end reducer; Air-Way sells it with an FF318 nut ("W/FF318-n NUT"), '
                        'so the nut hex is the Air-Way FF318 tube-nut hex S of the female dash (no hex column in FF2407)'),
    'FS2408': dict(aw='FF2408', br=['FS2408'], dims=[('L24', 'L LGTH', 'overall length'), ('S1', 'H HEX', 'hex')], threads=[('d UN/UNF-2A', 'A THREAD')],
                   note='Air-Way FF2408 rows are "-O-W/HOLE" (column W/HOLE = a hole dia) - check that OMi\'s plug is the same'),
    'FS2700': dict(aw='FF2700', br=['FS2700'], dims=[('L15', 'GG LGTH', 'overall length'), ('S4 (1)', 'B HEX', 'hex')],
                   threads=[('d(1) UN/UNF-2A', 'A1 THREAD'), ('d(2) UN/UNF-2A', 'A2 THREAD')], aw_ln=False),
    'FS2700-LN': dict(aw='FF2700', br=['FS2700'], dims=[('L15', 'GG LGTH', 'overall length'), ('S4 (1)', 'B HEX', 'hex')],
                      threads=[('d(1) UN/UNF-2A', 'A1 THREAD'), ('d(2) UN/UNF-2A', 'A2 THREAD')], aw_ln=True,
                      note='bulkhead union sold with its lock nut (Air-Way -LN-O rows); Brennan prints the bare union (FS2700) - the lock nut is FS0306'),
    'FS6400': dict(aw='FF6400', br=['FS6400-O'], dims=[('L8', 'L LGTH', 'overall length'), ('S5', 'H HEX', 'hex')],
                   threads=[('d UN/UNF-2A', 'A THREAD'), ('n UN/UNF-2A', 'B THREAD')]),
    'FS6400-L': dict(aw='FF6400-L', br=['FS6400-L-O'], dims=[('L32', 'L LGTH', 'overall length'), ('S5', 'H HEX', 'hex')],
                     threads=[('d UN/UNF-2A', 'A THREAD'), ('n UN/UNF-2A', 'B THREAD')], note='Air-Way prints styles A and B per size'),
    'FS6403': dict(aw='FF7403', br=['FS6403'], dims=[('L41', 'L LGTH', 'overall length'), ('S1', 'H HEX', 'hex')],
                   threads=[('d UN/UNF-2A', 'A THREAD'), ('B UN/UNF-2A', 'B THREAD')], note='OMi FS6403 (MFS x MJ) = Air-Way FF7403 (male ORFS x 37 deg male JIC)'),
    'FS6504': dict(aw='FF7504', br=['FS6504'], dims=[('L40', 'L LGTH', 'overall length')],
                   threads=[('d UN/UNF-2B', 'A1 THREAD'), ('B UN/UNF-2A', 'A2 THREAD')],
                   note='OMi FS6504 (FFSS x MJ) = Air-Way FF7504 (37 deg male JIC x female ORFS swivel), NOT Air-Way FF6504 (MFS x FFSS union). '
                        'Air-Way C2 / S do not match Brennan C HEX / H HEX - their meaning needs the Air-Way drawing; hexes not compared'),
    'FS6505': dict(aw='FF6505', br=['FS6505'], dims=[('L16', 'L LGTH', 'overall length'), ('S', 'C HEX', 'nut hex'), ('S1', 'H HEX', 'body hex'),
                                                     ('D2', 'A HOLE', 'pipe-end bore'), ('d19', 'B HOLE', 'swivel-end bore')],
                   threads=[('A NPTF', 'A THREAD'), ('d UN/UNF-2B', 'B THREAD')]),
    'FS6540': dict(aw='FF6402', br=['FS6540-O'], dims=[('L34', 'L LGTH', 'overall length'), ('S', 'C HEX', 'nut hex'), ('S5', 'H HEX', 'body hex')],
                   threads=[('d UN/UNF-2B', 'A THREAD'), ('n UN/UNF-2A', 'B MORB')],
                   note='OMi FS6540 (FFSS x MORB) = Air-Way FF6402 "Straight Thread / Female ORFS Swivel Adapter"'),
    'FS6565': dict(aw='FF6565', br=['FS6565'], dims=[('L45', 'L LGTH', 'overall length'), ('S(1)', 'C HEX', 'nut hex'), ('S1', 'H HEX', 'body hex')],
                   threads=[('d(1) UN/UNF-2A', 'A THREAD'), ('d(2) UN/UNF-2B', 'B THREAD')],
                   note='Air-Way calls it "Male ORFS / Female Double Swivel Union" but prints two nut hexes S(1) / S(2) (= Brennan FFSS-FFSS)'),
    'FS4000': dict(aw='AWs40', br=[], dims=[], threads=[], aw_prefix='FF4000-',
                   note='Buna O-rings for SAE J1453 face-seal ends (Air-Way s40 FF4000-n; FF4001 = Viton, FF4002 = Hi-Temp are other compounds): '
                        'I.D. / W, the 4000 O-ring model type'),
}
NO_AIRWAY = {
    'FS0304-C': 'Air-Way FF304-C is a plain cap NUT; OMi sells the cap assembly insert & nut (staked) - only the hex agrees with Brennan FS0304-C',
    'FS1700': 'no Air-Way ORFS flange series (Brennan: Flange catalog only)', 'FS1800': 'no Air-Way ORFS flange series (Brennan: Flange catalog only)',
    'FS2405': 'no Air-Way FS x female pipe series (Brennan FS2405 only)',
    'FS6402': 'no Air-Way MFS x female JIC swivel series (Air-Way FF6402 is MORB x FFSS = OMi FS6540; Brennan FS6402 only)',
}
FORGED_AW = {'FS2500': 'FF2500', 'FS2501': 'FF2501', 'FS2503': 'FF2503', 'FS2603': 'FF2603', 'FS2650': 'FF2650', 'FS2701': 'FF2701', 'FS2701-LN': 'FF2701',
             'FS2702': 'FF2702', 'FS2702-LN': 'FF2702', 'FS2703': 'FF2703', 'FS2703-LN': 'FF2703', 'FS2704': 'FF2704', 'FS2704-LN': 'FF2704',
             'FS6500': 'FF6500', 'FS6502': 'FF6502', 'FS6600': 'FF6600', 'FS6602': 'FF6602', 'FS6801': 'FF6801', 'FS6801-L': 'FF6801-L',
             'FS6802': 'FF6802', 'FS6803': 'FF6803', 'FS6804': 'FF6804', 'FS6809': 'FF6809'}
# forged parts (user 2026-10-15, ORFS only): the Air-Way NON-forged row of the same size is used ONLY where Brennan's catalog row of the
# forged part prints the same value in EVERY compared cell -> VERIFIED; otherwise MISSING. Column pairs by drawing meaning (Brennan
# letter vs Air-Way letter on the same view): legs in side order, JJ FLATS = forged body flats vs Air-Way S2 / S3 body hex, C HEX =
# swivel nut / locknut hex. The -LN kits (bulkhead + lock nut) use the bare forged fitting's Brennan row (Brennan prints no -LN rows).
FORGED_BR = {'FS2500': 'FS2500-FG', 'FS2501': 'FS2501-FG', 'FS2503': 'FS2503-FG', 'FS2603': 'FS2603-FG', 'FS2650': 'FS2650-FG',
             'FS2701': 'FS2701-FG', 'FS2701-LN': 'FS2701-FG', 'FS2702': 'FS2702-FG', 'FS2702-LN': 'FS2702-FG', 'FS2703': 'FS2703-FG',
             'FS2703-LN': 'FS2703-FG', 'FS2704': 'FS2704-FG', 'FS2704-LN': 'FS2704-FG', 'FS6500': 'FS6500-FG', 'FS6502': 'FS6502-FG',
             'FS6600': 'FS6600-FG', 'FS6602': 'FS6602-FG', 'FS6801': 'FS6801-NWO-FG', 'FS6801-L': 'FS6801-L-NWO-FG',
             'FS6802': 'FS6802-NWO-FG', 'FS6803': 'FS6803-NWO-FG', 'FS6804': 'FS6804-NWO-FG', 'FS6809': 'FS6809-NWO-FG'}
FORGED_PAIRS = {   # Brennan forged series: (Air-Way plain series, [(Brennan col, Air-Way col)])
    'FS2500-FG': ('FF2500', [('M1 LGTH', 'L7 (1)'), ('M2 LGTH', 'L7 (2)'), ('JJ FLATS', 'S2')]),
    'FS2501-FG': ('FF2501', [('M LGTH', 'L7'), ('N LGTH', 'N'), ('JJ FLATS', 'S2')]),
    'FS2503-FG': ('FF2503', [('M LGTH', 'L12'), ('N LGTH', 'N2'), ('JJ FLATS', 'S2')]),
    'FS2603-FG': ('FF2603', [('M1 LGTH', 'L7 (1)'), ('M2 LGTH', 'L7 (2)'), ('M3 LGTH', 'L7 (3)'), ('JJ FLATS', 'S2')]),
    'FS2650-FG': ('FF2650', [('M1 LGTH', 'L7 (1)'), ('M2 LGTH', 'L7 (2)'), ('M3 LGTH', 'L7 (3)'), ('M4 LGTH', 'L7 (4)'), ('JJ FLATS', 'S2')]),
    'FS2701-FG': ('FF2701', [('R LGTH', 'L16'), ('S LGTH', 'L17'), ('JJ FLATS', 'S2')]),
    'FS2702-FG': ('FF2702', [('P LGTH', 'L12'), ('ZZ LGTH', 'L18'), ('JJ FLATS', 'S2')]),
    'FS2703-FG': ('FF2703', [('R1 LGTH', 'L16 (1)'), ('R2 LGTH', 'L16 (2)'), ('S LGTH', 'L7'), ('JJ FLATS', 'S2')]),
    'FS2704-FG': ('FF2704', [('R1 LGTH', 'L16 (1)'), ('S LGTH', 'L17'), ('R2 LGTH', 'L16 (3)'), ('JJ FLATS', 'S2')]),
    'FS6500-FG': ('FF6500', [('M LGTH', 'L7'), ('AAA LGTH', 'L21'), ('C HEX', 'S'), ('JJ FLATS', 'S2')]),
    'FS6502-FG': ('FF6502', [('L1 LGTH', 'L7'), ('L2 LGTH', 'L52'), ('C HEX', 'S'), ('JJ FLATS', 'S2')]),
    'FS6600-FG': ('FF6600', [('M1 LGTH', 'L7 (1)'), ('M2 LGTH', 'L7 (2)'), ('AAA LGTH', 'L21'), ('C HEX', 'S'), ('JJ FLATS', 'S2')]),
    'FS6602-FG': ('FF6602', [('M1 LGTH', 'L7 (1)'), ('AAA LGTH', 'L21'), ('M2 LGTH', 'L7'), ('C HEX', 'S'), ('JJ FLATS', 'S2')]),
    'FS6801-NWO-FG': ('FF6801', [('M LGTH', 'L7'), ('N LGTH', 'L10'), ('C HEX', 'S3'), ('JJ FLATS', 'S2')]),
    'FS6801-L-NWO-FG': ('FF6801-L', [('M LGTH', 'L7'), ('N LGTH', 'L50'), ('C HEX', 'S3'), ('JJ FLATS', 'S2')]),
    'FS6802-NWO-FG': ('FF6802', [('M LGTH', 'L12'), ('N LGTH', 'L13'), ('C HEX', 'S3'), ('JJ FLATS', 'S2')]),
    'FS6803-NWO-FG': ('FF6803', [('M1 LGTH', 'L7 (1)'), ('M2 LGTH', 'L7 (2)'), ('N LGTH', 'L10'), ('C HEX', 'S3'), ('JJ FLATS', 'S2')]),
    'FS6804-NWO-FG': ('FF6804', [('M1 LGTH', 'L7 (1)'), ('N LGTH', 'L10'), ('M2 LGTH', 'L7 (3)'), ('C HEX', 'S3'), ('JJ FLATS', 'S2')]),
    'FS6809-NWO-FG': ('FF6809', [('AAA LGTH', 'L21'), ('N LGTH', 'L10'), ('JJ FLATS', 'S2')]),
}
FG_USER = ('[user 2026-10-15: "Yes - use Air-Way\'s sizes for the 121 forged ORFS parts where Brennan\'s forged row matches on every cell '
           '(VERIFIED); the rest stay MISSING."]')


def forged_check(pn, ser, k, A, bser):
    """status of one forged OMi FS part under the 2026-10-15 rule (dict for rec.update)"""
    bs = FORGED_BR.get(ser)
    if bs is None:
        return dict(status='MISSING', reason='forged (-FG): no Brennan forged table paired and no Air-Way non-forged series - stays MISSING')
    ac, pairs = FORGED_PAIRS[bs]
    hit = [(t, r) for t, r in bser.get(bs, []) if dashes(r['pn']) == k]
    aw_all = [r for r in A[ac]['rows'] if dashes(r['pn']) == k]
    ln = '-LN' in ser
    aw_rows = [r for r in aw_all if ('-LN' in r['pn'].upper()) == ln] or aw_all
    base = dict(airway_series=ac, airway_nonforged=[r['pn'] for r in aw_rows])
    if not hit:
        return dict(base, status='MISSING', reason=f'forged (-FG): Brennan {bs} prints no row of this size - stays MISSING' +
                    (f' (Air-Way plain {aw_rows[0]["pn"]} exists)' if aw_rows else ''))
    t, br = hit[0]
    base.update(brennan_rows=[f'{br["pn"]} ({t["table_id"]})'], brennan_values=br['values'], brennan_page=t['page'])
    if not aw_rows:
        return dict(base, status='MISSING', reason=f'forged (-FG): Brennan p{t["page"]} prints it but Air-Way has no non-forged row - Brennan-only stays MISSING')
    aw = aw_rows[0]
    cells = [dict(meaning=bc, airway=f'{acol}={aw["values"].get(acol)}', brennan=f'{bc}={br["values"].get(bc)}',
                  result=cmp_num(aw['values'].get(acol), br['values'].get(bc))) for bc, acol in pairs]
    base.update(airway_rows=[aw['pn']], cells=cells)
    if all(c['result'] in ('equal', 'rounding_only') for c in cells):
        return dict(base, status='VERIFIED', forged_rule='Air-Way plain = Brennan forged on every cell', airway_values=dict(aw['values']),
                    reason=f'forged (-FG): Air-Way non-forged {aw["pn"]} = Brennan forged {br["pn"]} p{t["page"]} on every compared cell ('
                           + ', '.join(f'{c["brennan"].split("=")[0]} ~ {c["airway"].split("=")[0]}' for c in cells) + f') {FG_USER}')
    bad = [c for c in cells if c['result'] not in ('equal', 'rounding_only')]
    return dict(base, status='MISSING', reason='forged (-FG): Air-Way non-forged row differs from Brennan forged on ' +
                '; '.join(f'{c["brennan"]} vs Air-Way {c["airway"]}' for c in bad) + ' - stays MISSING (user 2026-10-15)')


WEB_SRC = None
# 2026-10-16, from the ORFS model-type plan (tools/_out/orfs_modeltype_20261016/PLAN.md section 8):
HOLD = {   # conflicting sources -> MISSING, values not used (CLAUDE.md: never pick between conflicting sources - ask the user)
    'FS0319-24': 'HELD: Air-Way contradicts itself - FF319-24 sleeve OD d8 1.71, but Air-Way\'s own FF2407 reducer collar d8 for the -24 '
                 'female end is 2.00 (FS2406-24-20); Brennan FS0319-24 A O.D. 1.910. Conflicting sources - for the user (plan D5)',
}
CAP = {    # VERIFIED needs the key dimensions compared; these pairs compare too little -> at most ASSUMED
    'FS6504': 'only the overall length L40 is compared: Air-Way FF7504 "S" (0.40 ... 1.46) cannot be a nut hex and C2 equals Brennan\'s '
              'H HEX only at -08, so no hex is checked (plan D3, Q-FS-NUT) - ASSUMED, not VERIFIED',
}
NOTES = {  # printed as Air-Way prints it, noted
    'FS2704-LN-04-04-04-FG': 'Air-Way prints the lock-nut hex S4 ".081" on FF2704-4-4-4-LN-O (0.81 on FF2704-4-4-4-O): kept as printed; '
                             'the lock nut is not modelled (plan D2)',
}


def website_list():
    """OMi website ORFS SKUs: the published two-pass list if it exists, else the single pass A list of 2026-10-16 (this folder)"""
    global WEB_SRC
    for p, label in ((os.path.join(load.ROOT, '07_RAW_EXTRACTS', 'omi_feed', 'omi_skus_orfs.txt'), 'OMi website ORFS list (two passes, omi_skus_orfs.txt)'),
                     (os.path.join(HERE, 'omi_orfs_website_passA.txt'), 'OMi website ORFS collection, ONE crawl pass (pass A 2026-10-16; 385 = the published count)')):
        if os.path.exists(p):
            WEB_SRC = label
            return {s.strip() for s in open(p, encoding='utf-8') if s.strip() and not s.startswith('#')}
    return None


def main():
    A, B, O = load.airway(), load.brennan(), load.omi_file()
    web = website_list()
    bser = collections.defaultdict(list)
    for t in B:
        for r in t['rows']:
            bser[t['series']].append((t, r))
    out = []
    for pn, o in sorted(O.items()):
        if not pn.startswith('FS'):
            continue
        ser = str(o.get('Series'))
        rec = dict(omi_pn=pn, series=ser, description=o.get('Part Description'), on_website=(None if web is None else pn in web),
                   omi_row=o['_row'], dashes=list(dashes(pn)))
        k = dashes(pn)
        if ser in PAIRS:
            P = PAIRS[ser]
            rec['airway_series'] = P['aw']
            aw_rows = [r for r in A[P['aw']]['rows'] if dashes(r['pn']) == k and r['pn'].upper().startswith(P.get('aw_prefix', ''))]
            if 'aw_ln' in P:
                aw_rows = [r for r in aw_rows if ('-LN' in r['pn'].upper()) == P['aw_ln']] or aw_rows
            br_rows = [(t, r) for s in P['br'] for t, r in bser.get(s, []) if dashes(r['pn']) == k]
            rec['airway_rows'] = [r['pn'] for r in aw_rows]
            rec['brennan_rows'] = [f'{r["pn"]} ({t["table_id"]})' for t, r in br_rows]
            if not aw_rows:
                rec.update(status='MISSING', reason=f'no Air-Way {P["aw"]} row of this size' + (' (Brennan prints it: Brennan-only stays MISSING)' if br_rows else ''))
                out.append(rec); continue
            aw = dict(aw_rows[0]['values'])
            if ser == 'FS2406':           # nut hex = Air-Way FF318 tube nut of the female (first) dash
                nut = [r for r in A['FF318']['rows'] if dashes(r['pn']) == (k[0],)]
                aw['NUT S (FF318)'] = nut[0]['values'].get('S') if nut else None
            rec['airway_values'] = aw
            if len(aw_rows) > 1:
                rec['airway_alternatives'] = [dict(pn=r['pn'], values=r['values']) for r in aw_rows[1:]]
            if not br_rows:
                rec.update(status='ASSUMED', reason=f'Air-Way {P["aw"]} only (no Brennan catalog row of this size)')
                out.append(rec); continue
            t, br = br_rows[0]
            rec['brennan_values'] = br['values']; rec['brennan_page'] = t['page']
            thr = []
            for ac, bc in P['threads']:
                a_, b_ = norm_thread(aw.get(ac)), norm_thread(br['values'].get(bc))
                thr.append(dict(airway=f'{ac}={aw.get(ac)}', brennan=f'{bc}={br["values"].get(bc)}', same=(a_ == b_) if a_ and b_ else None))
            rec['threads'] = thr
            cells = []
            for ac, bc, meaning in P['dims']:
                r_ = cmp_num(aw.get(ac), br['values'].get(bc))
                cells.append(dict(meaning=meaning, airway=f'{ac}={aw.get(ac)}', brennan=f'{bc}={br["values"].get(bc)}', result=r_))
            rec['cells'] = cells
            # a thread that differs is noted, not blocking: on every case seen the Air-Way callout is a typo (9/19-18, 13/16-12,
            # 11/16-18 for ORFS -04 / -08 / -06), and the model takes its threads from the end library (Q-TRANSFER-ENDLIB), not this cell
            bad_thr = [x for x in thr if x['same'] is False]
            if bad_thr:
                rec['thread_note'] = 'thread printed differently (Air-Way vs Brennan): ' + '; '.join(f'{x["airway"]} vs {x["brennan"]}' for x in bad_thr)
            diff = [c for c in cells if c['result'] == 'different']
            cmpd = [c for c in cells if c['result'] in ('equal', 'rounding_only')]
            if diff:
                # PROJECT_STATUS s6 convention: "Differences between the dimension source and Brennan are built to the dimension source
                # and written in $COMMENT" (6801 precedent, batch 13b) -> Air-Way values, ASSUMED, Brennan's value in the reason / $COMMENT
                gap = max(abs(float(parse_num(c['airway'].split('=', 1)[1])[0]) - float(parse_num(c['brennan'].split('=', 1)[1])[0])) for c in diff)
                rec.update(status='ASSUMED', conflict_max_in=round(gap, 4), conflict_size=('small' if gap <= 0.0201 else 'large'),
                           reason=f'Air-Way {P["aw"]} (built to Air-Way); Brennan p{t["page"]} DIFFERS ({"<= 0.02 in" if gap <= 0.0201 else f"up to {gap:.3f} in"}): ' +
                                  '; '.join(f'{c["meaning"]} {c["airway"]} vs Brennan {c["brennan"]}' for c in diff))
            elif cmpd and len(cmpd) == len(P['dims']):
                rec.update(status='VERIFIED', reason=f'Air-Way {P["aw"]} = Brennan p{t["page"]} on ' + ', '.join(c['meaning'] for c in cmpd) + ' (rounding-only differences count as equal)')
            else:
                rec.update(status='ASSUMED', reason=f'Air-Way {P["aw"]}; Brennan p{t["page"]} agrees on {len(cmpd)} of {len(P["dims"])} compared cells')
        elif ser in NO_AIRWAY:
            br_rows = [(t, r) for t in B for r in t['rows'] if load.core(r['pn']).replace('-ASY', '') == load.core(pn).replace('-ASY', '')]
            rec.update(status='MISSING', reason=NO_AIRWAY[ser] + (' (Brennan prints it: Brennan-only stays MISSING)' if br_rows else ''))
        elif pn.endswith('-FG') or ser in FORGED_AW or ser in ('FS1704', 'FS1804', 'FS2502', 'FS2601', 'FS6503', 'FS7202'):
            rec.update(forged_check(pn, ser, k, A, bser))
        else:
            rec.update(status='MISSING', reason='no Air-Way series paired yet')
        out.append(rec)
    for rec in out:                                  # 2026-10-16 fixes from the ORFS model-type plan (HOLD / CAP / NOTES above)
        pn, ser = rec['omi_pn'], rec['series']
        if pn in HOLD:
            rec['held_values'] = rec.pop('airway_values', None)
            rec.update(status='MISSING', reason=HOLD[pn] + ' | was: ' + rec.get('reason', ''))
            rec.pop('conflict_size', None)
        elif ser in CAP and rec.get('status') == 'VERIFIED':
            rec.update(status='ASSUMED', reason=rec['reason'] + ' | ' + CAP[ser])
        if pn in NOTES:
            rec['extra_note'] = NOTES[pn]
    json.dump(out, open(os.path.join(HERE, 'compare_orfs.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
    with open(os.path.join(HERE, 'compare_orfs.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['OMi part', 'series', 'on OMi website', 'status', 'reason', 'Air-Way row', 'Brennan row', 'description'])
        for r in out:
            w.writerow([r['omi_pn'], r['series'], r['on_website'], r['status'], r['reason'], '; '.join(r.get('airway_rows') or r.get('airway_nonforged') or []),
                        '; '.join(r.get('brennan_rows') or []), r['description']])
    c = collections.Counter((r['series'], r['status']) for r in out)
    tot = collections.Counter(r['status'] for r in out)
    for s in sorted({r['series'] for r in out}):
        print(f'{s:<12}', {st: c[(s, st)] for st in ('VERIFIED', 'ASSUMED', 'MISSING') if c[(s, st)]})
    print('TOTAL', dict(tot), '| website list:', 'pending' if web is None else f'{len(web)} SKUs ({WEB_SRC})')
    if web is not None:
        on = [r for r in out if r['on_website']]
        print('ON THE WEBSITE', len(on), dict(collections.Counter(r['status'] for r in on)), '| website SKUs not in OMi parts file:',
              sorted(s for s in web if s not in O))
        json.dump(dict(source=WEB_SRC, n=len(web)), open(os.path.join(HERE, 'website_source.json'), 'w', encoding='utf-8'))


if __name__ == '__main__':
    main()
