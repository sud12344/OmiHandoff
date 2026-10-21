# Not-ready parts: sources, STEP checklist, OMi package (2026-10-21, cloud)

Nothing here changes a review table, a macro or a master. Re-run any script with `python -I <script>` from the repo root.

| File | What |
|---|---|
| `not_ready_1022.txt` | OMi parts not in a shipped master and not generated in the committed staging = the PC's 987 (`tools/_out/blocked_needs_20261020/BLOCKED_NEEDS.md`) + its 35 held configurations |
| `source_lookup.py` -> `sources.csv`, `sources_summary.json` | each of the 1,022 checked against the Air-Way extracts (+ the ORFS FF... map), the Brennan PDF catalogs, the Brennan STEPs in `09_STEP_FILES` and OMi's website file; exact / alias / near-match, plus the review-table row |
| `step_checklist.py` -> `STEP_CHECKLIST.md` / `.csv` | the PC's 240-file Brennan download list as exact `BRENNAN_<pn>.stp` names, priority order, the not-ready parts of each size; re-run after downloading: ticks arrivals, flags misnamed files / a STEP whose PRODUCT names another part |
| `triveni_package.py` -> `10_DRAWINGS/for_OMi_2026-10-21/` | PDF + fill-in workbook + email draft (NOT sent) for the 290 parts no source prints |

## Cross-check against the PC's BLOCKED_NEEDS.md (987 parts)
- Agrees on every part's category, except:
  - **6505-04-02** (PC: "no source anywhere"): OMi's website file prints Overall Length, L 1, Hex, Side 1 / 2 ID and Nut Hex 1 -> it has a
    source (ASSUMED, OMi file); left off the OMi package.
  - **11 parts on the PC's download list that no catalog prints** (1504-32-32-FG, 5404-L-04X3.000 / X4.000, 5503-04-02 / 06-04 / 08-06 /
    12-08 / 16-12-FG, 5652-32-32-32-32-FG, 6566-16-16-FG, 6806-12-08-NWO-FG): only a Brennan portal file would give them sizes. If
    Brennan has no file, they join the OMi list.
  - 5404-N-06X4.500 / -08X5.500: no printed source, but A4 (Q-TRANSFER-5404N = yes) covers them - the PC's "generator work" is right.
- The OMi package = PC category (b) 291 - 6505-04-02 = 290: compression 230 (11 series, -M1 = body only), test gauge 12, 34 single sizes
  (28 adapters + 6 ORFS; the 4 2700-LN asked as "same as the plain part?", A10), 4005 x9, 0618 / 0619 x4 (= Brennan V0318 / V0319?),
  FS0319-24 (three printed values disagree).
- Not in the package (for the user, not OMi): bent tubes (68, PC question 1), the kits (30, out of scope - one line in the email asks
  OMi to confirm), the remaining PC "questions for OMi" 6-9 (FS2408 hole, 6420-12-12 body, bent-tube cross-check, 2026-10-09 chase).
- The unsent 2026-10-14 size request (`10_DRAWINGS/for_OMi_2026-10-14/`, O-rings / bent tubes / flareless) overlaps items 4-5; send one
  or merge.
