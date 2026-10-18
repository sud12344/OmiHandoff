"""
OMi professional fitting drawing template — A4 landscape (841.89 x 595.28 pt).

Built ON TOP of the customer-supplied OM_Industrial_Drawing_Template_A4.pdf.
Every coordinate from that file is preserved exactly as extracted:

    outer border      24, 24  ->  817.9, 571.3      (lw 1.6)
    title block       417.9, 24 -> 817.9, 136       (lw 1.6)
    tb row rules      y = 50, 76, 104               (lw 1.0)
    tb label/value    x = 683.9                     (lw 1.0)
    tb logo divider   x = 595.9                     (lw 1.0)
    zone ticks V      x = 123.2 222.5 321.7 420.9 520.2 619.4 718.7
    zone ticks H      y = 480.1 388.9 297.6 206.4 115.2
    logo underline    472.9,98 -> 540.9,98          (lw 1.2)

ADDED for professional fitting-drawing practice:
    * document-control strip (drawn / date / scale / rev / sheet)
    * general tolerance block + third-angle projection symbol
    * tabulated dimension table (18 rows) — one drawing serves a whole series
    * structured notes block with thread/material/finish callouts

Field names match Parts-sheet column headers so fill_specsheets.py maps directly.
"""
from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

W, H = 841.8898, 595.2756
NAVY = Color(0.114, 0.216, 0.373)
GREY = Color(0.35, 0.35, 0.35)
FBG  = Color(0.975, 0.978, 0.988)
RULE = Color(0.72, 0.72, 0.72)

# --- geometry from the supplied template, unchanged -------------------------
BX0, BY0, BX1, BY1 = 24.0, 24.0, 817.9, 571.3
TB_X0, TB_Y0, TB_Y1 = 417.9, 24.0, 136.0
TB_LOGO_DIV, TB_LBL_DIV = 595.9, 683.9
TB_ROWS = (50.0, 76.0, 104.0)
ZV = (123.2, 222.5, 321.7, 420.9, 520.2, 619.4, 718.7)
ZH = (480.1, 388.9, 297.6, 206.4, 115.2)

# --- added blocks -----------------------------------------------------------
DOC_Y0, DOC_Y1 = 136.0, 168.0          # drawn / date / scale / rev / sheet
TOL_Y0, TOL_Y1 = 168.0, 222.0          # tolerances + projection
TAB_X0, TAB_Y0, TAB_Y1 = 530.0, 232.0, 565.0
TAB_ROWS = 18

FIELDS = []


def fld(c, name, x, y, w, h, tip="", size=7.5, ml=60):
    FIELDS.append(name)
    c.acroForm.textfield(
        name=name, tooltip=tip or name, x=x, y=y, width=w, height=h,
        borderStyle="solid", borderWidth=0, borderColor=white, fillColor=FBG,
        textColor=black, forceBorder=False, fontName="Helvetica", fontSize=size,
        value="", maxlen=ml, annotationFlags="print",
    )


def lbl(c, x, y, t, size=5.5):
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(GREY)
    c.drawString(x, y, t)


