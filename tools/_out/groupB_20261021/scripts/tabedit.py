"""tabedit.py (group B, 2026-10-21): small helper for the staged review-table edits. Every cell write is logged to CHANGES.csv
(table, part, column, old, new, source). Only EMPTY cells are filled with Brennan values (fill_brennan); other edits name their rule."""
import os, csv, openpyxl

H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
STAGE = os.path.join(A, 'stage', '04_DESIGN_TABLES'); STAGE_FS = os.path.join(A, 'stage', 'orfs_tables')
PC = os.path.join(ROOT, 'tools', '_out', 'partcommunity_20261021', 'pc_final.csv')
LOG = os.path.join(A, 'CHANGES.csv')
TODAY = '2026-10-21'
BR_NOTE = 'user 2026-10-21 "yes you can use them following my rule"'

_rec = None
def record(part):
    """the Brennan CAD parameter record of an OMi part (pc_final.csv), {code: value} with numbers as float"""
    global _rec
    if _rec is None:
        _rec = {}
        for r in csv.DictReader(open(PC, encoding='utf-8')):
            if r['found'] != 'yes': continue
            d = {}
            for kv in r['params'].split(';'):
                if '=' not in kv: continue
                k, v = kv.split('=', 1)
                try: d[k] = float(v)
                except ValueError: d[k] = v
            d['_pn'] = r['pn']; d['_family'] = r['family']; _rec[r['part']] = d
    return _rec.get(part)


class Table:
    def __init__(self, root, fs=False):
        self.root = root; self.path = os.path.join(STAGE_FS if fs else STAGE, f'DesignTable_{root}.xlsx')
        self.wb = openpyxl.load_workbook(self.path); self.ws = self.wb.worksheets[0]
        self.hdr = [c.value for c in self.ws[2]]
        self.rows = {}
        for i in range(3, self.ws.max_row + 1):
            k = self.ws.cell(i, 1).value
            if k: self.rows.setdefault(k, i)
        self.log = []; self._brennan = {}

    def col(self, name, create=False):
        if name in self.hdr: return self.hdr.index(name) + 1
        if not create: raise KeyError(f'{self.root}: no column {name}')
        # a new dimension column goes before the first $ column (generators read by name)
        j = next(i for i, h in enumerate(self.hdr) if h and str(h).startswith('$'))
        self.ws.insert_cols(j + 1); self.ws.cell(2, j + 1).value = name; self.hdr.insert(j, name)
        self.log.append((self.root, '(header)', name, '', 'new column', 'group B: column the SPEC reads'))
        return j + 1

    def get(self, part, name):
        return self.ws.cell(self.rows[part], self.col(name)).value

    def set(self, part, name, value, src, create=False):
        c = self.col(name, create); i = self.rows[part]; old = self.ws.cell(i, c).value
        if old == value: return False
        self.ws.cell(i, c).value = value; self.log.append((self.root, part, name, old, value, src)); return True

    def note(self, part, name, text, front=False):
        """append (or prepend) a text to a text column"""
        old = self.get(part, name) or ''
        if text in old: return
        new = (text + (' ' if old else '') + old) if front else (old + (' | ' if old else '') + text)
        self.set(part, name, new, 'group B note')

    def fill_brennan(self, part, name, value, code):
        """an EMPTY cell <- Brennan record value (Air-Way first: never overwrites); marks the row BRENNAN"""
        cur = self.get(part, name)
        if cur is not None: return False
        self.set(part, name, value, f'Brennan CAD record {part} {code} ({BR_NOTE})')
        self._brennan.setdefault(part, []).append((name, code))
        return True

    def finish_brennan(self):
        for part, cc in self._brennan.items():
            if not cc or part not in self.rows: continue
            self.set(part, '$PRP@DimSource', 'BRENNAN', 'group B: row takes Brennan cells', create=True)
            self.note(part, '$PRP@AxialSource', f'[BRENNAN-CAD {TODAY} group B: ' + ', '.join(n for n, _ in cc) + ']', front=True)
            rec = record(part)
            self.note(part, '$COMMENT', f'Brennan CAD record {rec["_pn"] if rec else part} (PARTcommunity / CADENAS, group B 2026-10-21: '
                      + ', '.join(f'{n}={c}' for n, c in cc) + f'; {BR_NOTE})')
        self._brennan = {}

    def save(self):
        self.finish_brennan()
        self.wb.save(self.path)
        new = not os.path.exists(LOG)
        with open(LOG, 'a', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            if new: w.writerow(['table', 'part', 'column', 'old', 'new', 'source'])
            w.writerows(self.log)
        self.log = []
