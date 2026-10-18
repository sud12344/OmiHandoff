# Next session - start here (written 2026-10-09, session stopped by the user)

Read `CLAUDE.md`, then this file. Keep usage low (user's request).

## Done 2026-10-09 (this session)
- SolidWorks dry runs of everything staged: 2404 (57 cfg) + 0304 0306 2504 1502 6500 6501 6505 2505 2606 2609 2611 5405.
  All 0 FAIL, 1 body per configuration. Old configurations identical: 6500 / 6501 / 6505 vs 11_MASTERS, 5405 vs a read-only sweep of
  its master, 2404's 24 kept rows vs the tier-1 dry run. Evidence: `tools/_out/wave1_ship_20261009/swtest/` (`cmp_out.txt`,
  `cmp_expected_out.txt`, `shots/contact_*.png`, `calls/out_all.txt`), 2404 in `tools/_out/r2404_20261009/swtest/`.
- **DEFECT FOUND: corner PUCK silently dropped** (outer elbow corner left square, no error). Cause: the puck equator = hex corner
  radius exactly, its section = the hex-arm end face. Read-only audit of the 16 shipped elbow masters
  (`tools/_out/puck_audit_20261009/`, `audit_rows.json`): 16 shipped configurations lack it (2501-06-02 / -L-06-04, 2503-06-04,
  2701-02-02 / -06-06 / -06-06-LN, 2702-06-06 / -LN, 6500-06-04 / -06-06, 6502-06-06, 6801-06-04 / -06-05 / -06-06, 6802-06-04 / -06-06)
  + 4 new staged ones (2504-04-04 / -06-06, 6500-L-04-04 / -L-06-06).
- Candidate fix (NOT live): `tools/_out/puckfix_20261009/tools_new` = wave1_ship tools + `PUCK_INSET = 0.0005` (puck 0.0005 radially
  inside the hex corners, 30 deg kept). Regen-all: only the puck lines / 3 PUCK columns change, in the 17 elbow roots
  (`regen/cmp.txt`). Tested by hand on 2504-04-04 / -06-06: corner comes back (= OCP volume).

## Interrupted (re-run)
- Dry runs of the 17 elbow roots with the fix: `python sw_mcp/call.py @tools/_out/puckfix_20261009/calls_dryrun.json >
  tools/_out/puckfix_20261009/out_dryrun.txt` (may have finished on its own - check the file / `sw_dryrun/<root>/` reports), then
  `python tools/_out/puckfix_20261009/cmp_dryrun.py`.
- Wave-2 implementation agent (PERLEGSW then HOSEB) was STOPPED part-way: workspace `tools/_out/wave2_impl_20261009/` (partial; check
  its REPORT.md if any, otherwise restart from the designs in `tools/_out/wave2_shapes_20261008/`).

## Then
1. If the puck dry runs pass: ask the user to ship batch 16 = staged wave 1 + leftovers + JIC tees + 2404 + 5405 + the puck fix
   (re-ship of the 14 affected shipped elbow masters). Nothing is in `11_MASTERS_NEW` yet.
2. Tell the user: 2505-08-08-FG / -16-16-FG stay blocked (library port depth deeper than the short leg); HOSEB bore option (a) is an
   assumption until Q-HOSEB-BORE.
