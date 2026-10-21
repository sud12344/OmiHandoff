#!/usr/bin/env python
"""Parse the Brennan catalog PDFs (TFA, Flange, Hosetail, ORFS) into one JSON of dimension tables.

    python tools/catalog/parse_brennan_catalog.py                  # all four catalogs
    python tools/catalog/parse_brennan_catalog.py --catalog TFA    # one catalog
    python tools/catalog/parse_brennan_catalog.py --png TFA:3,5,57 # also render pages (200 dpi) for a visual check

Input : 07_RAW_EXTRACTS/brennan_catalogs/*.pdf (omi_paths.RAW), text layer read with pymupdf.
Output (default tools/_out/brennan_catalog_20261001/parsed, override with --out):
  catalog_parsed.json          sources (sha256), tables (columns + rows, printed strings), index entries, checks
  catalog_parsed_summary.txt   per catalog / page: tables, rows, warnings; cross-checks
  catalog_<CAT>.csv            one per catalog, LONG format: one line per (part number, column)

How it works (no plain text order is trusted - every token is placed by its coordinates):
  * words come from page.get_text('rawdict') (characters with boxes and fonts), split at spaces; white text
    (invisible dot leaders) is dropped.
  * a table starts at a header cell 'PART NO.' (TFA / Flange / ORFS, GothamXNarrow-BoldItalic 7 pt) or 'Item'
    (Hosetail, Gotham-Bold 9 pt blue). Header words on the anchor line and on the following header lines (multi-
    line headers such as 'B1 / TUBE / O.D.') are merged into columns by x overlap. Several anchors on one line =
    side-by-side tables.
  * a value token belongs to the column whose header x-range it starts in (boundary = header x0 minus half the gap
    to the previous header, 2.5 .. 6 pt), so thread callouts with spaces ('1 1/4-11 1/2') stay one cell and cells
    that merge in the text layer ('1-1/4-11-1/2 1.250') are split again.
  * a row = a line whose first column holds a part number (bold in TFA/Flange/ORFS). A line without a part number
    directly under a row is merged into it (warning). A table ends at the next table header / heading /
    'Continued...' / footer in its x-range.
  * the heading (series number + title) is the nearest heading above the header in the same x-range; a header with
    no heading above it is a continuation of the previous table in reading order (left column, then right column,
    then next page): continued_from_page / continued_from_table, series and title inherited, header compared.
Values are never rounded or normalised; header keys are the printed header text (lines joined with a space).
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # tools/
import omi_paths  # noqa: E402

import pymupdf  # noqa: E402

CATALOGS = {  # key -> (file name, layout style)
    'TFA': ('TFA Catalog.pdf', 'gx'),
    'FLANGE': ('Flange Catalog.pdf', 'gx'),
    'HOSETAIL': ('Hosetail Catalog.pdf', 'gt'),
    'ORFS': ('ORFS Catalog.pdf', 'gx'),
}
PDF_DIR = os.path.join(omi_paths.RAW, 'brennan_catalogs')
DEFAULT_OUT = os.path.join(omi_paths.OUT, 'brennan_catalog_20261001', 'parsed')

BLUE = 0x6ca3
GRAY_HT = 0x939598  # Hosetail sub-heading grey
WHITE = 0xffffff
FOOTER_Y = 750.0     # words starting below this are page footer (page number, catalog name); Hosetail rows reach 746
UNLABELED = '(no header)'  # key of a printed column that has no header text (e.g. 'Steel' / 'Steel Forged')

PN_RE = re.compile(r'^[A-Z0-9][A-Za-z0-9.\-/]*\d[A-Za-z0-9.\-/]*$')
ANCHOR_RE = re.compile(r'^(PART\s*NO\.?|Item)$', re.I)
LETTER_RE = re.compile(r'^([A-Za-z]{1,3}\d{0,2}|\d{1,2})(\*?)(?:\s+(.+))?$')
SINGLE_LETTER_RE = re.compile(r'^([A-Za-z]\d{0,2}|\d{1,2})(\*?)$')


# ----------------------------------------------------------------------------------------------- words
def page_words(page):
    """all visible horizontal words with font info, split at spaces and at wide gaps between characters"""
    words = []
    rd = page.get_text('rawdict')
    for b in rd['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            dx, dy = ln['dir']
            if abs(dx - 1) > 1e-3 or abs(dy) > 1e-3:
                continue  # rotated text (none in the tables)
            for s in ln['spans']:
                if s['color'] == WHITE:
                    continue
                size = s['size']
                cur = []

                def flush():
                    if cur:
                        words.append({
                            'text': ''.join(c['c'] for c in cur),
                            'x0': min(c['bbox'][0] for c in cur), 'x1': max(c['bbox'][2] for c in cur),
                            'y0': min(c['bbox'][1] for c in cur), 'y1': max(c['bbox'][3] for c in cur),
                            'base': cur[0]['origin'][1], 'font': s['font'], 'size': size,
                            'color': s['color']})
                        cur.clear()

                for ch in s['chars']:
                    if ch['c'].isspace():
                        flush()
                        continue
                    if cur and ch['bbox'][0] - cur[-1]['bbox'][2] > 0.5 * size:
                        flush()
                    cur.append(ch)
                flush()
    return words


def group_lines(words, tol=2.0):
    """cluster words into lines by baseline; returns list of (baseline, [words sorted by x])"""
    lines = []
    for w in sorted(words, key=lambda w: (w['base'], w['x0'])):
        if lines and abs(w['base'] - lines[-1][0]) <= tol:
            lines[-1][1].append(w)
        else:
            lines.append([w['base'], [w]])
    return [(b, sorted(ws, key=lambda w: w['x0'])) for b, ws in lines]


def cells_from_line(ws, gap_factor=0.55):
    """merge adjacent words of one line into cells (gap < gap_factor * font size)"""
    cells = []
    for w in ws:
        if cells and w['x0'] - cells[-1]['x1'] < gap_factor * w['size']:
            c = cells[-1]
            c['text'] += ' ' + w['text']
            c['x1'] = max(c['x1'], w['x1'])
            c['y0'] = min(c['y0'], w['y0'])
            c['y1'] = max(c['y1'], w['y1'])
            c['words'].append(w)
        else:
            cells.append({'text': w['text'], 'x0': w['x0'], 'x1': w['x1'], 'y0': w['y0'], 'y1': w['y1'],
                          'base': w['base'], 'size': w['size'], 'words': [w]})
    return cells


# ----------------------------------------------------------------------------------------------- styles
def is_header_word(w, style):
    if style == 'gx':
        return 'BoldItalic' in w['font'] and 6.5 <= w['size'] <= 7.6 and w['color'] in (0, BLUE)
    return w['font'].startswith('Gotham-Bold') and 8.5 <= w['size'] <= 9.6 and w['color'] == BLUE


def is_data_word(w, style):
    if w['color'] != 0 or not (6.5 <= w['size'] <= 7.6):
        return False
    if style == 'gx':
        return w['font'] in ('GothamXNarrow-Light', 'GothamXNarrow-Bold', 'GothamXNarrow-Book')
    return w['font'] in ('Gotham-Book', 'Gotham-Bold')


def is_pn_word(w, style):
    if style == 'gx':
        return w['font'] == 'GothamXNarrow-Bold' and w['color'] == 0 and 6.5 <= w['size'] <= 7.6
    return w['font'] == 'Gotham-Book' and w['color'] == 0 and 6.5 <= w['size'] <= 7.6


def is_big_heading_word(w):
    """series numbers and section titles (Bebas, >= 18 pt)"""
    return w['font'].startswith('BebasNeue') and 'Bold' in w['font'] and w['size'] >= 18 and w['color'] != WHITE


def is_title_word(w, style):
    return style == 'gx' and w['font'].startswith('BebasNeueBook') and w['size'] >= 11 and w['color'] == 0


def is_ht_name_word(w):
    return w['font'] in ('Gotham-Black', 'Gotham-Bold') and w['size'] >= 9.5 and w['color'] == 0


def is_ht_sub_word(w):
    return w['font'] in ('Gotham-Black', 'Gotham-Bold') and w['size'] >= 7.5 and w['color'] == GRAY_HT


def is_continued_word(w):
    return w['text'].lower().startswith('continued')


# ----------------------------------------------------------------------------------------------- headings
def find_headings(words, style):
    """series headings with their titles; also section headings (barriers). Each: dict(kind, series, title,
    x0, x1, y0, y1)"""
    heads = []
    big = [w for w in words if is_big_heading_word(w)]
    for base, ws in group_lines(big, tol=3.0):
        for c in cells_from_line(ws, gap_factor=0.9):
            kind = 'series' if re.search(r'\d', c['text']) else 'section'
            heads.append({'kind': kind, 'series': c['text'] if kind == 'series' else None,
                          'text': c['text'], 'title': None, 'x0': c['x0'], 'x1': c['x1'], 'xr': c['x1'],
                          'y0': c['y0'], 'y1': c['y1'], 'size': c['size']})
    if style == 'gx':
        tl = []
        for base, ws in group_lines([w for w in words if is_title_word(w, style)], tol=3.0):
            for c in cells_from_line(ws, gap_factor=0.9):
                tl.append(c)
        series = sorted([h for h in heads if h['kind'] == 'series'], key=lambda h: h['y0'])
        used = set()
        # pass 1: title on the same line, right of the number
        for h in series:
            best = None
            for i, t in enumerate(tl):
                if i in used:
                    continue
                if t['y1'] > h['y0'] and t['y0'] < h['y1'] and 0 <= t['x0'] - h['x1'] < 60:
                    if best is None or t['x0'] < tl[best]['x0']:
                        best = i
            if best is not None:
                h['title'] = tl[best]['text']
                h['title_y1'] = tl[best]['y1']
                h['xr'] = max(h['xr'], tl[best]['x1'])
                used.add(best)
        # pass 2: title below the number (Flange head connectors, port blocks), x-aligned
        for h in series:
            if h['title']:
                continue
            best = None
            for i, t in enumerate(tl):
                if i in used:
                    continue
                if 0 <= t['y0'] - h['y1'] < 45 and abs(t['x0'] - h['x0']) < 30:
                    if best is None or t['y0'] < tl[best]['y0']:
                        best = i
            if best is not None:
                h['title'] = tl[best]['text']
                h['title_y1'] = tl[best]['y1']
                h['xr'] = max(h['xr'], tl[best]['x1'])
                used.add(best)
        # wrapped titles: following title lines with the same x0, directly below
        for h in series:
            if not h['title']:
                continue
            for i, t in enumerate(tl):
                if i in used:
                    continue
                if 0 <= t['y0'] - h['title_y1'] < 6 and any(abs(t['x0'] - tt['x0']) < 3 for tt in tl
                                                              if tt['text'] in h['title']):
                    h['title'] += ' ' + t['text']
                    h['title_y1'] = t['y1']
                    used.add(i)
        for i, t in enumerate(tl):
            if i not in used:
                heads.append({'kind': 'orphan_title', 'series': None, 'text': t['text'], 'title': t['text'],
                              'x0': t['x0'], 'x1': t['x1'], 'xr': t['x1'], 'y0': t['y0'], 'y1': t['y1'],
                              'size': t['size']})
    else:  # Hosetail: black name line(s) + grey code / description line(s)
        name_lines = []
        for base, ws in group_lines([w for w in words if is_ht_name_word(w) or is_ht_sub_word(w)], tol=2.0):
            for c in cells_from_line(ws, gap_factor=0.9):
                c['grey'] = all(w['color'] == GRAY_HT for w in c['words'])
                name_lines.append(c)
        name_lines.sort(key=lambda c: (c['y0'], c['x0']))
        blocks = []
        for c in name_lines:
            blk = None
            for b in blocks:
                if abs(b['x0'] - c['x0']) < 4 and -4 <= c['y0'] - b['y1'] < 6 and not (b['lines'][-1]['grey'] and not c['grey']):
                    blk = b
                    break
            if blk is None:
                blocks.append({'x0': c['x0'], 'x1': c['x1'], 'y0': c['y0'], 'y1': c['y1'], 'lines': [c]})
            else:
                blk['lines'].append(c)
                blk['x1'] = max(blk['x1'], c['x1'])
                blk['y1'] = c['y1']
        for b in blocks:
            name = ' '.join(l['text'].strip() for l in b['lines'] if not l['grey'])
            subs = [l['text'].strip() for l in b['lines'] if l['grey']]
            if not name:
                continue
            code = subs[0] if subs and re.fullmatch(r'[A-Z0-9][A-Z0-9/\-]*', subs[0]) else None
            series = code or name
            title = name if code else ' / '.join([name] + subs)
            if code and len(subs) > 1:
                title += ' / ' + ' / '.join(subs[1:])
            heads.append({'kind': 'series', 'series': series, 'text': name, 'title': title,
                          'x0': b['x0'], 'x1': b['x1'], 'xr': b['x1'], 'y0': b['y0'], 'y1': b['y1'], 'size': 10})
    return heads


# ----------------------------------------------------------------------------------------------- header -> columns
def parse_header_key(key, style):
    """'B2 THREAD' -> ('B2', 'THREAD', ''), 'E* BORE' -> ('E', 'BORE', '*'), 'TUBE O.D.' -> (None, 'TUBE O.D.', '')"""
    if style != 'gx':
        return None, key, ''
    m = LETTER_RE.match(key)
    if m and m.group(3):
        return m.group(1), m.group(3), m.group(2)
    m = SINGLE_LETTER_RE.match(key)
    if m:
        return m.group(1), None, m.group(2)
    return None, key, ''


def build_tables_on_page(words, style, page_w):
    hdr_words = [w for w in words if is_header_word(w, style) and w['y0'] < FOOTER_Y]
    hdr_lines = []
    for base, ws in group_lines(hdr_words, tol=2.0):
        hdr_lines.append((base, cells_from_line(ws)))
    anchors = []
    for li, (base, cells) in enumerate(hdr_lines):
        for c in cells:
            if ANCHOR_RE.match(c['text'].strip()):
                anchors.append({'line': li, 'cell': c, 'x0': c['x0'], 'base': base})
    tables = []
    for a in anchors:
        side_end = page_w
        for b in anchors:
            if b is not a and b['x0'] > a['x0'] + 20 and abs(b['base'] - a['base']) < 40:
                side_end = min(side_end, b['x0'] - 3)
        xs = a['x0'] - 3
        # header lines: anchor line + following header lines close below it
        used_lines = [a['line']]
        last_base = a['base']
        for lj in range(a['line'] + 1, len(hdr_lines)):
            base, cells = hdr_lines[lj]
            inx = [c for c in cells if xs <= c['x0'] < side_end]
            if not inx:
                continue
            if base - last_base > 1.6 * a['cell']['size'] + 1:
                break
            if any(ANCHOR_RE.match(c['text'].strip()) for c in inx):
                break
            used_lines.append(lj)
            last_base = base
        cols = []
        for k, lj in enumerate(used_lines):
            base, cells = hdr_lines[lj]
            for c in cells:
                if not (xs <= c['x0'] < side_end):
                    continue
                if k == 0:
                    cols.append({'parts': [c['text']], 'x0': c['x0'], 'x1': c['x1'], 'y0': c['y0'], 'y1': c['y1']})
                    continue
                best, bov = None, 0.0
                for col in cols:
                    ov = min(col['x1'], c['x1']) - max(col['x0'], c['x0'])
                    if ov > bov or (abs(col['x0'] - c['x0']) < 4 and best is None):
                        best, bov = col, max(ov, bov)
                if best is None:
                    cols.append({'parts': [c['text']], 'x0': c['x0'], 'x1': c['x1'], 'y0': c['y0'], 'y1': c['y1'],
                                 'starts_below': True})
                else:
                    best['parts'].append(c['text'])
                    best['x0'] = min(best['x0'], c['x0'])
                    best['x1'] = max(best['x1'], c['x1'])
                    best['y1'] = max(best['y1'], c['y1'])
        cols.sort(key=lambda c: c['x0'])
        seen, dup_warn = {}, []
        for col in cols:
            key = ''
            for p in col['parts']:
                p = p.strip()
                key = (key + p) if key.endswith('-') else (key + ' ' + p if key else p)
            col['printed'] = key
            if key in seen:  # e.g. 'M.M.' printed after several inch columns, 'Y FLATS' twice
                seen[key] += 1
                dup_warn.append('header %r printed %d times; later ones renamed %r'
                                % (key, seen[key], '%s #%d' % (key, seen[key])))
                key = '%s #%d' % (key, seen[key])
            else:
                seen[key] = 1
            col['key'] = key
        hw = set()
        for lj in used_lines:
            for c in hdr_lines[lj][1]:
                if xs <= c['x0'] < side_end:
                    for w in c['words']:
                        hw.add(id(w))
        tables.append({'anchor': a, 'cols': cols, 'x0': xs, 'side_end': side_end,
                       'hdr_y0': min(c['y0'] for c in cols), 'hdr_y1': max(c['y1'] for c in cols),
                       'header_lines': len(used_lines), 'dup_warn': dup_warn, 'hdr_word_ids': hw})
    # final x range end: the nearest table header that starts right of this table's last header column
    for t in tables:
        last_x1 = max(c['x1'] for c in t['cols'])
        t['x_end'] = min([page_w] + [u['x0'] for u in tables if u is not t and u['x0'] > last_x1 + 2])
        t['x_end'] = min(t['x_end'], t['side_end'])
    return tables


def overlap(a0, a1, b0, b1):
    return min(a1, b1) - max(a0, b0) > 0


def fill_rows(t, words, heads, all_tables, style, page_h):
    """assign data words to rows / columns of table t"""
    cols = t['cols']  # cols[0] = part-number column
    # column left boundaries
    bounds = [t['x0'] - 3]
    for k in range(1, len(cols)):
        gap = cols[k]['x0'] - cols[k - 1]['x1']
        tol = min(6.0, max(2.5, gap / 2.0))
        bounds.append(cols[k]['x0'] - tol)
    t['bounds'] = bounds
    # vertical end
    y_end = FOOTER_Y
    reason = 'footer'
    for u in all_tables:
        if u is t:
            continue
        if u['hdr_y0'] > t['hdr_y1'] and overlap(u['x0'], max(c['x1'] for c in u['cols']), t['x0'], t['x_end']):
            if u['hdr_y0'] < y_end:
                y_end, reason = u['hdr_y0'], 'next table header'
    for h in heads:
        if h['y0'] > t['hdr_y1'] and overlap(h['x0'], h['x1'], t['x0'], t['x_end']) and h['y0'] < y_end:
            y_end, reason = h['y0'], 'heading ' + (h['text'] or '')
    cont = None
    for w in words:
        if is_continued_word(w) and w['y0'] > t['hdr_y1'] and t['x0'] <= w['x0'] < t['x_end'] + 40 and w['y0'] < y_end:
            y_end, reason, cont = w['y0'], 'Continued...', w
    t['y_end'], t['end_reason'] = y_end, reason
    t['continued_marker'] = cont is not None
    region = [w for w in words if t['hdr_y1'] - 1 < w['base'] and w['y1'] <= y_end + 1
              and t['x0'] - 3 <= w['x0'] < t['x_end']]
    data = [w for w in region if is_data_word(w, style)]
    other = [w for w in region if not is_data_word(w, style) and not is_header_word(w, style) and w['size'] <= 8.5]
    rows, notes, twarn = [], [], []

    def col_of(w):
        k = 0
        for i, b in enumerate(bounds):
            if w['x0'] >= b:
                k = i
        return k

    for base, ws in group_lines(data, tol=2.0):
        if base <= t['hdr_y1']:
            continue
        by_col = {}
        for w in ws:
            by_col.setdefault(col_of(w), []).append(w)
        pnw = by_col.get(0, [])
        pn_text = ' '.join(w['text'] for w in pnw)
        is_row = bool(pnw) and all(is_pn_word(w, style) for w in pnw) and len(pnw) == 1 and PN_RE.match(pn_text)
        if is_row:
            rows.append({'base': base, 'pn_words': pnw, 'cells': {k: v for k, v in by_col.items() if k != 0},
                         'warnings': []})
            continue
        # not a row: continuation of the previous row (wrapped cell / wrapped part number) or a note
        if rows:
            pitch = 10.0
            if len(rows) >= 2:
                pitch = statistics.median(r2['base'] - r1['base'] for r1, r2 in zip(rows, rows[1:]))
            if base - rows[-1]['base'] < 1.25 * max(pitch, 7.0):
                r = rows[-1]
                for k, v in by_col.items():
                    if k == 0:
                        r['pn_words'] = r['pn_words'] + v
                    else:
                        r['cells'].setdefault(k, [])
                        r['cells'][k] = r['cells'][k] + v
                r['warnings'].append('text on the next line (y=%.1f) merged into this row: %r'
                                     % (base, ' '.join(w['text'] for w in ws)))
                continue
        notes.append({'y': round(base, 1), 'text': ' '.join(w['text'] for w in ws)})
    for base, ws in group_lines([w for w in other if not is_continued_word(w)], tol=2.0):
        notes.append({'y': round(base, 1), 'text': ' '.join(w['text'] for w in ws), 'non_data_font': True})
    # only text inside the rows' band (or just under the last row) belongs to the table
    if rows:
        lo, hi = rows[0]['base'] - 1, rows[-1]['base'] + 25
        notes = [n for n in notes if lo <= n['y'] <= hi]
    else:
        notes = []
    # printed columns that have no header text (e.g. 'Steel' / 'Steel Forged' right of the last column, the K2
    # thread values between 'K1 Drill' and 'L' in Flange 1967-61): inside the x-range of header column k, words
    # after a wide gap that start right of that header's x-range. Pass 1 finds them, pass 2 also moves cells of
    # rows where header column k is blank and only the unlabeled text is present.
    extra_x = {}
    for r in rows:
        r['extra'] = {}
        for k in range(1, len(cols)):
            ws = sorted(r['cells'].get(k, []), key=lambda w: w['x0'])
            for i in range(1, len(ws)):
                if abs(ws[i]['base'] - ws[i - 1]['base']) < 2 and ws[i]['x0'] - ws[i - 1]['x1'] > 0.62 * ws[i]['size'] \
                        and ws[i]['x0'] > cols[k]['x1'] + 2:
                    r['extra'][k] = ws[i:]
                    r['cells'][k] = ws[:i]
                    extra_x.setdefault(k, []).append(ws[i]['x0'])
                    break
    for k, xs_ in extra_x.items():
        lim = min(xs_) - 3
        for r in rows:
            ws = sorted(r['cells'].get(k, []), key=lambda w: w['x0'])
            if k not in r['extra'] and ws and ws[0]['x0'] >= lim and ws[0]['x0'] > cols[k]['x1'] + 2:
                r['extra'][k] = ws
                r['cells'][k] = []
    out_cols = []  # (key, header column index or None, unlabeled-after index or None)
    for k in range(1, len(cols)):
        out_cols.append((cols[k]['key'], k, None))
        if k in extra_x:
            ukey = UNLABELED if k == len(cols) - 1 else '%s after %s' % (UNLABELED, cols[k]['key'])
            out_cols.append((ukey, None, k))
            n = sum(1 for r in rows if k in r['extra'])
            twarn.append('%d row(s) carry text in a printed column that has no header, right of %r - kept as %r'
                         % (n, cols[k]['key'], ukey))
    t['out_cols'] = out_cols
    # build output rows
    out_rows = []
    offs = {k: [] for k in range(len(cols))}
    for r in rows:
        pnw = r['pn_words']
        pn = ''
        for w in pnw:
            pn = pn + w['text'] if (not pn or pn.endswith('-')) else pn + ' ' + w['text']
        vals = {}
        warns = list(r['warnings'])
        empty = []
        for key, k, uk in out_cols:
            if k is None:
                vals[key] = ' '.join(w['text'] for w in sorted(r['extra'].get(uk, []), key=lambda w: (round(w['base']), w['x0'])))
                continue
            ws = sorted(r['cells'].get(k, []), key=lambda w: (round(w['base']), w['x0']))
            txt = ' '.join(w['text'] for w in ws)
            vals[key] = txt
            if not ws:
                empty.append(key)
                continue
            offs[k].append((ws[0]['x0'] - cols[k]['x0'], r, k))
            # a gap wider than ~1.5 spaces inside one cell = possibly two printed cells in one column
            same_line = [w for w in ws if abs(w['base'] - r['base']) < 2]
            for w1, w2 in zip(same_line, same_line[1:]):
                if w2['x0'] - w1['x1'] > 0.62 * w1['size']:
                    warns.append('wide gap inside cell %r: %r' % (key, txt))
                    break
        if empty:
            warns.append('empty cell(s): ' + ', '.join(empty))
        if len(pnw) > 1:
            warns.append('part number assembled from %d words' % len(pnw))
        out_rows.append({'pn': pn, 'values': vals, 'line_y': round(r['base'], 1), 'warnings': warns})
    # alignment diagnostics: first word of a cell far from the column's usual start
    for k, lst in offs.items():
        if len(lst) < 3:
            continue
        med = statistics.median(o for o, _, _ in lst)
        for o, r, kk in lst:
            if abs(o - med) > 4.5:
                i = rows.index(r)
                out_rows[i]['warnings'].append('cell %r starts %.1f pt off the column alignment (value %r)'
                                               % (cols[kk]['key'], o - med, out_rows[i]['values'][cols[kk]['key']]))
    used = set()
    for r in rows:
        used |= set(id(w) for w in r['pn_words'])
        for v in list(r['cells'].values()) + list(r['extra'].values()):
            used |= set(id(w) for w in v)
    t['used_ids'] = used
    if not out_rows:
        twarn.append('header without rows')
    else:
        t['y_end'] = min(t['y_end'], max(r['base'] for r in rows) + 3)
    t['rows_out'], t['notes'], t['twarn'] = out_rows, notes, twarn


def assign_headings(page_tables, heads):
    """nearest series heading above each table header in an overlapping x-range, unless another table header
    of the same x-range is nearer (then: continuation)"""
    for t in page_tables:
        best, best_rank, best_kind = None, (-1e9, 0), None
        for h in heads:
            if h['kind'] not in ('series', 'section'):
                continue
            # rank: lowest bottom edge wins; on a tie a series number beats a section title
            rank = (round(h['y1'], 0), 1 if h['kind'] == 'series' else 0)
            if h['y1'] <= t['hdr_y0'] + 2 and overlap(h['x0'], h['xr'], t['x0'], t['x_end']) and rank > best_rank:
                best, best_rank, best_kind = h, rank, 'heading'
        for u in page_tables:
            if u is t:
                continue
            if u['hdr_y0'] < t['hdr_y0'] - 1 and overlap(u['x0'], max(c['x1'] for c in u['cols']), t['x0'], t['x_end']):
                rank = (round(u['hdr_y1'], 0), 2)
                if rank > best_rank:
                    best, best_rank, best_kind = u, rank, 'table'
        t['heading_note'] = None
        if best_kind == 'heading' and best['kind'] == 'series':
            t['heading'] = best
        else:
            t['heading'] = None
            t['heading_blocker'] = best_kind if best is not None else None
            t['heading_blocker_obj'] = best
    # fallback: a series heading that is not over any table, placed beside (not over) a table that found none,
    # below the table that blocked it (ORFS p19: FS0304-C heading on the left, its table on the right)
    used = set(id(t['heading']) for t in page_tables if t.get('heading'))
    for t in sorted(page_tables, key=lambda t: t['hdr_y0']):
        if t['heading'] is not None:
            continue
        floor = -1e9
        if t.get('heading_blocker') == 'table':
            floor = t['heading_blocker_obj']['y_end'] - 2
        elif t.get('heading_blocker') == 'heading':
            floor = t['heading_blocker_obj']['y0'] - 1
        cands = [h for h in heads if h['kind'] == 'series' and id(h) not in used
                 and floor <= h['y0'] and h['y1'] <= t['hdr_y0'] + 2 and t['hdr_y0'] - h['y1'] < 150]
        if cands and t.get('heading_blocker') is not None:
            h = max(cands, key=lambda h: h['y1'])
            t['heading'] = h
            used.add(id(h))
            t['heading_note'] = ('heading %r is not above the table (x %.0f-%.0f vs table x %.0f-%.0f); taken as the '
                                 'only unused heading between the previous table and this header'
                                 % (h['series'], h['x0'], h['xr'], t['x0'], t['x_end']))


def printed_page_number(words, page_h):
    nums = [w for w in words if w['y0'] > FOOTER_Y and re.fullmatch(r'\d{1,3}', w['text'])]
    return int(nums[0]['text']) if len(nums) == 1 else None


def parse_index(words, style):
    """TFA / Flange / ORFS index: blue Bebas code + Bebas title + 'PAGE: n'"""
    if style != 'gx':
        return []
    codes = [w for w in words if w['font'].startswith('BebasNeueBold') and 8 <= w['size'] <= 10.6 and w['color'] == BLUE]
    texts = [w for w in words if w['font'].startswith('BebasNeueBook') and 8 <= w['size'] <= 10.6 and w['color'] == 0]
    out = []
    for c in codes:
        same = sorted([w for w in texts if abs(w['base'] - c['base']) < 2 and w['x0'] > c['x1']], key=lambda w: w['x0'])
        nxt = [d['x0'] for d in codes if abs(d['base'] - c['base']) < 2 and d['x0'] > c['x1']]
        lim = min(nxt) if nxt else 1e9
        same = [w for w in same if w['x0'] < lim]
        txt = ' '.join(w['text'] for w in same)
        m = re.match(r'^(.*?)\s*PAGE:\s*(\d*)\s*$', txt)
        if not m:
            continue
        out.append({'series': c['text'], 'title': m.group(1).strip(), 'page': int(m.group(2)) if m.group(2) else None,
                    'y': round(c['base'], 1)})
    return out


# ----------------------------------------------------------------------------------------------- catalog
def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_catalog(cat, pdf_path, style):
    doc = pymupdf.open(pdf_path)
    tables, index, page_warn = [], [], []
    for pi in range(len(doc)):
        page = doc[pi]
        pno = pi + 1
        words = page_words(page)
        pw, ph = page.rect.width, page.rect.height
        heads = find_headings(words, style)
        ptables = build_tables_on_page(words, style, pw)
        for t in ptables:
            fill_rows(t, words, heads, ptables, style, ph)
        assign_headings(ptables, heads)
        idx = parse_index(words, style)
        for e in idx:
            e['index_page'] = pno
        index.extend(idx)
        printed = printed_page_number(words, ph)
        if printed is not None and printed != pno:
            page_warn.append({'catalog': cat, 'page': pno, 'warning': 'printed page number %d differs from PDF page index' % printed})
        # part numbers on the page that no table claimed
        claimed = set()
        for t in ptables:
            for r in t['rows_out']:
                claimed.add((r['pn'], r['line_y']))
        for w in words:
            if is_pn_word(w, style) and w['y0'] < FOOTER_Y and PN_RE.match(w['text']) and re.search(r'\d{2}', w['text']):
                if style == 'gt' and not re.fullmatch(r'D\d{5,6}', w['text']):
                    continue
                if not any(abs(w['base'] - y) < 2.1 and pn.startswith(w['text'][:4]) for pn, y in claimed):
                    page_warn.append({'catalog': cat, 'page': pno, 'warning': 'part-number-like word %r at x=%.0f y=%.0f is in no table'
                                      % (w['text'], w['x0'], w['base'])})
        # header-style text that no table used = a table this parser does not read (e.g. Hosetail charts)
        used_hw, used_dw = set(), set()
        for t in ptables:
            used_hw |= t['hdr_word_ids']
            used_dw |= t['used_ids']

        def headerish(w):
            if style == 'gx':
                return is_header_word(w, style)
            return w['font'].startswith('Gotham-Bold') and w['color'] == BLUE and w['size'] < 12
        loose = [w for w in words if headerish(w) and w['y0'] < FOOTER_Y and id(w) not in used_hw]
        if loose:
            txt = ' / '.join(' '.join(w['text'] for w in ws) for _, ws in group_lines(loose))
            page_warn.append({'catalog': cat, 'page': pno, 'warning': 'header-style text outside any parsed table '
                              '(table not parsed): %s' % (txt[:300] + ('...' if len(txt) > 300 else ''))})
        # completeness: every table-font word on the page must sit in some row
        lost = [w for w in words if is_data_word(w, style) and w['y0'] < FOOTER_Y and id(w) not in used_dw]
        if lost:
            txt = ' / '.join(' '.join(w['text'] for w in ws) for _, ws in group_lines(lost))
            page_warn.append({'catalog': cat, 'page': pno, 'warning': '%d table-font word(s) in no table row: %s'
                              % (len(lost), txt[:400] + ('...' if len(txt) > 400 else ''))})
        for h in heads:
            if h['kind'] == 'orphan_title':
                page_warn.append({'catalog': cat, 'page': pno, 'warning': 'title text %r not attached to a series number' % h['text']})
        half = pw / 2.0
        for t in ptables:
            t['page'] = pno
            t['printed_page'] = printed
            t['colgroup'] = 0 if t['x0'] < half - 20 else 1
        ptables.sort(key=lambda t: (t['colgroup'], t['hdr_y0']))
        used_heads = set(id(t['heading']) for t in ptables if t.get('heading'))
        for h in heads:
            if h['kind'] == 'series' and id(h) not in used_heads:
                page_warn.append({'catalog': cat, 'page': pno, 'warning': 'heading %r (%s) has no table under it'
                                  % (h['series'], h['title'])})
        tables.extend(ptables)
    # continuation linking (reading order = page, column group, y)
    out = []
    prev = None
    counter = {}
    for t in tables:
        counter[t['page']] = counter.get(t['page'], 0) + 1
        tid = '%s-p%03d-t%02d' % (cat, t['page'], counter[t['page']])
        cols = t['cols']
        warns = list(t['dup_warn']) + list(t['twarn'])
        columns = []
        for key, k, uk in t['out_cols']:
            if k is None:
                columns.append({'key': key, 'letter': None, 'meaning': None, 'printed': ''})
                continue
            c = cols[k]
            letter, meaning, mark = parse_header_key(c['printed'], style)
            col = {'key': c['key'], 'letter': letter, 'meaning': meaning}
            if c['key'] != c['printed']:
                col['printed'] = c['printed']
            if mark:
                col['mark'] = mark
            columns.append(col)
        rec = {'table_id': tid, 'catalog': cat, 'page': t['page'], 'printed_page': t['printed_page'],
               'series': None, 'title': None, 'pn_header': cols[0]['key'], 'columns': columns,
               'header_lines': t['header_lines'], 'rows': [], 'continued_from_page': None,
               'continued_from_table': None, 'continued_marker': t['continued_marker'],
               'bbox': [round(t['x0'], 1), round(t['hdr_y0'], 1), round(t['x_end'], 1), round(t['y_end'], 1)],
               'end_reason': t['end_reason'], 'notes': t['notes'], 'warnings': warns}
        rec['rows'] = t['rows_out']
        rec['pn_roots'] = sorted(set(r['pn'].split('-')[0] for r in rec['rows'])) if style == 'gx' else []
        if t.get('heading'):
            rec['series'] = t['heading']['series']
            rec['title'] = t['heading']['title']
            if t.get('heading_note'):
                warns.append(t['heading_note'])
        else:
            if prev is None:
                warns.append('no heading above this table and no previous table to continue')
            else:
                rec['series'], rec['title'] = prev['series'], prev['title']
                rec['continued_from_page'] = prev['page']
                rec['continued_from_table'] = prev['table_id']
                if [c['key'] for c in prev['columns']] != [c['key'] for c in columns]:
                    warns.append('continuation of %s but the header differs: %s vs %s'
                                 % (prev['table_id'], [c['key'] for c in prev['columns']], [c['key'] for c in columns]))
                if not prev['continued_marker'] and style == 'gx':  # Hosetail prints no 'Continued...'
                    warns.append('continuation of %s, which does not end with "Continued..."' % prev['table_id'])
                if t.get('heading_blocker') == 'table':
                    warns.append('no heading between this header and the table header above it')
        # part numbers must start like the series (first dash token), except Hosetail (D-numbers)
        if rec['series'] and style == 'gx':
            root = rec['series'].split('-')[0]
            bad = [r['pn'] for r in rec['rows'] if r['pn'].split('-')[0] != root]
            if bad:
                warns.append('%d part number(s) do not start with series root %r: %s' % (len(bad), root, bad[:6]))
        # cell count per row
        nbad = sum(1 for r in rec['rows'] if any(w.startswith('empty cell') for w in r['warnings']))
        if nbad:
            warns.append('%d of %d rows have empty cells (see row warnings)' % (nbad, len(rec['rows'])))
        out.append(rec)
        prev = rec
    return out, index, page_warn, len(doc)


# ----------------------------------------------------------------------------------------------- checks / output
def cross_checks(all_tables, all_index):
    checks = {}
    for cat in sorted(set(t['catalog'] for t in all_tables)):
        tabs = [t for t in all_tables if t['catalog'] == cat]
        idx = all_index.get(cat, [])
        found = {}
        for t in tabs:
            found.setdefault(t['series'], []).append(t['page'])
        missing, moved = [], []
        for e in idx:
            if e['series'] not in found:
                missing.append(e)
            elif e['page'] is not None and e['page'] not in found[e['series']]:
                moved.append({'series': e['series'], 'index_page': e['page'], 'parsed_pages': sorted(set(found[e['series']]))})
        not_in_index = sorted(s for s in found if s and idx and s not in {e['series'] for e in idx})
        pn_seen = {}
        for t in tabs:
            for r in t['rows']:
                pn_seen.setdefault(r['pn'], []).append(t['table_id'])
        dups = {pn: v for pn, v in pn_seen.items() if len(v) > 1}
        checks[cat] = {'index_entries': len(idx), 'index_series_without_table': missing,
                       'index_page_differs': moved, 'series_not_in_index': not_in_index,
                       'duplicate_part_numbers': dups}
    return checks


def write_csv(path, tabs):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['catalog', 'page', 'table_id', 'series', 'title', 'continued_from_page', 'pn', 'column_key',
                    'letter', 'meaning', 'value', 'line_y', 'row_warnings'])
        for t in tabs:
            for r in t['rows']:
                for c in t['columns']:
                    w.writerow([t['catalog'], t['page'], t['table_id'], t['series'], t['title'],
                                t['continued_from_page'] or '', r['pn'], c['key'], c['letter'] or '', c['meaning'] or '',
                                r['values'].get(c['key'], ''), r['line_y'], ' | '.join(r['warnings'])])


def write_summary(path, result, npages):
    tabs = result['tables']
    L = []
    L.append('Brennan catalog parse - %s' % result['created'])
    L.append('generator: %s' % result['generator'])
    for f, h in result['sources'].items():
        L.append('source: %s  sha256 %s' % (f, h))
    L.append('')
    tot_t = len(tabs)
    tot_r = sum(len(t['rows']) for t in tabs)
    L.append('TOTAL: %d tables, %d rows' % (tot_t, tot_r))
    for cat in result['catalogs']:
        ct = [t for t in tabs if t['catalog'] == cat]
        rw = sum(1 for t in ct for r in t['rows'] if r['warnings'])
        L.append('  %-9s %3d tables  %5d rows  %4d table warnings  %4d rows with warnings  %3d page warnings'
                 % (cat, len(ct), sum(len(t['rows']) for t in ct), sum(len(t['warnings']) for t in ct), rw,
                    sum(1 for w in result['page_warnings'] if w['catalog'] == cat)))
    for cat in result['catalogs']:
        L.append('')
        L.append('=' * 100)
        L.append('%s  (%d pages)' % (cat, npages[cat]))
        L.append('=' * 100)
        pages = sorted(set([t['page'] for t in tabs if t['catalog'] == cat] +
                           [w['page'] for w in result['page_warnings'] if w['catalog'] == cat]))
        for p in pages:
            pt = [t for t in tabs if t['catalog'] == cat and t['page'] == p]
            L.append('-- page %d: %d tables, %d rows' % (p, len(pt), sum(len(t['rows']) for t in pt)))
            for t in pt:
                cont = (' (continued from p%d %s)' % (t['continued_from_page'], t['continued_from_table'])) if t['continued_from_page'] else ''
                L.append('   %s  %-16s %-40s %3d rows  %d cols%s%s' % (
                    t['table_id'], t['series'], (t['title'] or '')[:40], len(t['rows']), len(t['columns']), cont,
                    '  [ends "Continued..."]' if t['continued_marker'] else ''))
                L.append('      columns: ' + ' | '.join(c['key'] for c in t['columns']))
                for w in t['warnings']:
                    L.append('      WARN ' + w)
                for r in t['rows']:
                    for w in r['warnings']:
                        L.append('      row %s: %s' % (r['pn'], w))
                for n in t['notes']:
                    L.append('      note y=%s: %s' % (n['y'], n['text']))
            for w in result['page_warnings']:
                if w['catalog'] == cat and w['page'] == p:
                    L.append('   PAGE WARN ' + w['warning'])
        ch = result['checks'].get(cat)
        if ch:
            L.append('')
            L.append('cross-check against the catalog index (%d entries):' % ch['index_entries'])
            for e in ch['index_series_without_table']:
                L.append('   index series without a parsed table: %s %s (index page %s)' % (e['series'], e['title'], e['page']))
            if ch['index_page_differs']:
                hist = {}
                for e in ch['index_page_differs']:
                    off = min(e['parsed_pages']) - e['index_page']
                    hist[off] = hist.get(off, 0) + 1
                L.append('   index page differs for %d series; parsed page minus index page: %s' % (
                    len(ch['index_page_differs']), ', '.join('%+d: %d series' % (k, v) for k, v in sorted(hist.items()))))
            for e in ch['index_page_differs']:
                L.append('   index page differs: %s index p%s, parsed p%s' % (e['series'], e['index_page'], e['parsed_pages']))
            if ch['series_not_in_index']:
                L.append('   parsed series not in the index: ' + ', '.join(ch['series_not_in_index']))
            if ch['duplicate_part_numbers']:
                L.append('   part numbers in more than one table: %d' % len(ch['duplicate_part_numbers']))
                for pn, v in sorted(ch['duplicate_part_numbers'].items()):
                    L.append('      %s: %s' % (pn, ', '.join(v)))
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')


def render_pngs(spec, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for part in spec:
        cat, pages = part.split(':')
        doc = pymupdf.open(os.path.join(PDF_DIR, CATALOGS[cat.upper()][0]))
        for p in pages.split(','):
            p = int(p)
            fn = os.path.join(out_dir, '%s_p%02d.png' % (cat.upper(), p))
            doc[p - 1].get_pixmap(dpi=200).save(fn)
            print('rendered', fn)


def show_pages(json_path, spec):
    """print parsed tables of CAT:p1,p2 as text grids (for comparing with the rendered page)"""
    with open(json_path, encoding='utf-8') as f:
        res = json.load(f)
    for part in spec:
        cat, pages = part.split(':')
        for p in [int(x) for x in pages.split(',')]:
            for t in [t for t in res['tables'] if t['catalog'] == cat.upper() and t['page'] == p]:
                print('=' * 120)
                print('%s  series=%s  title=%s  continued_from=%s  bbox=%s  end=%s' % (
                    t['table_id'], t['series'], t['title'], t['continued_from_table'], t['bbox'], t['end_reason']))
                keys = [c['key'] for c in t['columns']]
                grid = [[t['pn_header']] + keys] + [[r['pn']] + [r['values'].get(k, '') for k in keys] for r in t['rows']]
                wid = [max(len(row[i]) for row in grid) for i in range(len(grid[0]))]
                for row in grid:
                    print(' | '.join(c.ljust(wid[i]) for i, c in enumerate(row)))
                for w in t['warnings']:
                    print('  WARN', w)
                for r in t['rows']:
                    for w in r['warnings']:
                        print('  ROW %s: %s' % (r['pn'], w))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=DEFAULT_OUT)
    ap.add_argument('--pdf-dir', default=PDF_DIR)
    ap.add_argument('--catalog', nargs='*', default=list(CATALOGS))
    ap.add_argument('--png', nargs='*', default=[], help='CAT:p1,p2 ... render pages to <out>/png at 200 dpi')
    ap.add_argument('--show', nargs='*', default=[], help='CAT:p1,p2 ... only print the parsed tables of these pages '
                    'from <out>/catalog_parsed.json (no parsing)')
    a = ap.parse_args()
    if a.show:
        show_pages(os.path.join(a.out, 'catalog_parsed.json'), a.show)
        return
    os.makedirs(a.out, exist_ok=True)
    result = {'generator': 'tools/catalog/parse_brennan_catalog.py',
              'created': datetime.datetime.now().isoformat(timespec='seconds'),
              'conventions': {
                  'page': '1-based page index of the PDF (printed_page = the number printed in the footer, if any)',
                  'values': 'printed strings exactly as in the text layer (words of one cell joined by one space); '
                            'empty string = blank cell. Units as printed (mostly inches; some ORFS / Flange tables are mm).',
                  'columns': 'key = printed header text (multi-line headers joined top to bottom with a space); '
                             'letter = drawing letter when the header starts with one; the part-number column is '
                             'not in columns (pn_header)',
                  'continued_from_page': 'set when the table has no heading of its own: it continues the previous '
                                         'table in reading order (series/title inherited)',
                  'line_y': 'baseline of the row in PDF points from the top of the page',
                  'unlabeled columns': "'(no header)' / '(no header) after <key>' = a printed column without header "
                                       "text (e.g. 'Steel Forged', or K2 thread sizes in Flange 1967-61)",
                  'duplicate headers': "a header printed twice in one table keeps its text, later ones get ' #2', "
                                       "' #3' (e.g. 'M.M.' millimetre columns); 'printed' holds the header text"},
              'known_limitations': [
                  'Tables without a PART NO./Item column are not parsed (Hosetail p2 thread chart, p3 ferrule '
                  'compatibility matrix); they are listed in page_warnings.',
                  'Printed typos are kept as printed (e.g. heading "05010801" over 0801-06-04, 1930-61-24-24 inside '
                  'the 1929-61 table, L "23620", "136/16-16", "5/15", "2.2252"); only structural ones are warned.',
                  'Units are as printed; the parser does not mark metric tables (ORFS FS7210/FS7215 lengths and hexes, '
                  "'M.M.' columns) beyond their header text.",
                  'letter/meaning are a heuristic split of the printed header; key is the authoritative printed text.',
                  "A table with no heading above it inherits series/title from the previous table in reading order "
                  "(page, left column, right column); every such link is checked for an identical header."],
              'catalogs': [], 'sources': {}, 'tables': [], 'index': {}, 'page_warnings': [], 'checks': {}}
    npages = {}
    for cat in a.catalog:
        cat = cat.upper()
        fn, style = CATALOGS[cat]
        path = os.path.join(a.pdf_dir, fn)
        result['sources'][fn] = sha256(path)
        tabs, idx, pw, n = parse_catalog(cat, path, style)
        npages[cat] = n
        result['catalogs'].append(cat)
        result['tables'].extend(tabs)
        result['index'][cat] = idx
        result['page_warnings'].extend(pw)
        write_csv(os.path.join(a.out, 'catalog_%s.csv' % cat), tabs)
        print('%-9s %3d tables %5d rows' % (cat, len(tabs), sum(len(t['rows']) for t in tabs)))
    result['checks'] = cross_checks(result['tables'], result['index'])
    with open(os.path.join(a.out, 'catalog_parsed.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    write_summary(os.path.join(a.out, 'catalog_parsed_summary.txt'), result, npages)
    if a.png:
        render_pngs(a.png, os.path.join(a.out, 'png'))
    print('written to', a.out)


if __name__ == '__main__':
    main()
