# Batch 20 candidate (2026-10-21) - 5404N -06 thread fix + the 4 long nipples - STAGED, SolidWorks dry run NOT run yet

User paused SolidWorks use ("try not to do anything in solidworks for a bit, im running another project").

## Cause of QA #178 (5404N -06 THD_EndA / THD_EndB rebuild error 1)
SolidWorks probe on the batch-17 dry-run part (tools/_out/batch17_20261019/sw_dryrun/5404N), design table deleted in the throwaway copy so the
dimensions could be set (the earlier 2026-10-20 probe was invalid: the design table reset every value - and option 2 = ALL configurations):
- one -06 value at a time on the working -04 configuration: every one builds;
- cumulative: fails once the bar is above the -06 thread (BODYR 0.345 / 0.35 / 0.36 / 0.40 all fail, 0.28 builds);
- helix height: only exactly 0.4078 (= the thread length NPTF_THDL) fails; 0.36 / 0.38 / 0.39 / 0.395 / 0.40 / 0.4028 / 0.4048 / 0.4058 / 0.415
  build - the swept tooth ends on the shoulder edge where the crest cone meets the bar (the bar is only 0.004 above the crest there);
- with the helix 0.005 short: both ends build at every -06 length 2.0 ... 6.0.

## Changes (tools_b20 = live tools + one generator change; root20 = live tables + DesignTable_5404N.xlsx)
- `gen_straight2.py`: `ROUND_STEP_HELIX = 0.005`; on a round-bar-step end (the -06 rows, step < 0.005) the helix height = thread length - 0.005
  (logged in each row's AxialSource). Changes only the 7 -06 rows' HEIGHT@HELIX_A / _B (0.4078 -> 0.4028) + their source text.
- `DesignTable_5404N.xlsx`: the 4 long nipples 5404-N-06X4.500 / -06X5.500 / -08X2.500 / -08X5.500 filled by the A4 transfer their siblings
  carry (L from the part number, bar / bores / thread majors from the Air-Way nipple of the same dash), MISSING -> ASSUMED (CHANGES.csv, 29 cells).

## Checks done
- regen20.py: every root regenerated with tools_b20 on root20 - only 5404N changes (4 shipped configurations unchanged, +22 new: 18 held + 4);
  the 5 known pre-2026-09-25 roots differ as before (regen_cmp.txt).
- dofcheck: fully defined, 0 redundant; allcfg: 26 configurations, 0 outline problems; vbacheck OK.

## Next (when SolidWorks is free)
1. `python -u sw_mcp/call.py @tools/_out/batch20_20261021/dryrun/calls_5404N.json > tools/_out/batch20_20261021/dryrun/out_5404N.txt`
   (build into dryrun/5404N, sweep, then sweep the shipped 4-configuration master read-only). Expected: the reference-configuration
   "Body diameter 0.886 / 0.893 (expect 0.880)" FAIL seen in batch 17 = the loose part box around the live helix (accepted the same way for
   5406HHP / 5406SHP in batch 17); everything else 0 FAIL, 26 configurations 1 body, THD_* live without errors.
2. Ship as batch 20 (copy batch 19's ship / verify / paperwork scripts), QA #182.
