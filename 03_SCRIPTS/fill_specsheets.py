#!/usr/bin/env python3
"""
OMi SPEC SHEET AUTO-FILL  —  Phase 1d mechanism.

Reads the Parts sheet of the master workbook and writes one filled spec sheet
per part, using OMi_SpecSheet_Template.pdf.

The template's AcroForm field names are IDENTICAL to the Parts sheet column
headers, so the mapping is automatic. Only fields that exist in both are
touched; anything else is reported, never guessed.

Usage
-----
  python fill_specsheets.py --dry-run                  # report only, write nothing
  python fill_specsheets.py                            # fill all releasable rows
  python fill_specsheets.py --part 2404-08-06          # one part
  python fill_specsheets.py --allow-unverified         # include MISSING-data rows
  python fill_specsheets.py --out ./sheets             # output directory

Safety
------
  * Dry-run prints exactly what would be written and exits.
  * Rows whose DataStatus is not VERIFIED or ASSUMED are SKIPPED by default.
    This is the same gate the VBA macro uses. A MISSING-data part cannot
    silently become a released document.
  * Existing files are never overwritten unless --overwrite is given.
  * Every run writes a timestamped log next to the output.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

from openpyxl import load_workbook
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
DEFAULT_WB = HERE / "OMi_Fitting_Library_MasterData_v1.xlsx"
DEFAULT_TPL = HERE / "OMi_SpecSheet_Template.pdf"

RELEASABLE = {"VERIFIED", "ASSUMED"}

# Template fields that are not Parts-sheet columns; supplied per run.
RUN_FIELDS = ("DrawingNo", "Revision", "IssueDate", "PreparedBy", "ApprovedBy")


def log(msg: str, handle=None) -> None:
    print(msg)
    if handle:
        handle.write(msg + "\n")


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


def load_parts(wb_path: Path):
    """Return (headers, rows) from the Parts sheet, header row = row 2."""
    wb = load_workbook(wb_path, data_only=True)
    if "Parts" not in wb.sheetnames:
        raise SystemExit(f"No 'Parts' sheet in {wb_path}")
    ws = wb["Parts"]
    headers = [ws.cell(2, c).value for c in range(1, ws.max_column + 1)]
    rows = []
    for r in range(3, ws.max_row + 1):
        rec = {}
        for c, h in enumerate(headers, 1):
            if h:
                rec[str(h)] = ws.cell(r, c).value
        if rec.get("PartNumber_OMi"):
            rows.append(rec)
    return headers, rows


def template_fields(tpl_path: Path) -> set[str]:
    fields = PdfReader(str(tpl_path)).get_fields() or {}
    return set(fields.keys())


def fill_one(tpl_path: Path, out_path: Path, values: dict) -> None:
    reader = PdfReader(str(tpl_path))
    writer = PdfWriter()
    writer.append(reader)
    writer.set_need_appearances_writer(True)
    for page in writer.pages:
        writer.update_page_form_field_values(page, values)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as fh:
        writer.write(fh)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Fill OMi spec sheets from the master workbook.")
    ap.add_argument("--workbook", type=Path, default=DEFAULT_WB)
    ap.add_argument("--template", type=Path, default=DEFAULT_TPL)
    ap.add_argument("--out", type=Path, default=HERE / "specsheets")
    ap.add_argument("--part", help="Fill only this PartNumber_OMi")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--allow-unverified", action="store_true")
    ap.add_argument("--revision", default="A")
    ap.add_argument("--prepared-by", default="")
    ap.add_argument("--approved-by", default="")
    a = ap.parse_args(argv)

    for p in (a.workbook, a.template):
        if not p.exists():
            print(f"FATAL: not found: {p}", file=sys.stderr)
            return 2

    headers, rows = load_parts(a.workbook)
    tfields = template_fields(a.template)
    cols = {h for h in headers if h}

    mapped = sorted(tfields & cols)
    unmapped_t = sorted(tfields - cols - set(RUN_FIELDS))
    unused_c = sorted(cols - tfields)

    a.out.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    lg = open(a.out / f"fill_log_{stamp}.txt", "w", encoding="utf-8")

    log("=" * 66, lg)
    log("OMi SPEC SHEET FILL", lg)
    log(f"  workbook : {a.workbook.name}", lg)
    log(f"  template : {a.template.name}  ({len(tfields)} fields)", lg)
    log(f"  mode     : {'DRY RUN — nothing written' if a.dry_run else 'LIVE'}", lg)
    log(f"  gate     : {'OFF (all rows)' if a.allow_unverified else 'DataStatus in ' + str(sorted(RELEASABLE))}", lg)
    log("=" * 66, lg)
    log(f"Auto-mapped fields ({len(mapped)}): {', '.join(mapped)}", lg)
    if unmapped_t:
        log(f"Template fields with NO workbook column ({len(unmapped_t)}): {', '.join(unmapped_t)}", lg)
    if unused_c:
        log(f"Workbook columns not on the sheet ({len(unused_c)}) — informational only.", lg)
    log("", lg)

    todo = [r for r in rows if not a.part or str(r.get("PartNumber_OMi")) == a.part]
    if a.part and not todo:
        log(f"FATAL: part '{a.part}' not found in workbook.", lg)
        lg.close()
        return 3

    n_ok = n_skip = n_fail = 0
    for rec in todo:
        pn = str(rec["PartNumber_OMi"])
        status = str(rec.get("DataStatus") or "").strip().upper()

        if str(rec.get("ScopeAction", "BUILD")).upper() == "DROP":
            log(f"SKIP  {pn:<16} ScopeAction=DROP (not in the OMi carbon steel catalog)", lg)
            n_skip += 1
            continue

        if status not in RELEASABLE and not a.allow_unverified:
            log(f"SKIP  {pn:<16} DataStatus={status or '<blank>'}", lg)
            n_skip += 1
            continue

        out = a.out / f"{pn}_SPEC.pdf"
        if out.exists() and not a.overwrite:
            log(f"SKIP  {pn:<16} output exists (use --overwrite)", lg)
            n_skip += 1
            continue

        values = {k: fmt(rec.get(k)) for k in mapped}
        values["DrawingNo"] = pn
        values["Revision"] = a.revision
        values["IssueDate"] = _dt.date.today().isoformat()
        values["PreparedBy"] = a.prepared_by
        values["ApprovedBy"] = a.approved_by

        blanks = [k for k in ("Material", "Finish", "PressureRating", "D_HEXB") if not values.get(k)]
        note = f"AUTO-FILLED from master data. Incomplete: {', '.join(blanks)}." if blanks else ""
        if status == "ASSUMED":
            note = ("NOT STANDARDS-VERIFIED — one or more values are single-sourced. "
                    "Not released for production. " + note)
        values["Notes"] = note.strip()

        if a.dry_run:
            log(f"DRY   {pn:<16} status={status:<9} -> {out.name}"
                + (f"   [gaps: {', '.join(blanks)}]" if blanks else ""), lg)
            n_ok += 1
            continue

        try:
            fill_one(a.template, out, values)
            log(f"OK    {pn:<16} status={status:<9} -> {out.name}"
                + (f"   [gaps: {', '.join(blanks)}]" if blanks else ""), lg)
            n_ok += 1
        except Exception as exc:                      # noqa: BLE001
            log(f"FAIL  {pn:<16} {type(exc).__name__}: {exc}", lg)
            n_fail += 1

    log("", lg)
    log("=" * 66, lg)
    log(f"DONE   ok={n_ok}  skipped={n_skip}  failed={n_fail}", lg)
    log("=" * 66, lg)
    lg.close()
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
