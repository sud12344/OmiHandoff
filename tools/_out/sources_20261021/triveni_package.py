"""triveni_package.py (2026-10-21, cloud): the parts nobody gives us dimensions for, as a package for Triveni (OMi).
Rule (2026-10-21, after the PARTcommunity lookup): a not-ready part goes to OMi when
  (1) no catalog prints it - Air-Way, Brennan's PDF catalogs, OMi's own parts file (sources.csv: NO SOURCE), and
  (2) Brennan has no CAD model for it (tools/_out/partcommunity_20261021/pc_final.csv: match exact / alias = covered);
      a body-only "-M1" compression part counts as covered when Brennan models the complete fitting (asked as a question).
Then: kits 1901 / 1902 / 1927 out of scope (one line); 5404-N-..X.. long nipples covered by A4 (Q-TRANSFER-5404N: the length is in the
part number); the 2700-LN rows asked as "same as the plain part?" (A10); FS0319-24 asked as a question (three printed values disagree);
0618 / 0619 asked as "= Brennan V0318 / V0319?" (Brennan prints V0318 / V0319; Q-NEW-F3-FLARELESS-ALIAS).
Writes 10_DRAWINGS/for_OMi_2026-10-21/: the PDF, the fill-in workbook and the email text. Nothing is sent."""
import os, re, csv, collections, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
OUT = J('10_DRAWINGS', 'for_OMi_2026-10-21'); os.makedirs(OUT, exist_ok=True)
DATE = '2026-10-21'

src = {r['part']: r for r in csv.DictReader(open(os.path.join(HERE, 'sources.csv'), encoding='utf-8'))}
pcf = {r['part']: r for r in csv.DictReader(open(J('tools', '_out', 'partcommunity_20261021', 'pc_final.csv'), encoding='utf-8'))}
cad = lambda p: p in pcf and pcf[p]['match'] in ('exact', 'alias')
covered = lambda p: cad(p) or (p.endswith('-M1') and cad(p[:-3]))
need = [p for p in src if src[p]['cls'] == 'NO SOURCE' and not covered(p)
        and '-KIT' not in p and not p.startswith('5404-N-')]
COMP_ALL = [l.strip().upper() for l in open(J('07_RAW_EXTRACTS', 'omi_feed', 'omi_skus_compression.txt')) if l.strip()]
G_COMP, G_TG, G_4005, G_FL = 'comp', 'tg', '4005', 'fl'
grp = {G_COMP: [p for p in need if p in COMP_ALL], G_TG: [p for p in need if p.startswith('TGT-')],
       G_4005: [p for p in need if p.startswith('4005-')], G_FL: ['0618-06', '0618-08', '0619-06', '0619-08']}
singles = [p for p in need if p not in grp[G_COMP] + grp[G_TG] + grp[G_4005]]
n_comp_brennan = sum(1 for p in COMP_ALL if cad(p))                      # complete fittings Brennan models
n_comp_m1 = sum(1 for p in COMP_ALL if covered(p) and not cad(p))      # their body-only -M1 numbers (assumed same body)

ws = openpyxl.load_workbook(J('07_RAW_EXTRACTS', 'omi_dimensions', 'WebsitePartsInfo2026.xlsx'), read_only=True, data_only=True)['Items']
rows = list(ws.iter_rows(values_only=True)); H = rows[0]
desc = {}
for r in rows[3:]:
    d = dict(zip(H, r))
    if d.get('Part Number'):
        desc[str(d['Part Number']).strip().upper()] = str(d.get('Part Description') or '').strip()


