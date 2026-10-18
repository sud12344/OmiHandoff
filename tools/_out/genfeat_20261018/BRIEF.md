# Generator features 2026-10-18 - shared brief

Project: OMi fitting CAD library, `C:\Users\sudha\OneDrive\Desktop\OMi_Handoff`. Read `CLAUDE.md` first (the "Toolchain" section:
changing a generator touches every macro). Hard rules:
- never fabricate a dimension;
- every modelling assumption is logged in `$PRP@AxialSource`;
- never delete files (move them to `_to_delete\<dated reason>\`);
- NO SolidWorks, no macros run - SolidWorks is unavailable (license problem, and another session owns it);
- no websites;
- write .py / .txt / .csv / .json / .diff only - report files (.md) are refused for subagents; put the report in your final message.

User 2026-10-18: "build the missing generator features (hose barb, flange legs, angled legs, per-leg swivels, 5404-N names, -40 pipe
end, 6400 SPEC) so the ~100 data-complete rows can build". The six capabilities were approved on 2026-10-08 (PROJECT_STATUS s5); the
answers of today are in `00_DOCS/ANSWERS_2026-10-18.md` (A2 hexless ok, A6 rebuild 6400 by the generator, A13 / A15 / A16 / A17 / A18).

## Base and where you work
- **Base tools (read-only):** `tools/_out/puckfix_20261009/tools_new/` = the batch-16 toolchain (wave 1 + puck fix). Copy the WHOLE folder to
  `tools/_out/genfeat_20261018/<feature>/tools/` and edit only that copy.
- **Earlier partial work to reuse:**
  - designs `tools/_out/wave2_shapes_20261008/<ANGLED|FLG61LEG|HOSEB|PERLEGSW>/DESIGN.md` (+ evidence);
  - the stopped implementation `tools/_out/wave2_impl_20261009/` (`patch.diff`, `tools_new/`, `s4/`, `CHANGES.csv`; HOSEB ran there).
  Re-check before reusing; the wave-1 / puck changes came after it.
- **Data:** `tools/_out/brennan_yes_20261018/stage/04_DESIGN_TABLES` = the latest staged tables (read-only). The data-complete rows for
  your feature are NOT all in it yet: their cells are in `tools/_out/brennan_yes_20261018/wave2/<straight|tee_elbow|flange_hose>/cells.csv`
  (+ `rows.csv` notes "DATA COMPLETE" / gates) and `wave1/w1brennan_cells.csv` (1724 / 1800 / 1824 / 3474).
  - For testing: copy the stage 04_DESIGN_TABLES to `<feature>/test/root/04_DESIGN_TABLES`.
  - Apply the relevant cells there with `python -I tools/_out/brennan_yes_20261018/scripts/apply_brennan.py <feature>/test/root <cells.csv>`.
    It adds new columns, marks BRENNAN and asserts empty cells; it creates `04_DESIGN_TABLES` only if missing, so copy first.
  - Then set the target rows ASSUMED in your test copy.

## Definition of done
1. **The feature is in your tools copy.** Every target row your feature should build generates (gen_* summary), or blocks with a clear
   geometry reason.
2. **Static checks** (`<feature>/tools/checks/`) pass on every changed / new macro: vbacheck, dofcheck_*, `allcfg_check s|t <roots>`.
   - Where a measuring script exists for the end / body (`tools/measure`, the wave-1 extractors), run an OCP closed loop: model -> measure
     -> reproduces the table values.
3. **Regression:**
   - Regenerate ALL roots with the base tools and with yours, both on the SAME untouched stage copy, with GS_OUT / GT_OUT in separate
     folders under `<feature>/regen/`.
   - Diff ignoring line endings and the date line.
   - Only the roots your feature targets may change; SW2 tables of every other root identical.
   - Write `regen/cmp.txt`.
4. **Deliverables:**
   - `<feature>/patch.diff`: unified diff of your tools copy vs the base tools, generators / templates / checks / measure only.
   - `<feature>/rows_result.csv`: table,config,result(built|blocked|skipped),reason.
   - `<feature>/notes.txt`: assumptions added (each with source), anything the user must decide.
5. **Reply** with: rows built / blocked per root, files changed, regression result, open decisions. Keep it short.

Other agents work in parallel on other features, each in its own `genfeat_20261018/<feature>/` copy. Never touch another feature's folder,
the base tools, the stage, or the live `tools/` / `04_DESIGN_TABLES`. Keep your changes local to your feature's SPECs / functions where
you can, so the patches merge.
