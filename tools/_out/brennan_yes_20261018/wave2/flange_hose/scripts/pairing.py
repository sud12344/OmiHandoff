"""pairing.py - letter-mapping evidence for the flange_hose group: every row of the 9 review tables that has an Air-Way (or OMi) value
AND a Brennan catalog row of the same part number (or the same size with/without -FG / -61- / NWO spelling), cell by cell.
Writes ../evidence/pairing.txt and ../evidence/pairing.json."""
import os, re, json, collections
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
BASE = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\base_root\04_DESIGN_TABLES')
CAT = os.path.join(ROOT, r'tools\_out\brennan_catalog_20261001\catalog_verified.json')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'evidence')
os.makedirs(OUT, exist_ok=True)

# table column <- catalog header, per table (the mapping under test)
MAP = {
    '1700': {'L28@DRIVE': 'L (in.)', 'CHEX@HEX': 'A/F (in.)'},
    '1703': {'M2@DRIVE': 'L1 (in.)', 'N3@DRIVE': 'L2 (in.)', 'CHEX@HEX': 'A/F (in.)'},
    '1704': {'M@DRIVE': 'L1 (in.)', 'N2@DRIVE': 'L2 (in.)', 'Y@HEX': 'A/F (in.)'},
    '4501': {'L4@DRIVE': 'L LGTH', 'N@DRIVE': 'N LGTH', 'Y@HEX': 'Y FLATS', 'D1@BORE': 'A2 DRILL', 'D1@BORE ': 'B1 DRILL'},
    '4503': {'L5@DRIVE': 'L LGTH', 'N2@DRIVE': 'N LGTH', 'CHEX@HEX': 'Y FLATS', 'D1@BORE': 'A2 DRILL', 'D1@BORE ': 'B1 DRILL'},
    '4601': {'L4@DRIVE': 'L LGTH', 'M7@DRIVE': 'M LGTH', 'C4HEX@HEX': 'C HEX', 'Y@HEX': 'Y FLATS', 'D@BORE': 'B2 DRILL', 'D@BORE ': 'B1 DRILL'},
    '4603': {'L5@DRIVE': 'L LGTH', 'M8@DRIVE': 'M LGTH', 'C4HEX@HEX': 'C HEX', 'CHEX@HEX': 'Y FLATS', 'D@BORE': 'B2 DRILL', 'D@BORE ': 'B1 DRILL'},
}


def cat_rows():
    d = json.load(open(CAT, encoding='utf-8'))
    out = collections.defaultdict(list)
    for t in d['tables']:
        for r in t['rows']:
            out[r['pn']].append((t, r))
    return out


def dashes(s):
    return tuple(int(x) for x in re.findall(r'-(\d\d)(?=-|$| )', ' ' + str(s).replace(' ', '-') + ' '))


def fnum(s):
    try:
        return float(str(s).strip())
    except ValueError:
        return None


def main():
    C = cat_rows()
    res, lines = {}, []
    for t, mp in MAP.items():
        ws = openpyxl.load_workbook(os.path.join(BASE, f'DesignTable_{t}.xlsx'), data_only=True).worksheets[0]
        hdr = [c.value for c in ws[2]]
        stats = collections.defaultdict(lambda: [0, 0, 0, []])   # equal(<=0.006), rounding (<=0.015), differ, list
        lines.append(f'===== {t}  mapping {mp}')
        for row in ws.iter_rows(min_row=3, values_only=True):
            if not row[0]:
                continue
            rec = dict(zip(hdr, row))
            if all(rec.get(k.strip()) in (None, '') for k in mp):
                continue
            pn = str(row[0])
            fg = 'FG' in pn
            ds = dashes(pn.replace('-61-', '-'))
            root = pn[:4]
            # candidate catalog part numbers: same dashes, forged and plain spellings
            cands = []
            for k, lst in C.items():
                if not k.startswith(root + '-'):
                    continue
                if dashes(k) != ds:
                    continue
                cands.extend((k, tt, rr) for tt, rr in lst)
            for k, tt, rr in cands:
                kfg = 'FG' in k
                same = 'same-forging' if kfg == fg else ('AW-plain-vs-Brennan-FG' if kfg else 'AW-FG-vs-Brennan-plain')
                cmp = []
                for col, ch in mp.items():
                    a = rec.get(col.strip())
                    b = fnum(rr['values'].get(ch, ''))
                    if a in (None, '') or b is None:
                        continue
                    dlt = round(float(a) - b, 4)
                    cls = 'EQ' if abs(dlt) <= 0.006 else ('RND' if abs(dlt) <= 0.015 else 'DIFF')
                    st = stats[(col, ch, same)]
                    st[0 if cls == 'EQ' else 1 if cls == 'RND' else 2] += 1
                    st[3].append((pn, k, a, b))
                    cmp.append(f'{col.strip()}={a} vs {ch}={b} [{cls}]')
                lines.append(f'  {pn:22s} <-> {k:22s} {tt["table_id"]:16s} ({same}) ' + '; '.join(cmp))
        lines.append(f'  --- summary {t} (EQ <=0.006 / RND <=0.015 / DIFF)')
        res[t] = {}
        for (col, ch, same), (e, r_, dd, lst) in sorted(stats.items()):
            lines.append(f'      {col.strip():12s} <- {ch:10s} {same:24s} EQ {e:3d}  RND {r_:3d}  DIFF {dd:3d}')
            res[t][f'{col.strip()}<-{ch}|{same}'] = dict(EQ=e, RND=r_, DIFF=dd, rows=lst)
    open(os.path.join(OUT, 'pairing.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    json.dump(res, open(os.path.join(OUT, 'pairing.json'), 'w', encoding='utf-8'), indent=1)
    print('\n'.join(l for l in lines if 'summary' in l or l.startswith('      ') or l.startswith('=====')))


if __name__ == '__main__':
    main()