def needs(p, ds):
    """What we ask for, in the column names of OMi's own parts file."""
    swivel = bool(re.search(r'\b(FJS|FFSS|FPS)\b', ds))
    if p.startswith('2700-LN-'):
        return 'Same as the plain part ' + p.replace('-LN', '') + '? (we model the -LN part without the lock nut)'
    if p.startswith('2700-'):
        return 'Overall Length, Hex Flat, Side 1 ID, Side 2 ID, bulkhead thread length'
    if p.startswith('5404-R-'):
        return 'Overall Length, Hex Flat, orifice length'
    if p.startswith('5404-L-'):
        return 'Hex Flat, hex length and position, Side 1 ID'
    if p.startswith('FS0304-C'):
        return 'Overall Length, Hex Flat, insert sizes (a drawing is best)'
    if '1803-' in p:
        return 'M 1 Size, L 1 Size, Side 1 ID, Side 2 ID, flange head diameter and thickness'
    if 'Tee' in ds:
        return 'M 1 Size, L 1 Size, branch leg length, Hex Flat, Side 1-3 ID' + (', Nut Hex 1' if swivel else '')
    if 'Elbow' in ds:
        return 'M 1 Size, L 1 Size, Hex Flat, Side 1 ID, Side 2 ID' + (', Nut Hex 1' if swivel else '')
    return 'Overall Length, Hex Flat, Side 1 ID, Side 2 ID' + (', Nut Hex 1' if swivel else '')


single_rows = [(p, desc.get(p, ''), needs(p, desc.get(p, ''))) for p in singles]
tg_rows = [(p, desc.get(p, ''), 'M 1 Size, L 1 Size, test-port leg length, Hex Flat, Nut Hex 1, Side 1-3 ID') for p in grp[G_TG]]

# compression: one body per series; "-M1" = the same body sold without nut and sleeve
comp = collections.OrderedDict()
for p in sorted(grp[G_COMP]):
    s = p.split('-')[0]; comp.setdefault(s, {'parts': [], 'm1': []})
    comp[s]['m1' if p.endswith('-M1') else 'parts'].append(p)
SER_DESC = {}
for s, v in comp.items():
    d = desc.get((v['parts'] or v['m1'])[0], '')
    SER_DESC[s] = re.sub(r'^\d\d\s+', '', re.sub(r'\b\d\d\s+(?=(BT|MJ|MP|FP|MAORB)\b)', '', d)).replace(' (Body)', '')
n_out = len(grp[G_COMP]) + len(tg_rows) + len(single_rows) + 1 + len(grp[G_4005]) + len(grp[G_FL])


def dashes(ps):
    return ', '.join(re.sub(r'^[A-Z]*\d{4}-', '', p).replace('-NWO', '').replace('-FG', '').replace('-M1', '') for p in ps)


