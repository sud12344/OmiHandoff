# Wave 2 tee_elbow - report (saved by the main session from the agent's hand-back, 2026-10-18)

107 rows: **13 ready** (all became configurations in the test), **7 already complete** in the base (Brennan agrees with every value,
no cells: 2505-12-12-FG, 2606 x4, 2609-08-08-08-FG, 2611-08-08-08-FG), **6 blocked**, **81 held**.

- Ready: 1501-16-20-FG, 1501-20-16-FG, 2501-LL-04-02-FG, 2602-08-08-08-FG, 2611-12-12-12-FG, 5502-02-04 / -06-08 / -12-08 / -20-16-FG,
  5504-06-04 / -06-06 / -08-06 / -20-20-FG.
- Blocked: 1503 x5 (gen_tee stops: angled leg needs the angled-helix capability - also on the untouched base); 2505-16-16-FG ("port
  depth 1.14 >= leg 1.12", Q-ANGLED-P1 - needs its own STEP).
- Held 81: 19 3D-file rows (no STEP on disk); 62 by gates - approved capabilities not yet in the batch-16 tools / no SPEC (1503 1504 1601
  1602 1603 5501 5503 5505 6606 6815 6832 6835 6901 6902), Q-HX (2500 x4, 2502 x6), A9 tap drills, Q-NEW-ASME40 / Q-SIZE40-JIC
  (2501-40-40-FG), pilot / shape STEPs.

Test (`test/compare.txt`): 11 tee roots regenerated on base and base + cells; no pre-existing configuration changed (SW2 cell by cell);
macros differ only in the expected-count line and extreme-configuration arrays (2501 / 2611 / 5504). vbacheck 10/10, dofcheck_tee 25 legs
fully defined, allcfg 0 problems.

Conflicts (left empty): 2502-08-04-FG / -12-08-FG legs (Brennan = OMi 1.42 / 1.01, 1.89 / 1.35 vs MS51506 1.250 / 0.890, 1.660 / 1.230;
Q-CONFLICT-2502-MS51506); A9 rows; 1603-08-08-08-FG range drills (A14: measure STEP - present, not measured); 1504 / 1602 bores (OMi
drawings 0.01-0.02 below Brennan drill on 7 / 7 - Brennan proposed, flagged); 6901 / 6902 legs and body hex do not pair with Air-Way (not
proposed). OMi vs Brennan: 82 cells on 27 parts, all equal.

Open: Q-ANGLED-5503D can be settled by Brennan (drills 0.188 / 0.281 / 0.531 / 0.719 vs Air-Way's non-bore 0.83 / 1.19 / 1.54 / 1.64 on
5503-02 / -04 / -08 / -12-FG) - base cells not empty, overwrite is the user's call. New skeleton columns proposed for 6815 / 6832 / 6835
(no generator reads them yet). 2501-40-40-FG needs the 2-1/2 NPT end (ASME or its own STEP, present). 1501-24-24-FG nut (Air-Way 1.88 vs
Brennan 2.125) already in OPEN_QUESTIONS D.

Mappings with evidence: `mapping_evidence.txt` (TFA catalog page per family; agreement counts on rows with both values). Note: 1501 /
1503 swivel legs pair poorly with Air-Way's own -FG legs (Air-Way 0.02-0.13 shorter; base values kept).
