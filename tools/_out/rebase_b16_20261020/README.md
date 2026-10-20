# Batch-17 work rebased on batch 16 (shipped at d63e1a6): regeneration from the new state (2026-10-20, cloud session)

The user asked (2026-10-20): rebase the branch on origin/main and regenerate the elbow roots and the 12 changed tables only from the new
state. Read-only for every table. Nothing is shipped.

## 1. The rebase
- The branch `claude/pensive-planck-t9i90d` is rebased on d63e1a6 (batch 16).
- There were two conflicts, as expected: `.gitignore` and the top of `00_DOCS/PROJECT_STATUS.md` section 1. Both sides were kept in each:
  - in `.gitignore`, the ship / puckfix includes come first, then the a14 lines;
  - in section 1, the 2026-10-20 A14 entry comes first, then the batch-16 entry.

## 2. The inputs, against the new state
- **Live `tools/` = the batch-16 toolset** (`puckfix_20261009/tools_new`), file for file (`gen_straight2.py.orig` aside).
  - The merged batch-17 tools (`genfeat_20261018/merged/tools`) were built on that toolset.
  - They carry the puck fix (`PUCK_INSET = 0.0005`).
- **The 12 shipped review tables vs their copies in the batch-17 stage** (`scripts/explain_tables.py` -> `explain_tables.txt`):
  - 206 cells / rows differ, **0 unexplained**;
  - each one is a logged batch-17 change that starts at the shipped value (`omi_answers_20261018/CHANGES.csv`, then `stage/CHANGES.csv`), a
    note appended to the shipped text, or a logged new row (2504-16-16-FG, 2505-04-04-FG, 2505-06-06-FG);
  - 6 A19 notes were written into empty `$COMMENT` cells. `apply_a19.py` did not log the notes, but it did log the dimension cells they
    describe.
  - So the stage holds no stale pre-ship copy of these tables. 0304 0306 2606 2609 6500L are identical.

## 3. Regeneration of the 24 batch-16 roots (`scripts/regen_b16roots.py`, `scripts/split_b.py`)
The 24 roots: every elbow root of the puck fix plus the 12 changed tables. 6500L folds into 6500. Each root runs in its own process.

| Run | Tools | Tables | Result |
|---|---|---|---|
| A | live `tools/` | live `04_DESIGN_TABLES` (shipped) | **24 of 24 identical** to the shipped `03_SCRIPTS` macros (date line aside) and `04_DESIGN_TABLES` SW2 (cell by cell) |
| C | merged batch-17 tools | shipped tables | **identical to A on all 24 roots** (macro and SW2): the batch-17 tool features change nothing here |
| B | merged batch-17 tools | batch-17 stage | 372 -> **417 configurations (+45 new), 0 dropped, no column added or lost** |

B vs C = data only (`split_b.txt`, `regen_b16roots.txt`):
- **New configurations (+45):**
  - 2501 +8, 5502 +7, 1502 +7, 5504 +4, 6801 +4, 2701 +3;
  - 2404 / 6505 / 6500 / 1501 +2 each;
  - 2611 / 2504 / 2505 / 6502 +1 each.
- **32 built configurations change geometry, and every one traces to an A19 cell** (the OMi values the user approved on 2026-10-18,
  groups 2 and 3): 6505 x13, 5502 x5, 2503 x3, 6500 x3, 6502 x3, 2501 x2 (one via `DesignTable_2501L.xlsx`), 5500 / 6501 / 6503 x1.
  0 untraced.
  - The changed SW2 cells are the A19 lengths and the cells derived from them (bore-cut depths, thread profile start, hex-body length,
    nose tip).
  - These masters need rebuilding in batch 17 (expected: ANSWERS_2026-10-18, A19).
- **34 built configurations change text / status only** (`$COMMENT`, DataStatus ASSUMED -> VERIFIED under A23).
- **Untouched:** 0304 0306 2606 2609 2702 6802. Every SW2 cell is the same and the macro is unchanged.

## 4. Static checks on the B macros (`checks/`)
- vbacheck: 24 of 24 OK.
- dofcheck_tee: all 46 legs fully defined, 0 redundant.
- dofcheck_straight: 0304 0306 2404 6505 fully defined, 0 redundant, apex on axis.
- allcfg_check: 0 outline problems on all 417 configurations (6502 neck turns: 12 checked; 6802 corner neck trims: 20 checked).

## Not here
- SolidWorks dry runs (PC only).
- The other batch-17 roots (the new masters 1601 1602 1603 6606 6807, the hose-barb / flange / angled / straight features). They are not
  in batch 16, so the ship does not touch their inputs (the tools are the same as live + the features).
- The regenerated macros (`regen/`, 8.5 MB) are not committed. Rerun `scripts/regen_b16roots.py` + `scripts/split_b.py` (about 1 minute).