# ---------------------------------------------------------------- PDF
ss = getSampleStyleSheet()
INK, MUTED, RULE, HEAD = colors.HexColor('#1f2933'), colors.HexColor('#52606d'), colors.HexColor('#cbd2d9'), colors.HexColor('#e4e7eb')
st = {
    'title': ParagraphStyle('t', parent=ss['Title'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=INK, alignment=0, spaceAfter=4),
    'sub': ParagraphStyle('s', parent=ss['Normal'], fontSize=10, leading=13, textColor=MUTED, spaceAfter=14),
    'h1': ParagraphStyle('h1', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=13.5, leading=17, textColor=INK, spaceBefore=14, spaceAfter=6),
    'h2': ParagraphStyle('h2', parent=ss['Heading3'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=INK, spaceBefore=8, spaceAfter=3),
    'p': ParagraphStyle('p', parent=ss['Normal'], fontSize=9.5, leading=13, textColor=INK, spaceAfter=6),
    'cell': ParagraphStyle('c', parent=ss['Normal'], fontSize=8.3, leading=10.4, textColor=INK),
    'cellb': ParagraphStyle('cb', parent=ss['Normal'], fontName='Helvetica-Bold', fontSize=8.3, leading=10.4, textColor=INK),
    'li': ParagraphStyle('li', parent=ss['Normal'], fontSize=9.5, leading=13, textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=3),
}
C = lambda t, b=False: Paragraph(str(t), st['cellb' if b else 'cell'])


def table(head, body, widths, zebra=True):
    t = Table([[C(h, True) for h in head]] + [[C(x) for x in r] for r in body], colWidths=widths, repeatRows=1)
    sty = [('BACKGROUND', (0, 0), (-1, 0), HEAD), ('LINEBELOW', (0, 0), (-1, 0), 0.8, MUTED), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
           ('LINEBELOW', (0, 1), (-1, -1), 0.25, RULE), ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if zebra:
        sty += [('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f5f7fa')) for i in range(2, len(body) + 1, 2)]
    t.setStyle(TableStyle(sty)); return t


def footer(c, doc):
    c.saveState(); c.setFont('Helvetica', 7.5); c.setFillColor(MUTED)
    c.drawString(0.75 * inch, 0.5 * inch, f'OM Industrial carbon-steel fitting library - parts without dimensions - {DATE}')
    c.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f'Page {doc.page}'); c.restoreState()


W = letter[0] - 1.5 * inch
S = [Paragraph('Parts we have no dimensions for', st['title']),
     Paragraph(f'OM Industrial carbon-steel fitting library &nbsp;|&nbsp; {DATE} &nbsp;|&nbsp; {n_out} part numbers', st['sub']),
     Paragraph('We checked every part number on your website that is not modelled yet against Air-Way\'s catalog, Brennan\'s catalogs and '
               '3D files, and your website parts file (WebsitePartsInfo2026.xlsx). The parts below appear in none of them with '
               'dimensions, so we cannot model them without your help. All sizes in inches.', st['p']),
     Paragraph('<b>The quickest answer is usually your supplier\'s drawing:</b> one drawing per series with its size table is plenty, and '
               'then nothing needs to be filled in. Otherwise the attached workbook has a yellow cell for each value we need, using the '
               'same column names as your parts file.', st['p']),
     Spacer(1, 4),
     table(['', 'What', 'Parts', 'What we need'], [
         ['1', 'Compression (bite-type) fittings', str(len(grp[G_COMP])), f'A drawing per series ({len(comp)} series); which standard the bite-type port follows'],
         ['2', 'Test-gauge tees TGT-6504 / TGT-FS2406', str(len(tg_rows)), 'A drawing per series (2 series)'],
         ['3', 'Single sizes nobody prints', str(len(single_rows)), 'The values listed per part (or a drawing)'],
         ['4', 'Flange O-rings 4005', str(len(grp[G_4005])), 'Code 61 or 62; I.D. x cross-section; material, hardness'],
         ['5', 'Flareless nut 0618 / sleeve 0619', str(len(grp[G_FL])), 'Are they Brennan\'s V0318 / V0319? If not: sizes and shape'],
         ['6', 'FS0319-24 sleeve: three printed values disagree', '1', 'Which outside diameter is right'],
     ], [0.25 * inch, 2.6 * inch, 0.5 * inch, W - 3.35 * inch]),
     Spacer(1, 8),
     Paragraph('Not on this list: parts that Air-Way, Brennan or your parts file already print, and parts Brennan has 3D models for '
               f'(including {n_comp_brennan} of your compression fittings, and with them {n_comp_m1} body-only -M1 numbers). We are treating the kits 1901 / 1902 / 1927 (30 parts) as out of scope; tell us if you need them '
               'modelled.', st['p'])]

S += [PageBreak(), Paragraph(f'1. Compression (bite-type) fittings - {len(grp[G_COMP])} parts', st['h1']),
      Paragraph(f'Brennan has 3D models for {n_comp_brennan} of your compression part numbers (all nuts and sleeves and most fittings). '
                f'A "(Body)" part number (-M1) is, we assume, the same body sold without the nut and sleeve - please confirm; on that '
                f'basis those models also cover {n_comp_m1} of the -M1 numbers, and only these {len(grp[G_COMP])} remain. Air-Way has no '
                'compression series. Please also tell us which '
                'standard the bite-type port follows (thread, tube bore, the cone the sleeve bites into, port depth).', st['p']),
      table(['Series', 'Description (your file)', 'Sizes (dash numbers)', 'Parts'],
            [[s, SER_DESC[s], dashes(v['parts']) + (f'<br/><font color="#52606d">Body only (-M1): {dashes(v["m1"])}</font>' if v['m1'] else ''),
              str(len(v['parts']) + len(v['m1']))] for s, v in comp.items()],
            [0.6 * inch, 1.75 * inch, W - 2.85 * inch, 0.5 * inch]),
      Paragraph('What we need per part: Overall Length (or M 1 / L 1 Size for elbows and tees), Hex Flat, Side 1 ID, Side 2 ID.', st['p'])]

S += [Paragraph('2. Test-gauge tees - 12 parts', st['h1']),
      Paragraph('Swivel unions with a -04 pipe test port. Air-Way\'s test points are a different (metric) part, and Brennan does not print these.', st['p']),
      table(['Part number', 'Description (your file)', 'What we need'], tg_rows, [1.45 * inch, 2.35 * inch, W - 3.8 * inch])]

S += [PageBreak(), Paragraph(f'3. Single sizes nobody prints - {len(single_rows)} parts', st['h1']),
      Paragraph('The rest of each series is modelled; only these sizes are missing from Air-Way, Brennan and your parts file. The values we '
                'need use your parts file\'s column names (M 1 / L 1 Size = the two leg lengths of an elbow).', st['p']),
      table(['Part number', 'Description (your file)', 'What we need'], single_rows, [1.45 * inch, 2.35 * inch, W - 3.8 * inch])]

S += [Paragraph(f'4. Flange O-ring {", ".join(grp[G_4005])}', st['h1']),
      Paragraph('Brennan models the other eight 4005 sizes, not this one. Code 61 or code 62 flange? Inside diameter and cross-section, '
                'material and hardness.', st['p']),
      Paragraph('5. Flareless nut 0618 and sleeve 0619 - 4 parts', st['h1']),
      Paragraph(f'{", ".join(grp[G_FL])}. Brennan sells a flareless nut V0318 and sleeve V0319 in the same sizes. Are yours the same parts? '
                'If yes, we use Brennan\'s 3D files; if not, please send length, hex, inside and outside diameters and the shape (a drawing or '
                'a photo with sizes).', st['p']),
      Paragraph('6. FS0319-24 face-seal sleeve - which outside diameter?', st['h1']),
      Paragraph('Air-Way prints 1.71 for the sleeve, but its own -24 female face-seal end (FF2407-24) is 2.00; Brennan prints 1.910. Which '
                'is right for your part?', st['p'])]


def build_pdf(path):
    SimpleDocTemplate(path, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                      title='Parts we have no dimensions for', author='OMi fitting library').build(S, onFirstPage=footer, onLaterPages=footer)


PDF = os.path.join(OUT, f'OMi_parts_without_dimensions_{DATE}.pdf'); build_pdf(PDF)

# ---------------------------------------------------------------- workbook (fill-in)
wb = openpyxl.Workbook(); YEL = PatternFill('solid', fgColor='FFF2A8'); GRY = PatternFill('solid', fgColor='E4E7EB')
thin = Side(style='thin', color='CBD2D9'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
COLS = ['Overall Length', 'M 1 Size', 'L 1 Size', 'Hex Flat', 'Side 1 ID', 'Side 2 ID', 'Side 3 ID', 'Nut Hex 1', 'Other (see "What we need")']


def sheet(ws, title, note, items):
    ws.title = title; ws['A1'] = note; ws['A1'].alignment = Alignment(wrap_text=True, vertical='top'); ws.merge_cells('A1:M1')
    ws.row_dimensions[1].height = 48
    head = ['#', 'Part number', 'Description (your file)', 'What we need'] + COLS + ['Your notes']
    for j, h in enumerate(head, 1):
        c = ws.cell(row=2, column=j, value=h); c.font = Font(bold=True); c.fill = GRY; c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for i, (p, d, n) in enumerate(items, 1):
        vals = [i, p, d, n]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i + 2, column=j, value=v); c.border = BOX; c.alignment = Alignment(wrap_text=True, vertical='top')
        for j, col in enumerate(COLS, 5):
            c = ws.cell(row=i + 2, column=j); c.border = BOX
            key = col.split(' (')[0]
            wanted = key in n or (key == 'Other' and re.search(r'length|orifice|insert|flange|Same as|thread|shape|branch|test-port', n))
            c.fill = YEL if wanted else GRY
        ws.cell(row=i + 2, column=len(head)).border = BOX
    for j, w in enumerate([4, 22, 34, 42] + [11] * len(COLS) + [28], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = 'C3'


comp_items = []
for s, v in comp.items():
    for p in v['parts'] + v['m1']:
        n = ('Body only: same as ' + p[:-3] + '? ' if p.endswith('-M1') else '') + (
            'Overall Length, Hex Flat, Side 1 ID, shape of the inside (a drawing)' if s == 'C0318' else
            'Overall Length, outside diameter, Side 1 ID, shape of the front edge (a drawing)' if s == 'C0319' else
            'M 1 Size, L 1 Size, Hex Flat, Side 1 ID, Side 2 ID' if re.match(r'C(25|26|68)', s) else 'Overall Length, Hex Flat, Side 1 ID, Side 2 ID')
        comp_items.append((p, desc.get(p, ''), n))
sheet(wb.active, 'Compression', 'Compression (bite-type) fittings. One supplier drawing per series with its size table is enough - then '
      'nothing needs to be filled in. Yellow = we need it, grey = not needed. Inches. Also: which standard does the bite-type port follow?', comp_items)
sheet(wb.create_sheet(), 'Test gauge', 'Test-gauge tees (-04 pipe test port). A drawing per series is enough. Yellow = we need it. Inches.', tg_rows)
sheet(wb.create_sheet(), 'Single sizes', 'Single sizes no catalog prints (the rest of each series is modelled). Yellow = we need it. Inches.',
      single_rows)
XLSX = os.path.join(OUT, f'OMi_parts_without_dimensions_{DATE}.xlsx'); wb.save(XLSX)

# ---------------------------------------------------------------- email
EMAIL = f"""DRAFT - not sent.

To: Triveni (OM Industrial)
Subject: Parts we have no dimensions for ({n_out} part numbers)

Hi Triveni,

We have now checked every part number on your website that is not modelled yet against Air-Way's catalog, Brennan's catalogs and 3D
files, and your website parts file. {n_out} of them appear in none of these with dimensions, so we cannot model them without your help.
The attached PDF lists them; the attached workbook has a yellow cell for each value we need, using your parts file's column names.

In short:
1. Compression (bite-type) fittings - {len(grp[G_COMP])} part numbers in {len(comp)} series. Brennan's 3D models cover
   {n_comp_brennan} of your compression fittings, and {n_comp_m1} more body-only numbers if each "(Body)" -M1 part is the
   same body without the nut and sleeve - is it? Supplier drawings would cover the rest. Which standard does the
   bite-type port follow?
2. Test-gauge tees TGT-6504 / TGT-FS2406 - 12 parts, two series.
3. {len(single_rows)} single sizes that no catalog prints and Brennan does not model (the rest of each series is modelled), e.g.
   1405-20-24, 2403-06-02, the 2700 bulkhead reducers, the 6500 / 6502 forged reducers and the FS0304-C cap assemblies. For the four
   2700-LN parts: are they the same as the plain 2700 part?
4. Flange O-ring 4005-48: code 61 or 62, I.D. x cross-section, material and hardness (Brennan models the other eight sizes).
5. Flareless nut 0618 and sleeve 0619 (4): are they the same parts as Brennan's V0318 / V0319?
6. FS0319-24 sleeve: Air-Way prints 1.71, Brennan 1.910, Air-Way's own -24 female face-seal end 2.00 - which is right?

Drawings are the easiest for you and for us; if you send drawings, the cells do not need filling in. Also, we are treating the kits
1901 / 1902 / 1927 as out of scope - please tell us if you need them modelled.

Best regards,
Sudhanva

Attachments:
- OMi_parts_without_dimensions_{DATE}.pdf
- OMi_parts_without_dimensions_{DATE}.xlsx
"""
open(os.path.join(OUT, f'Email_to_Triveni_{DATE}.txt'), 'w', encoding='utf-8').write(EMAIL)
print('parts on the list:', n_out, '| compression', len(grp[G_COMP]), 'of 230 (Brennan', n_comp_brennan, '+ M1', n_comp_m1, ')', '| singles', len(single_rows), '| TG', len(tg_rows), '| compression series', len(comp))
print(PDF); print(XLSX)
