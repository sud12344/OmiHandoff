# Wave 3 bent tubes / 6701 - report (saved by the main session from the agent's hand-back, 2026-10-18)

68 rows: **0 ready, 37 blocked, 31 held.**
- **What Brennan's catalog gives:** only the two lengths and the end-piece hex.
- **No source for:**
  - tube OD;
  - bend radius;
  - end-piece hex length (HEXL);
  - bore (except on 4 Air-Way rows).

  So gen_bent cannot build any row yet.
- **Held 31:**
  - 1803 x13 and 1804 x15: code 62 heads -12 to -32 still need STEPs.
  - 1704-16-20 / -24-20 / -24-24-Tube: Air-Way and Brennan conflict - Air-Way M3 / N4 is 0.23-0.91 shorter under either reading; no length cells were written.

**Cells: 338 in `cells.csv`, all filling empty stage cells.**
- By kind: 227 brennan-dim, 36 endlib, 75 other.
- By column: CHEX 68, M1 65, L1 65, O 61, FlangeCode 61, NUTHEX 7, NOSETIP 7, D 4.
- New columns needed: M1 / L1 / HEXL / TUBEOD / RB / $PRP@FlangeCode, plus NUTHEX / NOSETIP for 6701.
- The skeleton tables 1803 / 1804 / 6701 also need O / CHEX / D.
- gen_bent reads tables 1704T / 1703T / 6701T: at ship time route the -Tube rows there, and keep the forged 1703 / 1704 SPEC from
  picking them up.

**Mapping** (evidence: `mapping_evidence.csv`, `pairs_45_90.csv`, `head_3300_vs_library.csv`)
- **90 deg:** L1 = JIC tip to the leg-2 axis (gen M1); L2 = JIC axis to the flange face (gen L1); A/F = end hex.
- **45 deg:** gen M1 = L1 - L2, gen L1 = L2 x sqrt2. Confirmed on 25 / 33 45 / 90 pairs within 0.05.
- **TUBE O.D. column** = the JIC end's tube size, not the bent tube's OD.
- **6701:** C2 equals the swivel library at all 6 sizes.
- **Air-Way s115:** 1704-12-12-Tube agrees fully once M3 is read as tip to the leg-2 axis. **So gen_bent's TEST rows used
  M1 = M3 - O/2, which is wrong by O/2.**
- **Head OD:** Air-Way s61 = Brennan 3300-61 at every size; 3300-61 also matches the measured code 61 head library (FLG61_MEAS).

**Generator test**
- With placeholder tube / HEXL / radius values only:
  - 27 configurations generate;
  - 47 when the code 62 heads come from Brennan's 3300-62 catalog table (what-if).
- vbacheck OK.

**Open points**
1. Tube OD, wall / bore, bend radius and HEXL per row: from OMi, Air-Way's own 3D models, or (Brennan = yes) the parts' own Brennan
   STEPs.
2. Code 62 heads -12 to -32: Brennan's catalog table 3300-62 prints head OD, thickness and groove OD - a catalog alternative to the 5 STEP
   downloads (user's yes needed; generator change).
3. Kept as printed and flagged:
   - 6701-20-20: M 2.750 < the -16's 3.10 (possible catalog M / L swap).
   - 1803-20-12 / 1804-20-12: A/F 1-1/2 / 2 against 1-11/16 on the other -20 rows (A13).
