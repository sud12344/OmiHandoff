import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import omi_paths as P    # portable paths (2026-09-25)
_WORK = P.COVERAGE_WORK; _os.makedirs(_WORK, exist_ok=True); _HERE = _os.path.dirname(_os.path.abspath(__file__))
import openpyxl, glob, os, re, collections, json
from openpyxl.styles import Font, PatternFill, Alignment
R = P.ROOT
res = json.load(open(os.path.join(_WORK, 'res.json')))
need = {}
for line in open(os.path.join(_HERE, 'need_compact.txt')):
    k, v = line.strip().split('=')
    kind, dash = k.split('|')
    for pn in v.split(','): need[pn] = (kind, dash)
# OMiSKU -> PartNo from review tables
def load(f):
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True); ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows[:6]) if any(isinstance(x, str) and ('DataStatus' in x or '@' in x) for x in r if x))
    hdr = [str(x) if x is not None else '' for x in rows[hi]]
    ci = lambda k: next((i for i, h in enumerate(hdr) if k in h), None)
    out = []
    for r in rows[hi+1:]:
        if not r or not r[0]: continue
        g = lambda k: (r[ci(k)] if ci(k) is not None and ci(k) < len(r) else None)
        out.append(dict(cfg=str(r[0]).strip(), sku=g('OMiSKU'), part=g('PartNo')))
    return out
pn_of = {}
for f in glob.glob(f'{R}/04_DESIGN_TABLES/DesignTable_*.xlsx'):
    t = os.path.basename(f)[12:-5]
    if t.endswith('_SW2') or t == '6400_v2': continue
    for x in load(f):
        if x['sku']: pn_of.setdefault(str(x['sku']).strip(), str(x['part'] or x['cfg']).strip())
