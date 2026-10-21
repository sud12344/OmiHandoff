"""Batch 19 paperwork (2026-10-21): QA_Log rows #179-#181 + Topologies notes in the MasterData workbook.
(Copied from tools/_out/ship_20261019/paperwork/update_masterdata_16.py; changed: data block qa_data_19.py, expected last QA #172,
backup paths, NOTES limited to roots that have a Topologies row, STATUS computed: new masters TABLED / SKELETON-MISSING -> BUILT.)

Same method as the earlier batches (the workbook is written by openpyxl 3.1.5 - see docProps/app.xml): load with openpyxl,
append QA_Log rows in the style of row #158, prepend a dated note to the Topologies 'Status note' (newest first, ' | '
separator, as the 2026-09-25 notes), save to a scratch copy, re-load and prove that ONLY the intended cells changed and that
sheets / sizes / freeze panes / filters / widths / comments / validations are as before, then copy over the live file.

Usage: python update_masterdata.py            (dry: writes paperwork/MasterData_new.xlsx + the check report only)
       python update_masterdata.py --apply    (same, then replaces the live workbook if the live sha256 is still the
                                               backed-up one)
Backups (made before, by paperwork/backup.py): tools/_out/batch18_20261020/old_files/paperwork/01_MASTER_DATA/ and
_to_delete/superseded_20261020/batch18_replaced/paperwork/01_MASTER_DATA/ (MANIFEST_paperwork.txt).
"""
import hashlib, os, shutil, sys, copy
import openpyxl

R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
LIVE = os.path.join(R, '01_MASTER_DATA', 'OMi_Fitting_Library_MasterData_v1.xlsx')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'MasterData_new.xlsx')
REPORT = os.path.join(HERE, 'masterdata_check.txt')
SHA_BEFORE = '6a43ad3058b4dab7bb8ad1ff76e4e628aa755e96fc0e40cfad9b8b5e3a384e8a'
DATE = '2026-10-21'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qa_data_19.py'), encoding='utf-8').read())


def snapshot(wb):
    s = {}
    meta = {'sheets': wb.sheetnames, 'defined_names': sorted(str(k) for k in wb.defined_names.keys())}
    for ws in wb.worksheets:
        cells = {}
        comments = {}
        styles = {}
        for row in ws.iter_rows():
            for c in row:
                if c.value is not None:
                    cells[c.coordinate] = c.value
                if c.comment is not None:
                    comments[c.coordinate] = (c.comment.text, c.comment.author)
                if c.has_style:
                    styles[c.coordinate] = (c.font.name, c.font.sz, c.font.b, c.font.i, str(c.font.color.rgb if c.font.color else None),
                                            c.fill.fill_type, str(c.fill.fgColor.rgb), c.alignment.wrap_text,
                                            c.alignment.vertical, c.alignment.horizontal, c.number_format,
                                            c.border.left.style, c.border.bottom.style)
        s[ws.title] = dict(cells=cells, comments=comments, styles=styles, max_row=ws.max_row, max_col=ws.max_column,
                           freeze=str(ws.freeze_panes), filter=str(ws.auto_filter.ref),
                           widths={k: v.width for k, v in ws.column_dimensions.items()},
                           heights={k: v.height for k, v in ws.row_dimensions.items() if v.height is not None},
                           merged=sorted(str(m) for m in ws.merged_cells.ranges),
                           dv=len(ws.data_validations.dataValidation), cf=len(ws.conditional_formatting),
                           tables=sorted(ws.tables.keys()))
    return meta, s


