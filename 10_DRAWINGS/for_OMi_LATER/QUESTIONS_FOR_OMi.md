# Questions for OMi - collected to send later (2026-10-18)

User 2026-10-18: "for questions for OMI place them somewhere else to be sent later". Nothing here has been sent.
Collected from `00_DOCS/OPEN_QUESTIONS_2026-10-18.md` group B, updated with the answers of 2026-10-18 (`00_DOCS/ANSWERS_2026-10-18.md`).
The older draft `10_DRAWINGS/for_OMi_2026-10-14/` (size request: bent tubes, 4005, flareless) is also unsent - merge the two before sending.

Since 2026-10-18 Brennan's catalogs and 3D files are an allowed size source, so ask OMi only what Brennan does not cover (marked below).

## 1. Sizes and facts only OMi has
1. **4005 flange O-rings** (9 parts): code 61 or code 62? AS568 size, or I.D. + cross-section; material and hardness.
2. **Flareless nut and sleeve 0618 / 0619** (3 parts): sizes and shape. Is OMi's 0618 / 0619 the same part as Brennan's V0318 / V0319?
3. **Compression fittings (230) and test-gauge parts (12)**: dimensions or supplier drawings. Neither Air-Way nor Brennan prints them.
4. **6 dropped tube fittings and 6 ORFS parts with no source anywhere** - list: `tools/_out/adapters77_20261016/possible_2535.json`
   ("no source" entries) and `tools/_out/brennan_yes_20261018/brennan_rows.csv` (to re-list before sending).
5. **FS2408 ORFS plug**: solid, or with a blind hole (Air-Way shows one)? Built solid meanwhile.
6. **FS0319-24 braze sleeve collar**: Air-Way 1.71, Brennan 1.910, Air-Way's own FF2407-24 2.00 - which?
7. **6420-12-12**: website length 1.730 does not fit the standard ports - which body?
8. **13 parts that are only in OMi's parts file, not on the website** (e.g. 4000-05, 6701-10-10, 0618-06): are they sold? (Our rule:
   the website list decides - user 2026-10-18 A24 - so they are left out unless OMi says they sell them.)
9. **Bent-tube elbows (1703 / 1704 / 1803 / 1804 -Tube, 6701)**: Brennan's catalog now covers the 68 parts. Optional: ask OMi to
   confirm tube OD / wall / bend radius as a cross-check.
10. **The rest of the 226 "sizes we need"** (OMi sent 14 drawings): re-count first - ask only for what Brennan cannot cover now.
11. **One drawing per series, or one per part number?** (for the drawings OMi wants)

## 2. Questions from the 2026-10-09 email with no answer yet (chase)
1. Does any number on the 62 check drawings look wrong?
2. What goes in the drawing title block (logo, material, finish, tolerances, drawn by)?
3. Small 6408 plugs (-02, -03, -05, -04-O-SLD): hollow or solid? (built solid meanwhile)
4. (Answered by the user on 2026-10-18, A10: -LN parts are modelled without the locknut - just inform OMi.)

## 3. Replies OMi asked for (their notes on the typo sheet)
- "NPFT - why is this an issue?" -> NPFT is not a thread name; customers and search filters looking for NPTF miss those 234 parts.
- Pipe swivel ends written NPTF (229 rows) - "not sure what this means" -> your own drawings call the swivel thread NPSM (e.g.
  "3/8-18 NPSM"), so the website's "NPTF" on the swivel side is the typo.

## 4. Findings to report (for OMi's website / file)
- Inside holes wider than the threaded port they drill into (6404 / 6410 reducers; e.g. 6410-20-06-O 0.509 vs port drill 0.50,
  -20-08-O 0.689 vs 0.68, -32-12-O 0.981 vs 0.97, -32-16-O 1.231 vs 1.22). We cap them at the port drill (user 2026-10-18, A11).
- 6801-04-02: Air-Way leg 1.03, Brennan 0.92. 6801-12-12: Air-Way thread length 0.469, Brennan 0.410.
- 4601-16-12-NWO-FG: Air-Way's -FG row differs strongly from Brennan and from Air-Way's own plain row.
- 1704 rows 260-272 of OMi's parts file say "45° Elbow" (they are 90 deg).
- 2408-14-SOLID: Air-Way hex 1.125 is smaller than its own thread (1-3/16); Brennan / MS51518D give 1.250.
- 1404 overall lengths that do not fit the swivel nut (we kept Air-Way's length there):
  - Parts: 1404-02-02 (OMi 1.08), 1404-04-04 (1.42), 1404-16-12 (2.29), 1404-20-24 (2.47), 1404-24-20 (2.54).
  - With these lengths the swivel nut face sits too close to (or too far from) the swivel stem tip.
  - Also: the website's 1404-20-24 and 1404-24-20 rows look swapped - the SAE cross-reference column says "24-20" on the 1404-20-24 row
    and "20-24" on the 1404-24-20 row.
  - Please check these lengths.