NWO = {'6801', '6801L', '6801LL', '6802', '6803', '6804', '6805', '6806', '6807', '6901', '6902', '4601', '4603'}
G = collections.OrderedDict([
 ('A1', ('Built - master in 11_MASTERS', 'done')),
 ('A2', ('Built earlier - 2404 / 6400 masters (files not in 11_MASTERS)', 'done (copy the two master files into 11_MASTERS)')),
 ('B',  ('Macro ready - waiting for you to run it', 'you: run the macros already in 03_SCRIPTS')),
 ('C1', ('Macro ready - batch 11 (new masters 1501, 6502)', 'you: run Build_1501 / Build_6502')),
 ('C2', ('Macro ready - batch 11 extra sizes for a built master (re-run)', 'you: re-run Build_5405 / 6401 / 6405')),
 ('D1', ('Needs a Brennan STEP - female JIC swivel size', 'Brennan 6500-XX-XX-FG, one per swivel size')),
 ('D2', ('Needs a Brennan STEP - female NPSM swivel size', 'Brennan 1404-XX-XX, one per NPSM size (1501-1503 also need an NPSM elbow leg - my work)')),
 ('D3', ('Needs a Brennan STEP - female JIC port size', 'Brennan 2406, one per female size')),
 ('D4', ('Needs a Brennan STEP - female ORB port size', 'Brennan 6404 / 6410, one per female size')),
 ('D5', ('Needs a Brennan STEP - code 61 flange size', 'Brennan 1700-16-16, 1700-20-20, 1700-32-32')),
 ('D6', ('Needs Brennan STEPs - adjustable ORB stud (nut/washer) sizes + a new module', 'Brennan 6801-XX-XX-NWO-FG, one per ORB size (have -14)')),
 ('D7', ('Needs one specific item (see note)', 'see the note on each row')),
 ('E',  ('Needs your decision', 'see the note on each row')),
 ('F1', ('Missing - Air-Way lists only the non-forged part (OMi sells -FG)', 'decision (use the non-forged dims) or Brennan -FG dimensions')),
 ('F2', ('Missing - OMi part not in Air-Way', 'a second dimensional source (Brennan catalog page or STEP)')),
 ('F3', ('Missing - no Air-Way page for the whole series', 'a dimensional source for the series')),
 ('F4', ('Missing - Air-Way misprint or conflict with the MS standard', 'correction / decision per row')),
 ('F5', ('Missing - Air-Way cell blank / other', 'see the note on each row')),
 ('X',  ('Out of scope - kits', 'none')),
])
rows = []
for s, r, c, st, t, cm in res:
    pn = pn_of.get(s, s); note = ''
    if st == 'BUILT': g = 'A1'; note = f'master {t}'
    elif st == 'BUILT-WB': g = 'A2'; note = f'master {t}'
    elif st == 'MACRO': g = 'B'; note = f'Build_{t}_MASTER.bas'
    elif st == 'OUT-KIT': g = 'X'
    elif st == 'DATA-NO-MACRO':
        if pn in need:
            kind, d = need[pn]
            g = {'JICSW': 'D1', 'NPSMSW': 'D2', 'JICF': 'D3', 'ORBF': 'D4', 'FLG61': 'D5'}[kind]
            note = {'JICSW': f'swivel -{d}: Brennan 6500-{d}-{d}-FG', 'NPSMSW': f'NPSM swivel -{d}: Brennan 1404-{d}-{d}',
                    'JICF': f'female JIC -{d}: a Brennan 2406-{d}-xx', 'ORBF': f'female ORB -{d}: a Brennan 6404/6410 with a -{d} female port',
                    'FLG61': f'flange -{d}: Brennan 1700-{d}-{d}'}[kind]
        elif t == '3051': g = 'D7'; note = 'Air-Way 3051 prints one leg length N and the hex W: which leg N measures must be read off the Air-Way drawing (or a Brennan 3051 STEP)'
        elif t == '5503' and s != '5503-06-06-FG': g = 'F4'; note = 'Air-Way prints D (bore) 0.83-1.64 on the -FG rows, larger than the pipe itself - misprint, bore unknown'
        elif t in ('5503', '5505'): g = 'D7'; note = 'my work: 45 deg elbow with a pipe-thread leg on the angled arm (not written yet)'
        elif t == '6502':
            sw = re.findall(r'-(\d\d)', s)[1]
            if sw in ('04', '08'): g = 'C1'; note = '45 deg swivel elbow (batch 11d: Build_6502_MASTER.bas)'
            elif sw in ('12', '16'): g = 'D7'; note = 'the body corner would stick out beside the swivel neck at this size - needs a Brennan 6502-12-12-FG STEP'
            else: g = 'D1'; note = f'swivel -{sw}: Brennan 6500-{sw}-{sw}-FG'
        elif t in ('1501', '1502', '1503'):
            sw = re.findall(r'-(\d\d)', s)[1]
            if sw == '08' and t == '1501': g = 'C1'; note = 'NPSM swivel elbow, swivel -08 (batch 11: Build_1501_MASTER.bas)'
            elif sw == '08' and s == '1503-08-08-FG': g = 'D7'; note = 'body checked on the Brennan 1503-08-08-FG STEP - needs a pipe-thread helper for the 45 deg leg (my work)'
            elif sw == '08': g = 'D7'; note = 'the body corner would stick out beside the swivel neck at this size - needs a Brennan 1503-12-08-FG STEP'
            else: g = 'D2'; note = f'NPSM swivel -{sw}: Brennan 1404-{sw}-{sw} + NPSM elbow leg (my work)'
        elif t in NWO: g = 'D6'; note = 'adjustable ORB stud + locknut' + (' + NPSM swivel' if t in ('6901', '6902') else ' + hose-barb leg' if t in ('4601', '4603') else '')
        elif t == '5405': g = 'C2'; note = 'Air-Way bore is larger than the port drill: bore stops at the port bottom (assumption) - batch 11 update, re-run 5405'
        elif s == '6405-32-24-O': g = 'F4'; note = 'Air-Way prints the bore D3 as 2.38 - larger than the whole ORB -32 end (groove root 2.381) - misprint'
        elif s in ('6401-32-32-O', '6405-32-20-O', '6405-32-32-O'): g = 'C2'; note = 'ORB -32 groove now measured (Brennan 6400-32-32-O) - batch 11 update, re-run ' + t
        elif s in ('6405-14-12-O', '6408-14-O'): g = 'D7'; note = 'fixed ORB -14 groove unmeasured: Brennan 6400-14-14-O'
        elif s == '6405-24-16-O': g = 'F4'; note = 'Air-Way port depth 1.14 >= length 1.00 - OMi to confirm'
        elif t in ('2404L', '6400L', '2501L'): g = 'D7'; note = 'fold into the base master (your yes, 2026-09-25) - needs one Brennan STEP to see where the extra length goes: ' + {'2404L': '2404-L-08-08', '6400L': '6400-L-08-08-O', '2501L': '2501-L-06-04-FG'}[t]
        elif t in ('2701', '2702'): g = 'E'; note = '2701/2702 -06/-10/-12: Air-Way collar dia equals the hex flats - model without a collar step?' if t == '2701' else 'Air-Way row looks like a -16 row (flagged) - confirm'
        elif t == '2404_FINAL': g = 'D7'; note = (cm or 'counterbore depth / NPTF end length unsourced')[:90]
        elif t == '0319': g = 'D7'; note = 'tube sleeve: needs the sleeve standard (MS20819) or a Brennan 0319 STEP per size (Air-Way gives only L and OD)'
        elif t == '4501': g = 'D7'; note = 'hose-barb elbow leg (my work)'
        else: g = 'D7'; note = cm[:90]
    elif st == 'MISSING':
        cml = cm.lower()
        if 'skeleton' in cml or 'no dimensional source' in cml or 'needs a dimensional source' in cml: g = 'F3'
        elif 'unpl' in cml: g = 'E'; note = 'OMi plated part = Air-Way UNPL (unplated) listing? The 0403 master already has these sizes'
        elif 'near' in cml and '-fg' in cml: g = 'F1'
        elif 'printed' in cml or 'conflict' in cml: g = 'F4'; note = cm[:100]
        elif 'orb groove' in cml and '-32-' in s + '-': g = 'D7'; note = 'ORB -32 groove now measured - my work: regenerate the hand-built 6400 master with the current generator (then your re-run)'
        elif 'orb groove' in cml: g = 'D7'; note = 'fixed ORB -14 groove unmeasured: Brennan 6400-14-14-O'
        elif 'male-orb -32 groove' in cml: g = 'D4'; note = 'female ORB -' + re.findall(r'-(\d\d)', s)[1] + ' port: a Brennan 6404/6410 with that female port (-32 male end now measured)'
        elif t == '0304': g = 'F2'; note = 'OMi 0304-C-xx is a JIC CAP nut (OMi: "04 JIC Cap Nut"), not the Air-Way 0304 standard nut - needs a cap source (Brennan 0304-C STEPs or AN929) + the female JIC port per size'
        elif 'female-jic union' in cml: g = 'D3'; note = '6900 female JIC union: a Brennan 6900 STEP per size'
        elif 'no row' in cml or 'omi-only' in cml or 'not in air-way' in cml: g = 'F2'
        else: g = 'F5'; note = cm[:100]
    else: g = 'F5'; note = st
    rows.append((s, c, r, t, g, G[g][0], note))
cnt = collections.Counter(x[4] for x in rows)
for k in G: print(f'{k:3} {cnt.get(k, 0):5}  {G[k][0]}')
print('TOTAL', sum(cnt.values()))
json.dump(rows, open(os.path.join(_WORK, 'cov_rows.json'), 'w'))