def build(path):
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle("OM Industrial — Fitting Drawing Template A4")
    c.setAuthor("OM Industrial Products Corp.")

    # ================= original border + zones =================
    c.setStrokeColor(black)
    c.setLineWidth(1.6)
    c.rect(BX0, BY0, BX1 - BX0, BY1 - BY0, stroke=1, fill=0)

    c.setLineWidth(0.6)
    for x in ZV:
        c.line(x, BY1, x, BY1 + 6)
        c.line(x, BY0 - 6, x, BY0)
    for y in ZH:
        c.line(BX0 - 6, y, BX0, y)
        c.line(BX1, y, BX1 + 6, y)

    c.setFont("Helvetica", 7)
    c.setFillColor(black)
    nx = [71.7, 170.9, 270.1, 369.4, 468.6, 567.9, 667.1, 766.3]
    for i, x in enumerate(nx):
        s = str(8 - i)
        c.drawString(x, H - 17.4, s)
        c.drawString(x, 8.6, s)
    for letter, ytop in zip("FEDCBA", (66.1, 157.3, 248.5, 339.7, 430.9, 522.1)):
        yy = H - ytop - 7
        c.drawString(9.6, yy, letter)
        c.drawString(827.6, yy, letter)

    # ================= title block (original) =================
    c.setLineWidth(1.6)
    c.rect(TB_X0, TB_Y0, BX1 - TB_X0, TB_Y1 - TB_Y0, stroke=1, fill=0)
    c.setLineWidth(1.0)
    c.line(TB_LOGO_DIV, TB_Y0, TB_LOGO_DIV, TB_Y1)
    for y in TB_ROWS:
        c.line(TB_LOGO_DIV, y, BX1, y)
    for y0, y1 in ((TB_Y0, 50.0), (50.0, 76.0), (76.0, 104.0), (104.0, TB_Y1)):
        c.line(TB_LBL_DIV, y0, TB_LBL_DIV, y1)

    # logo block — reproduced from the supplied file
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(506.9, 106.0, "OM")
    c.setLineWidth(1.2)
    c.setStrokeColor(NAVY)
    c.line(472.9, 98.0, 540.9, 98.0)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(506.9, 84.5, "OM INDUSTRIAL PRODUCTS CORP.")
    c.setFillColor(black)
    c.setFont("Helvetica", 7.5)
    for i, t in enumerate(("3334 Creekmont Drive", "Houston, TX 77091, USA",
                           "Ph: 713-462-7900  |  1-888-663-4884",
                           "sales@omindustrial.com")):
        c.drawCentredString(506.9, 71.0 - i * 10.5, t)

    c.setStrokeColor(black)
    tb = (("PART NUMBER", "PartNumber_OMi", 104.0, TB_Y1, 9),
          ("DESCRIPTION", "Description", 76.0, 104.0, 7),
          ("MATERIAL", "Material", 50.0, 76.0, 7),
          ("FINISH / COATING", "Finish", TB_Y0, 50.0, 7))
    for label, name, y0, y1, fs in tb:
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(black)
        c.drawString(TB_LOGO_DIV + 5, y1 - 10, label)
        fld(c, name, TB_LBL_DIV + 2, y0 + 3, BX1 - TB_LBL_DIV - 5,
            y1 - y0 - 6, label, size=fs, ml=90)

    # ================= document control strip =================
    c.setLineWidth(1.6)
    c.rect(TB_X0, DOC_Y0, BX1 - TB_X0, DOC_Y1 - DOC_Y0, stroke=1, fill=0)
    c.setLineWidth(1.0)
    doc = (("DRAWN BY", "PreparedBy"), ("CHECKED", "ApprovedBy"),
           ("DATE", "IssueDate"), ("SCALE", "Scale"),
           ("REV", "Revision"), ("SHEET", "Sheet"))
    cw = (BX1 - TB_X0) / len(doc)
    for i, (label, name) in enumerate(doc):
        x = TB_X0 + i * cw
        if i:
            c.line(x, DOC_Y0, x, DOC_Y1)
        lbl(c, x + 4, DOC_Y1 - 9, label)
        fld(c, name, x + 3, DOC_Y0 + 3, cw - 6, 14, label, size=7, ml=24)

    # ================= tolerance + projection =================
    c.setLineWidth(1.6)
    c.rect(TB_X0, TOL_Y0, BX1 - TB_X0, TOL_Y1 - TOL_Y0, stroke=1, fill=0)
    projx = BX1 - 96
    c.setLineWidth(1.0)
    c.line(projx, TOL_Y0, projx, TOL_Y1)

    lbl(c, TB_X0 + 5, TOL_Y1 - 10, "UNLESS OTHERWISE SPECIFIED — GENERAL TOLERANCES")
    c.setFont("Helvetica", 6.2)
    c.setFillColor(black)
    tol = ("DECIMALS  .X = ±0.030    .XX = ±0.015    .XXX = ±0.005",
           "ANGLES  ±0°30'     THREADS PER APPLICABLE STANDARD",
           "SURFACE FINISH 125 MICROIN. Ra     BREAK SHARP EDGES 0.010 MAX",
           "SEAT ANGLE TOLERANCE ±0°15'   CONCENTRICITY 0.010 TIR")
    for i, t in enumerate(tol):
        c.drawString(TB_X0 + 6, TOL_Y1 - 21 - i * 8.2, t)

    # third-angle projection symbol
    lbl(c, projx + 5, TOL_Y1 - 10, "THIRD ANGLE PROJECTION")
    cy = TOL_Y0 + 22
    cx = projx + 30
    c.setLineWidth(0.8)
    c.circle(cx, cy, 10, stroke=1, fill=0)
    c.circle(cx, cy, 4.5, stroke=1, fill=0)
    tx = projx + 62
    c.lines([(tx - 12, cy - 10, tx + 12, cy - 6), (tx + 12, cy - 6, tx + 12, cy + 6),
             (tx + 12, cy + 6, tx - 12, cy + 10), (tx - 12, cy + 10, tx - 12, cy - 10)])
    c.setDash(2, 2)
    c.line(cx, cy - 13, cx, cy + 13)
    c.line(cx - 13, cy, cx + 13, cy)
    c.setDash()

    # ================= tabulated dimension table =================
    cols = (("PART NUMBER", 62, "PN"), ("TUBE\nOD", 32, "OD"),
            ("THREAD B (JIC)", 52, "THDB"), ("THREAD A (NPTF)", 52, "THDA"),
            ("L", 30, "L"), ("C", 30, "C"), ("HEX", 30, "HEX"))
    tw = sum(x[1] for x in cols)
    tx1 = TAB_X0 + tw
    rh = (TAB_Y1 - TAB_Y0) / (TAB_ROWS + 2)

    c.setLineWidth(1.6)
    c.rect(TAB_X0, TAB_Y0, tw, TAB_Y1 - TAB_Y0, stroke=1, fill=0)

    # table caption row
    c.setFillColor(NAVY)
    c.rect(TAB_X0, TAB_Y1 - rh, tw, rh, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(TAB_X0 + tw / 2, TAB_Y1 - rh + 4, "DIMENSIONS — INCHES")

    hy = TAB_Y1 - 2 * rh
    c.setStrokeColor(black)
    c.setLineWidth(1.0)
    c.line(TAB_X0, hy, tx1, hy)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 5.6)
    xx = TAB_X0
    for name, cwid, _ in cols:
        parts = name.split("\n")
        for k, pt in enumerate(parts):
            c.drawCentredString(xx + cwid / 2, hy + rh - 8 - k * 6 + (3 if len(parts) > 1 else 0), pt)
        xx += cwid
        if xx < tx1 - 0.5:
            c.setLineWidth(0.6)
            c.line(xx, TAB_Y0, xx, TAB_Y1 - rh)

    c.setLineWidth(0.4)
    c.setStrokeColor(RULE)
    for r in range(TAB_ROWS):
        ry = hy - (r + 1) * rh
        if r < TAB_ROWS - 1:
            c.line(TAB_X0, ry, tx1, ry)
        xx = TAB_X0
        for _, cwid, key in cols:
            fld(c, f"TBL{r+1:02d}_{key}", xx + 1, ry + 1.5, cwid - 2, rh - 3,
                f"Row {r+1} {key}", size=5.6, ml=22)
            xx += cwid

    # ================= notes block =================
    c.setStrokeColor(black)
    c.setLineWidth(1.6)
    c.rect(BX0, TB_Y0, TB_X0 - BX0, TB_Y1 - TB_Y0, stroke=1, fill=0)
    lbl(c, BX0 + 6, TB_Y1 - 11, "NOTES", 6.5)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(black)
    c.drawString(BX0 + 6, TB_Y1 - 24,
                 "1.  ALL DIMENSIONS IN INCHES UNLESS OTHERWISE SPECIFIED.  DO NOT SCALE DRAWING.")
    notes = (("2.  END A THREAD PER", "EndA_ThreadStd", 37),
             ("3.  END B THREAD PER", "EndB_ThreadStd", 50),
             ("4.  MATERIAL PER", "MaterialSpec", 63),
             ("5.  FINISH PER", "FinishSpec", 76))
    for text, name, dy in notes:
        y = TB_Y1 - 24 - (dy - 24)
        c.setFont("Helvetica", 6.5)
        c.drawString(BX0 + 6, y, text)
        fld(c, name, BX0 + 108, y - 3, 180, 11, text, size=6.5, ml=60)
    c.setFont("Helvetica", 6.5)
    c.drawString(BX0 + 6, TB_Y1 - 89, "6.")
    fld(c, "Notes", BX0 + 20, TB_Y1 - 100, TB_X0 - BX0 - 30, 22, "Additional notes",
        size=6.5, ml=200)
    c.setFont("Helvetica-Bold", 6)
    c.setFillColor(GREY)
    c.drawString(BX0 + 6, TB_Y0 + 5, "DATA STATUS:")
    fld(c, "DataStatus", BX0 + 62, TB_Y0 + 2, 80, 10, "VERIFIED / ASSUMED / MISSING",
        size=6, ml=20)
    c.drawString(BX0 + 150, TB_Y0 + 5, "STD CHECK:")
    fld(c, "StdCheck_Result", BX0 + 196, TB_Y0 + 2, 90, 10, "MATCH / DIVERGENT", size=6, ml=24)
    c.drawString(BX0 + 292, TB_Y0 + 5, "GEOM ROOT:")
    fld(c, "GeometryRoot", BX0 + 340, TB_Y0 + 2, 50, 10, "Master model key", size=6, ml=16)

    c.save()
    return FIELDS


if __name__ == "__main__":
    f = build("/home/claude/phase0/OMi_DrawingTemplate_Pro_A4.pdf")
    print(f"{len(f)} fillable fields")
    print("title/meta:", [x for x in f if not x.startswith("TBL")])
