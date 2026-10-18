# Wave 3 ORFS - report (saved by the main session from the agent's hand-back, 2026-10-18)

110 ORFS rows; Brennan prints all of them (27 under another name: FS0304-C-xx-ASY = FS0304-C-xx, FS27xx-LN = the bare -FG part,
FS1700 / 1704 / 1800 / 1804 in the Flange catalog). All are ready=no (gate: ORFS model type).
- **DATA COMPLETE: 12.** FS0304-C x8, FS0306-04 / -12, FS0319-12, FS6505-04-04.
- **Partial: 97.**
  - 45 become complete if the user approves `cells_proposed.csv` (proposed **Q-FS-XFER**).
  - 54 lack only bores: Brennan's ORFS catalog prints bores only on FS6505 / FS6809.
  - L11 / L14 (20 rows) and L9 / L31 (4 rows) are not printed by Brennan.
  - FS1800 / 1804: code 62 heads beyond -08 are needed.
  - FS27xx -16: the bulkhead I2 / I4 / D17 are missing.
  - FS2406: collar D8 is missing.
  - FS6402-12-12: L is a misprint ("0.609").
  - FS7202: no BSPP thread data.
- **Held: 1.** FS0319-24 (Air-Way 1.71 / 2.00 vs Brennan 1.910; PLAN D5).

**Files**
- `cells.csv`: 922 cells - 375 brennan-dim, 184 endlib, 363 other.
- `cells_proposed.csv`: 154 cells, NOT applied (Q-FS-XFER). Per-dash bores, and L9 / L11 / L14 / L31 = Brennan leg - Air-Way stud length.
  A value is proposed only where the Air-Way rows agree unanimously: same table first, else the forged or straight tables of the same
  end type.
- `rows.csv`, `evidence/` (mapping, crosscheck, verify_apply), `tables/` (copies of the 51 FS tables, untouched), `test/04_DESIGN_TABLES`
  (cells applied: 109 rows marked BRENNAN, 0 set ASSUMED; verify_apply: 813 cells filled, all empty before).
- New columns where FS tables had none (FS0304-C, FS1700 / 1800 / 1704 / 1804, FS2601, FS6402, FS7202) and FS6502 L2@DRIVE.

**Mappings:** confirmed on same-table Air-Way rows for most series (FS6400 L 25 / 29, hex 27 / 29; FS2406 L 11 / 12, ...); the others
against related tables (details in `evidence/mapping.txt`).

**Conflicts (50 rows; `rows.csv`)**
- FS6505: Brennan L vs Air-Way L16 agree 0 / 3.
- FS6502: Brennan L2 vs Air-Way L52 agree 0 / 8 -> new column, L52 left empty.
- FS6809: Brennan hole 0.04-0.06 smaller than Air-Way d20.
- 36 forged rows: Brennan's forged values differ from the Air-Way plain row (not used).
- FS2601-10-10-08-FG: N 1.59 looks like a misprint.
- Swivel / reducer nut hexes agree with Air-Way FF318 S to rounding.

Note: the OMi-answers block of `apply_brennan.py` also wrote 19 DimSource cells on non-FS tables in the agent's test copy (harmless there;
the stage already has them).