def main(apply):
    out = []
    p = out.append
    live_sha = sha(LIVE)
    p(f'live workbook sha256 {live_sha}')
    assert live_sha == SHA_BEFORE, 'the live workbook changed since the backup - re-read it first'
    meta0, s0 = snapshot(openpyxl.load_workbook(LIVE))   # separate object: iterating creates empty rows in memory
    wb = openpyxl.load_workbook(LIVE)                     # the object that is edited and saved (touch only what changes)

    # ---- QA_Log
    ws = wb['QA_Log']
    last = ws.max_row
    last_id = ws.cell(last, 1).value
    p(f'QA_Log last row {last}, last # {last_id!r}')
    assert str(last_id) == '178', last_id
    expected = {}
    for i, (num, check, method, result, sev, action) in enumerate(QA):
        assert int(num) == int(last_id) + 1 + i
        r = last + 1 + i
        vals = [num, DATE, check, method, result, sev, action]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c)
            cell.value = v
            cell._style = copy.copy(ws.cell(last, c)._style)
            expected[('QA_Log', cell.coordinate)] = v
    # ---- Topologies
    wt = wb['Topologies']
    hdr = [wt.cell(1, c).value for c in range(1, wt.max_column + 1)]
    rows_t = {str(wt.cell(rr, 1).value): rr for rr in range(2, wt.max_row + 1) if wt.cell(rr, 1).value is not None}
    for t in [t for t in NOTES if t not in rows_t]:
        p(f'no Topologies row for {t}: note not written')
        del NOTES[t]
    ci_s = hdr.index('Master status') + 1
    for t in NOTES:
        if 'NEW master' in NOTES[t] and wt.cell(rows_t[t], ci_s).value in ('TABLED', 'SKELETON-MISSING', 'TABLED - master not built'):
            STATUS[t] = (wt.cell(rows_t[t], ci_s).value, 'BUILT')
    ci_note = hdr.index('Status note') + 1
    ci_stat = hdr.index('Master status') + 1
    done = set()
    for rr in range(2, wt.max_row + 1):
        v0 = wt.cell(rr, 1).value
        t = str(v0) if v0 is not None else None
        if t in NOTES:
            cell = wt.cell(rr, ci_note)
            old = cell.value or ''
            assert 'BATCH 19 ' not in old, t
            new = NOTES[t] + (' | ' + old if old else '')
            cell.value = new
            expected[('Topologies', cell.coordinate)] = new
            if t in STATUS:
                sc = wt.cell(rr, ci_stat)
                assert sc.value == STATUS[t][0], (t, sc.value)
                sc.value = STATUS[t][1]
                expected[('Topologies', sc.coordinate)] = STATUS[t][1]
            done.add(t)
    assert done == set(NOTES), set(NOTES) - done
    p(f'Topologies notes prepended: {len(done)} roots: {" ".join(sorted(done))}; master status changed: {STATUS}')
    wb.save(OUT)

    # ---- re-load and compare
    wb2 = openpyxl.load_workbook(OUT)
    meta1, s1 = snapshot(wb2)
    p(f'sheets before {meta0["sheets"]}')
    p(f'sheets after  {meta1["sheets"]}')
    assert meta0 == meta1, 'sheet list / defined names changed'
    ok = True
    for name in meta0['sheets']:
        a, b = s0[name], s1[name]
        keys = set(a['cells']) | set(b['cells'])
        diff = [k for k in keys if a['cells'].get(k) != b['cells'].get(k)]
        intended = [k for k in diff if (name, k) in expected and b['cells'].get(k) == expected[(name, k)]]
        other = sorted(set(diff) - set(intended))
        missing = [k for (n, k) in expected if n == name and k not in diff]
        sdiff = [k for k in set(a['styles']) | set(b['styles']) if a['styles'].get(k) != b['styles'].get(k)
                 and (name, k) not in expected]
        same_meta = all(a[x] == b[x] for x in ('freeze', 'filter', 'widths', 'heights', 'merged', 'dv', 'cf', 'tables',
                                                 'comments', 'max_col'))
        line = (f'{name:18} rows {a["max_row"]:4} -> {b["max_row"]:4}  cols {a["max_col"]:3} -> {b["max_col"]:3}  '
                f'changed cells {len(diff):3} (intended {len(intended)}, OTHER {len(other)}, intended-not-written '
                f'{len(missing)})  style diffs outside new cells {len(sdiff)}  freeze/filter/widths/heights/merged/'
                f'dv/cf/comments same: {same_meta}  comments {len(a["comments"])} dv {a["dv"]}')
        p(line)
        if other or missing or sdiff or not same_meta:
            ok = False
            p(f'   OTHER {other[:20]} missing {missing[:20]} style {sdiff[:20]}')
    qa_new_rows = s1['QA_Log']['max_row'] - s0['QA_Log']['max_row']
    p(f'QA_Log rows added: {qa_new_rows} (#179-#181 expected 3)')
    assert qa_new_rows == len(QA)
    for name in meta0['sheets']:
        if name not in ('QA_Log',):
            assert s0[name]['max_row'] == s1[name]['max_row'], name
    import zipfile
    za, zb = zipfile.ZipFile(LIVE), zipfile.ZipFile(OUT)
    p(f'zip members identical list/order: {za.namelist() == zb.namelist()}')
    raw = [n for n in za.namelist() if za.read(n) != zb.read(n)]
    p(f'raw XML parts that differ from the live file: {raw}')
    allowed = {'docProps/core.xml', 'xl/worksheets/sheet4.xml', 'xl/worksheets/sheet14.xml'}   # modified date, Topologies, QA_Log
    if za.namelist() != zb.namelist() or set(raw) - allowed:
        ok = False
    p('RESULT ' + ('OK - only the intended cells changed' if ok else 'PROBLEM'))
    p(f'new workbook sha256 {sha(OUT)}')
    if apply and ok:
        assert sha(LIVE) == SHA_BEFORE, 'live workbook changed during the run'
        shutil.copyfile(OUT, LIVE)
        p(f'APPLIED: live workbook replaced, sha256 now {sha(LIVE)}')
    open(REPORT, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('\n'.join(out))
    return ok


if __name__ == '__main__':
    sys.exit(0 if main('--apply' in sys.argv) else 1)
