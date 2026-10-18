"""
Builds OMi_SpecSheet_Template.pdf — a fillable AcroForm spec sheet.

Every field name matches a column header in the Parts sheet of
OMi_Fitting_Library_MasterData_v1.xlsx exactly, so the fill mechanism is a
direct 1:1 mapping with no translation layer.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

W, H = letter
NAVY   = Color(0.122, 0.220, 0.392)
LGREY  = Color(0.90, 0.90, 0.90)
MGREY  = Color(0.45, 0.45, 0.45)
RULE   = Color(0.75, 0.75, 0.75)
FIELD_BG = Color(0.97, 0.975, 0.99)

M   = 40           # page margin
FS  = 8            # field font size
LBL = 6.5          # label font size
RH  = 19           # row height

FIELDS = []        # (name, tooltip) collected for the manifest


def label(c, x, y, text):
    c.setFont("Helvetica-Bold", LBL)
    c.setFillColor(MGREY)
    c.drawString(x, y, text.upper())


def field(c, name, x, y, w, h=13, tip="", value="", align=0, maxlen=120):
    """Draw one AcroForm text field."""
    FIELDS.append((name, tip or name))
    c.acroForm.textfield(
        name=name, tooltip=tip or name,
        x=x, y=y, width=w, height=h,
        borderStyle="underlined", borderWidth=0.6,
        borderColor=RULE, fillColor=FIELD_BG, textColor=black,
        forceBorder=True, fontName="Helvetica", fontSize=FS,
        value=value, maxlen=maxlen, fieldFlags="", annotationFlags="print",
    )


def section(c, y, title):
    c.setFillColor(NAVY)
    c.rect(M, y, W - 2 * M, 14, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(M + 6, y + 4, title.upper())
    return y - 6


def build(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle("OM Industrial — Product Specification Sheet")
    c.setAuthor("OM Industrial Products Corp.")
    c.setSubject("Hydraulic fitting specification (fillable template)")

    # ---------------- header ----------------
    y = H - M
    c.setFillColor(NAVY)
    c.rect(M, y - 40, W - 2 * M, 40, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(M + 10, y - 19, "OM INDUSTRIAL PRODUCTS CORP.")
    c.setFont("Helvetica", 8)
    c.drawString(M + 10, y - 32, "Hydraulic & Industrial Fittings")
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(W - M - 10, y - 19, "PRODUCT SPECIFICATION")
    c.setFont("Helvetica", 7)
    c.drawRightString(W - M - 10, y - 32, "omindustrial.com")

    y -= 56

    # ---------------- identification ----------------
    y = section(c, y, "Identification")
    y -= 20
    label(c, M, y + 19, "Part Number")
    field(c, "PartNumber_OMi", M, y, 150, 15, "OM Industrial part number", maxlen=40)
    label(c, M + 160, y + 19, "Geometry Root")
    field(c, "GeometryRoot", M + 160, y, 80, 15, "Shared topology key / master model ID", maxlen=20)
    label(c, M + 250, y + 19, "Category")
    field(c, "Category", M + 250, y, 130, 15, "Product family")
    label(c, M + 390, y + 19, "Shape")
    field(c, "Shape", M + 390, y, 90, 15, "Straight / 90 / 45 / Tee / Cross")

    y -= RH + 11
    label(c, M, y + 19, "Description")
    field(c, "Description", M, y, 340, 15, "Full product description", maxlen=200)
    label(c, M + 350, y + 19, "Cross-Reference P/N")
    field(c, "PartNumber_AirWay", M + 350, y, 130, 15, "Interchange / cross-reference number")

    y -= RH + 8

    # ---------------- end A / end B ----------------
    y = section(c, y, "End Connections")
    y -= 18

    col = [M, M + 90, M + 190, M + 300, M + 410]
    hdr = ["", "End Type", "Dash Size", "Thread", "Thread Standard"]
    c.setFont("Helvetica-Bold", LBL)
    c.setFillColor(MGREY)
    for i, h in enumerate(hdr):
        if h:
            c.drawString(col[i], y + 14, h.upper())

    for tag in ("EndA", "EndB"):
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(NAVY)
        c.drawString(M, y + 3, "END " + tag[-1])
        field(c, f"{tag}_Type",      col[1], y, 95, 13, f"{tag} connection style")
        field(c, f"{tag}_DashSize",  col[2], y, 55, 13, f"{tag} dash size", maxlen=10)
        field(c, f"{tag}_Thread",    col[3], y, 105, 13, f"{tag} thread callout")
        field(c, f"{tag}_ThreadStd", col[4], y, 105, 13, f"{tag} governing thread standard")
        y -= RH

    y -= 2
    label(c, M, y + 14, "Seat Angle — End A")
    field(c, "EndA_SeatAngle_deg", M, y, 150, 13, "End A seat half-angle, or N/A for tapered thread")
    label(c, M + 250, y + 14, "Seat Angle — End B")
    field(c, "EndB_SeatAngle_deg", M + 250, y, 150, 13, "End B seat half-angle in degrees")

    y -= RH + 8

    # ---------------- dimensions ----------------
    y = section(c, y, "Dimensions  (inches unless noted)")
    y -= 20
    dims = [("D_L", "L — Overall Length"), ("D_C", "C"), ("D_D", "D"), ("D_D1", "D1")]
    x = M
    for name, lab in dims:
        label(c, x, y + 19, lab)
        field(c, name, x, y, 105, 15, lab, maxlen=20)
        x += 120
    y -= RH + 11
    dims2 = [("D_HEXA", "Hex A — Across Flats"), ("D_HEXB", "Hex B — Across Flats"),
             ("D_TubeOD", "Tube OD"), ("D_BendAngle_deg", "Bend Angle (deg)")]
    x = M
    for name, lab in dims2:
        label(c, x, y + 19, lab)
        field(c, name, x, y, 105, 15, lab, maxlen=20)
        x += 120

    y -= RH + 8

    # ---------------- material ----------------
    y = section(c, y, "Material & Finish")
    y -= 20
    label(c, M, y + 19, "Material")
    field(c, "Material", M, y, 210, 15, "Base material")
    label(c, M + 225, y + 19, "Material Specification")
    field(c, "MaterialSpec", M + 225, y, 255, 15, "e.g. ASTM A108 Gr 12L14")
    y -= RH + 11
    label(c, M, y + 19, "Finish / Plating")
    field(c, "Finish", M, y, 210, 15, "Surface finish or plating")
    label(c, M + 225, y + 19, "Finish Specification")
    field(c, "FinishSpec", M + 225, y, 255, 15, "e.g. ASTM F1941")

    y -= RH + 8

    # ---------------- performance ----------------
    y = section(c, y, "Performance")
    y -= 20
    perf = [("PressureRating", "Working Pressure"), ("PressureUnit", "Unit"),
            ("TempMin_F", "Min Temp (F)"), ("TempMax_F", "Max Temp (F)")]
    x = M
    for name, lab in perf:
        label(c, x, y + 19, lab)
        field(c, name, x, y, 105, 15, lab, maxlen=20)
        x += 120

    y -= RH + 8

    # ---------------- document control ----------------
    y = section(c, y, "Document Control")
    y -= 20
    label(c, M, y + 19, "Drawing No.")
    field(c, "DrawingNo", M, y, 130, 15, "Drawing number")
    label(c, M + 140, y + 19, "Revision")
    field(c, "Revision", M + 140, y, 50, 15, "Revision level", maxlen=8)
    label(c, M + 200, y + 19, "Date")
    field(c, "IssueDate", M + 200, y, 90, 15, "Issue date", maxlen=20)
    label(c, M + 300, y + 19, "Prepared By")
    field(c, "PreparedBy", M + 300, y, 85, 15, "Preparer")
    label(c, M + 395, y + 19, "Approved By")
    field(c, "ApprovedBy", M + 395, y, 85, 15, "Approver")

    y -= RH + 11
    label(c, M, y + 19, "Data Status")
    field(c, "DataStatus", M, y, 100, 15, "VERIFIED / ASSUMED / MISSING", maxlen=20)
    label(c, M + 110, y + 19, "Standards Check")
    field(c, "StdCheck_Result", M + 110, y, 120, 15, "MATCH / DIVERGENT / UNVERIFIABLE")
    label(c, M + 240, y + 19, "Source Reference")
    field(c, "SourceURL", M + 240, y, 240, 15, "Source of dimensional data", maxlen=250)

    y -= RH + 6

    # ---------------- notes ----------------
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(M, y - 46, W - 2 * M, 52, stroke=1, fill=0)
    label(c, M + 5, y - 3, "Notes")
    FIELDS.append(("Notes", "Free-text notes"))
    c.acroForm.textfield(
        name="Notes", tooltip="Free-text notes", x=M + 4, y=y - 44, width=W - 2 * M - 8,
        height=38, borderStyle="solid", borderWidth=0, borderColor=white,
        fillColor=white, textColor=black, forceBorder=False,
        fontName="Helvetica", fontSize=7.5, fieldFlags="multiline",
        annotationFlags="print", maxlen=600,
    )

    # ---------------- drawing reference ----------------
    y -= 60
    y = section(c, y, "Dimensional Reference")
    box_top = y - 4
    box_h = box_top - (M + 34)
    c.setStrokeColor(RULE)
    c.setDash(2, 2)
    c.setLineWidth(0.7)
    c.rect(M, M + 34, W - 2 * M, box_h, stroke=1, fill=0)
    c.setDash()
    c.setFont("Helvetica-Oblique", 7.5)
    c.setFillColor(MGREY)
    c.drawCentredString(W / 2, M + 34 + box_h / 2 + 4,
                        "Dimensional drawing placeholder")
    c.drawCentredString(W / 2, M + 34 + box_h / 2 - 6,
                        "The batch macro stamps the exported drawing PDF into this area.")

    # ---------------- footer ----------------
    c.setStrokeColor(RULE)
    c.setLineWidth(0.5)
    c.line(M, M + 22, W - M, M + 22)
    c.setFont("Helvetica", 6)
    c.setFillColor(MGREY)
    c.drawString(M, M + 13,
                 "Dimensions are nominal and subject to standard manufacturing tolerances. "
                 "Values marked ASSUMED are not standards-verified and are not released for production.")
    c.drawString(M, M + 5, "OM Industrial Products Corp.  ·  omindustrial.com")
    c.drawRightString(W - M, M + 5, "Form OMi-SPEC-01  ·  Page 1 of 1")

    c.save()
    return FIELDS


if __name__ == "__main__":
    fields = build("/home/claude/phase0/OMi_SpecSheet_Template.pdf")
    print(f"created template with {len(fields)} fillable fields")
    for n, t in fields:
        print("  ", n)
