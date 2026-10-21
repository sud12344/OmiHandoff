# Batch 20 (2026-10-21): data block for update_masterdata_20.py (QA_Log row #182, Topologies note 5404N).
QA = [
    ('182',
     'Batch 20 shipped - RUN_ME_batch20.txt: 5404N -06 thread fix (QA #178 closed) + the 4 long nipples 5404-N-06X4.500 / -06X5.500 / -08X2.500 / -08X5.500 (A4); user 2026-10-21 "run the 5404N dry run and ship batch 20 if it passes"',
     'Cause found by a SolidWorks probe on the batch-17 dry-run part with its design table removed (the 2026-10-20 probe was invalid: the table reset every value): with the bar only 0.004 above the -06 crest cone, a helix ending exactly at the thread length (0.4078) puts the end of the swept tooth on the shoulder edge - THD_End* error 1; 0.36 ... 0.4058 and 0.415 build. Fix: gen_straight2 ROUND_STEP_HELIX = 0.005 - the helix stops 0.005 short on a round-bar-step end (the 7 -06 rows: HEIGHT@HELIX 0.4078 -> 0.4028, logged in AxialSource). Every root regenerated: only 5404N changes (tools/_out/batch20_20261021/regen_cmp.txt); dofcheck / allcfg / vbacheck clean. SolidWorks dry run: 26 configurations rebuilt with the threads live, 0 feature failures, 1 body each, the 4 shipped configurations identical (dV 0); the reference body-diameter FAIL is the loose part box around the live helix (exact size 0.88 = table), accepted as for 5406HHP / 5406SHP. Post-ship verify 0 BAD (checks/verify_b20.txt).',
     '5404N master replaced (4 -> 26 configurations), macro + report + SW2 + review table (4 rows MISSING -> ASSUMED by the A4 transfer, 29 cells) + tools/generators/gen_straight2.py deployed. Old files -> _to_delete/superseded_20261021b/batch20_replaced + tools/_out/batch20_20261021/old_files.',
     'INFO',
     'Done.'),
]
NOTES = {'5404N': '2026-10-21 BATCH 20 SHIPPED (QA #182): -06 thread fix (helix 0.005 short of the round-bar shoulder) + 4 long nipples -> 26 configurations'}
STATUS = {}
