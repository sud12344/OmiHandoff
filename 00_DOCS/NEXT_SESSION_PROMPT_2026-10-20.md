# Next session (written 2026-10-20, end of the cloud session) - what was staged, what waits on the PC, what waits on the user

Nothing has shipped since batch 16 (2026-10-19). Everything below is STAGED in the cloud (Python side only, no SolidWorks). It is on the branch
`claude/pensive-planck-t9i90d`, rebased on batch 16 (d63e1a6).

## Count (`tools/_out/count_20261020/count_ready.py`)
| | parts of 2,535 |
|---|---|
| shipped now (in a master) | 1,106 |
| generated, waiting for the SolidWorks dry runs + ship | 431 |
| of which ORFS (FS...) | 121 (+ 8 FS4000 O-rings in the 4000 master) |
| = ready after SolidWorks | **1,537** |
| not yet (data, STEP, decision or OMi needed) | 998 |

## What the 2026-10-20 session staged (details: `00_DOCS/PROJECT_STATUS.md` section 1, the 2026-10-20 entries)
1. A14: the 1603-08-08-08-FG bores (`tools/_out/a14_1603bore_20261020/`), in the batch-17 stage.
2. Batch-17 work rebased on batch 16; the 24 batch-16 roots regenerated from the new state (`tools/_out/rebase_b16_20261020/`).
3. ORFS pilots: 8 of 9 Brennan STEPs in `09_STEP_FILES/BRENNAN_FS*.stp` (FS2406-08-06 has no CAD at Brennan).
   - Extractors validated on them: `tools/_out/orfs_wp2_20261020/`.
4. ORFS generator (`tools/_out/orfs_gen_20261020/README.md`, steps 1-5). It is a staging copy of the merged batch-17 toolset plus the ORFS
   end functions. Outputs:
   - `out/`: FS2403, FS6400, FS0306, FS0318, FS0319, FS0319C, the straight swivels FS6565 / FS6540 / FS6504 / FS6505 (+ ...C);
   - `out/tee/`: 31 forged FS masters (the base masters plus the leg-shape variants `<root>N / R / C / NR / NC`, one sketch each);
   - `out/ring/`: the O-ring master 4000 with FS4000.
5. 29 more Brennan STEPs from the user (per-size nuts / sleeves, FS6500-04 ... -20, FS2403-24-24, FS6400-32-32-O, FS2501-08-08-FG,
   FS6565-08-08): filed, measured (`tools/_out/orfs_steps2_20261020/`), in the generator (README step 5).

   Every root has passed vbacheck, dofcheck and allcfg. The regression shows 99 / 99 existing roots identical. The OCP closed loops against
   the rows and the Brennan pilots found 0 off.

## On the PC (SolidWorks; the user signs in to 3DEXPERIENCE first - never start SLDWORKS.exe yourself)
1. **Batch 17** as planned in `00_DOCS/NEXT_SESSION_PROMPT_2026-10-19.md`. adapters77 goes first, with the user's OK.
2. **ORFS dry runs**, using the CLAUDE.md verify loop. `TABLE_PATH` points at `tools/_out/orfs_gen_20261020/out` (or at `out/tee` / `out/ring`).
   SAVE / REPORT go to a scratch folder. Run them in this order:
   - FS2403, then FS6400: the first face-seal ends (the Thread feature, the bore-cut face pick on the land);
   - one forged root of each leg shape: FS2500 (stepped), FS2500N (no step), FS6500C (counterbored swivel), FS6801R (stud neck below the
     flats); then the rest of `out/tee/` (PLAN risk R1: the thread run-out at the flats);
   - FS0306, FS0318, FS0319, FS0319C and 4000 (the 4000 master has 29 configurations; its 21 old rows dry-ran clean on 2026-10-14).
3. Nothing ORFS ships before those dry runs and the user's review. Shipping also needs the staged FS review tables moved into
   `04_DESIGN_TABLES`, and the staging generator changes merged into the live `tools/`. Merging means: back up the live tools, regenerate
   all roots with the old and the new tools, then diff.

## Downloads that would add parts (Brennan PARTcommunity, saved as `09_STEP_FILES/BRENNAN_<pn>.stp`)
Received 2026-10-20 and in the generator: the per-size nuts / sleeves, FS6500-04 ... -20-FG, FS2403-24-24, FS6400-32-32-O, FS2501-08-08-FG,
FS6565-08-08. Still missing:
- **Bulkhead legs:** FS2701-04-04-FG, FS2701-06-06-FG, FS2701-10-10-FG, FS2701-12-12-FG, FS2701-16-16-FG.
- **Adjustable studs:** FS6801-04-04-NWO-FG, -06-06, -10-10, -12-12, -16-16, -20-20, -24-24 (all -NWO-FG).
- **Straight male ends** (a forged leg has no thread relief): FS2403-04-04, -06-06, -10-10, -12-12, -16-16, -20-20.
- **-24 forged leg / swivel:** FS6500-24-24-FG.
- **FS2406-08-04:** the stand-in for the missing FS2406-08-06 pilot.

## Decisions waiting on the user
- **Sleeve length:** FS0319 holds the collar length and the stop lip from the seal face, so Air-Way L 0.37 (STEP 0.374) shortens the spigot
  (-04 / -06 / -08). OK? (Sleeve sizes: settled - the user sent every FS0319 STEP.)
- **Tell the user:** Brennan's FS0306 / FS0318 -10 and -24 thread bores (dia 0.892 / 1.817) are smaller than the ASME basic minor of 1-14 /
  2-12 (0.9227 / 1.9098); the model keeps the basic minor (each row's `$COMMENT` says BRENNAN DIFFERS).
- **Straight swivel body hex:** where Air-Way prints the hex length (FS6540 L37, FS6504 L39) the body hex is built to it; it is 0.015 ... 0.09
  shorter than the Brennan swivel (hex face -> seal face, e.g. -12: Air-Way 1.03 / Brennan 1.12). Keep Air-Way, or use Brennan's?
- **New masters per leg shape** (`<root>N / R / C`): SolidWorks needs one sketch per master, so e.g. FS6500 is now four masters. OK, or should a
  different split be used?
- **Still open from before:**
  - FS0319-24 (Air-Way / Brennan OD conflict, plan D5);
  - FS6400-L / FS6801-L (no shape source for the long variants);
  - Q-FS-ORBSTUD;
  - the VERIFIED-or-ASSUMED question for the OMi answers.

  The questions of `NEXT_SESSION_PROMPT_2026-10-19.md` are still open as well.

## Found in passing (not fixed: batch-17 tools)
- SPEC 6400 End A ORB thread label uses the wrong dash on unequal-dash rows. This affects text only.
