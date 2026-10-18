# A9 - tap drill of the -24 / -32 female pipe port (user 2026-10-18: "wait for a brennan step")

Extractor: `tools/_out/puckfix_20261009/tools_new/measure/fgelbow.py --port <axis,sign> <file>` (batch-16 tools). Output: `measure_out.txt`.

- Validation: BRENNAN_5405-08-08 leg (0,1) -> drill dia **0.718**, taper depth 0.75, drill depth 0.90, 120 deg point = the values recorded
  2026-09-23. The extractor still reproduces them.
- BRENNAN_5406-40-32 (the only file on disk with a -32 female pipe port), leg (0,1): NPTF taper 0.97 deep (2.3148 -> 2.2582), then a
  90 deg shoulder straight into the bushing's through-bore **2.172**. There is no separate tap-drill section, and 2.172 is neither Air-Way
  value (2.19 / 2.20). **It does not settle A9.**
- No file on disk has a -24 female pipe port.

**Needed (user download):** `BRENNAN_5405-24-24.stp` and `BRENNAN_5405-32-32.stp`. They are the same family as the validation part, and
both are OMi parts (5405 table rows 28 / 30: Air-Way prints 1.72 and 2.20). Until they arrive, A9 stays open, and the rows that need a
-24 / -32 tap drill stay held.
