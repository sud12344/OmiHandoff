## RESULT: No public text-readable reproduction of the SAE J1926-2 stud-end table itself was found. The closest fetchable source is Parker ORD-5700 Design Table 4-4 (AS4395 fitting end, "used with J1926/1 and AS5202 bosses"), whose groove-diameter and groove-width columns match ALL your anchors. Stud/thread length is not in that table; Parker Catalog 4300 p. G7 gives Parker's own stud-length columns. Everything below is exactly as extracted; nothing is estimated.

### (1) Sources fetched
A. Parker O-Ring Handbook ORD 5700, Section 4 excerpt "Tube Fitting Boss Seals", Design Table 4-4 "Fitting end AS4395 used with J1926/1 and AS5202 bosses (only the dimensions that define the O-ring cavity are shown.)"
   - https://www.parker.com/content/dam/Parker-com/Literature/O-Ring-Division-Literature/ORD-5700_BossSeals.pdf (fetched 3x, incl. 2 raw-text passes)
   - Mirror (independent pass, identical raw text): https://www.bayseal.com/wp-content/uploads/2021/05/Tube-Fitting-pages-4-22-through-4-24-Parker-Handbook.pdf
B. Parker Catalog 4300, page G7 "Port Ends for SAE J1926-1 (ISO 11926-1) Port" (Pipe Fittings and Port Adapters section):
   - https://www.goodyearrubberproducts.com/files/Parker/ParkerTubeCatalog4300/Parker%20Tube%20Catalog%204300examin1.Page192.pdf (fetched 2x; both passes numerically identical)

### (2a) Parker ORD-5700 Table 4-4 — RAW extracted text (both passes identical)
Header tokens in order: `Parker O-ring Size No. | Tubing OD | Thread T | E Dimension Across Hex Flats | F +.002 -.003 | H Max. | K Dia. ±.010 | G +.015 -.000`
Row raw text (verbatim token order):
```
3-902 1/8 5/16-24 UNF-3A .563 +.003 -.004 .250 .005 .549 .063
3-903 3/16 3/8-24 .625 .312 .611 .063
3-904 1/4 7/16-20 .688 .364 .674 .075
3-905 5/16 1/2-20 .750 .426 .736 .075
3-906 3/8 9/16-18 .813 .481 .799 .083
3-908 1/2 3/4-16 1.000 .660 .986 .094
3-910 5/8 7/8-14 1.125 .773 1.111 .107
3-912 3/4 1 1/16-12 UNJ-3A 1.375 .945 .008 1.361 .125
3-914* 7/8 1 3/16-12 1.500 ±.016 1.070 1.475
3-916 1 1 5/16-12 1.625 1.195 1.599
3-920 1 1/4 1 5/8-12 1.875 1.507 1.879
3-924 1 1/2 1 7/8-12 2.125 ±.020 1.756 2.095
3-932 2 2 1/2-12 2.750 2.381 2.718
*No fitting end for the 3-914 O-ring size is included in AS4395, but the dimensions shown here follow the same pattern.
```
Parsed table (my column assignment: E = hex flats, F = groove root dia, H Max = shoulder dia max, G = groove width; the header lists a 5th column "K Dia. ±.010" but only 4 numeric values per row are extractable, so K is MISSING for every row and the stray tokens ".005" (in 3-902 row) and ".008" (in 3-912 row) plus "+.003 -.004", "±.016", "±.020" appear to be merged/spanning tolerance cells — I could not verify their column visually; no browser/PDF download was possible):

dash | thread (as printed) | groove width G (+.015/-.000) | groove root dia F (+.002/-.003) | stud/thread length | E hex flats | H Max | K Dia ±.010
-2 | 5/16-24 UNF-3A | .063 | .250 | not tabulated | .563 | .549 | MISSING
-3 | 3/8-24 | .063 | .312 | not tabulated | .625 | .611 | MISSING
-4 | 7/16-20 | .075 | .364 | not tabulated | .688 | .674 | MISSING
-5 | 1/2-20 | .075 | .426 | not tabulated | .750 | .736 | MISSING
-6 | 9/16-18 | .083 | .481 | not tabulated | .813 | .799 | MISSING
-7 | (row absent in source) | — | — | — | — | — | —
-8 | 3/4-16 | .094 | .660 | not tabulated | 1.000 | .986 | MISSING
-10 | 7/8-14 | .107 | .773 | not tabulated | 1.125 | 1.111 | MISSING
-12 | 1 1/16-12 UNJ-3A | .125 | .945 | not tabulated | 1.375 | 1.361 | MISSING
-14* | 1 3/16-12 | not printed on row (see note) | 1.070 | not tabulated | 1.500 (±.016) | 1.475 | MISSING
-16 | 1 5/16-12 | not printed on row | 1.195 | not tabulated | 1.625 | 1.599 | MISSING
-20 | 1 5/8-12 | not printed on row | 1.507 | not tabulated | 1.875 | 1.879 | MISSING
-24 | 1 7/8-12 | not printed on row | 1.756 | not tabulated | 2.125 (±.020) | 2.095 | MISSING
-32 | 2 1/2-12 | not printed on row | 2.381 | not tabulated | 2.750 | 2.718 | MISSING
Note on G for -14..-32: the text layer prints ".125" only once, on the 3-912 row, and nothing for 914–932 — consistent with a merged cell spanning -12 through -32, but NOT individually printed, so I report those rows as not printed rather than .125.
Caveat: this is the AS4395 (military) fitting end, not the SAE J1926-2 table; Parker labels it as the fitting end used with J1926/1 ports. -14 is flagged by Parker as not in AS4395 ("follow the same pattern").

### (2b) Parker Catalog 4300 p. G7 — stud length data (Parker product dimensions, not the J1926-2 table)
Raw header tokens: `Thread | Locknut Hex | Drill | Minimum Thread | Stud Length` and symbol row `SIZE | T | C4 | D Max | L4 Min | X | Z Max` with units `UN/UNF (inch) (inch) (inch) (inch) (inch)`. Five names vs six symbols — the name-to-symbol mapping is ambiguous from text; values are given in printed column order.
LIGHT DUTY (TRIPLE-LOK, FERULOK, ADAPTERS): SIZE | T | C4 | D Max | L4 Min | X | Z Max
2 | 5/16-24 | 7/16 | 0.063 | 0.390 | 0.297 | 0.36
3 | 3/8-24 | 1/2 | 0.125 | 0.390 | 0.297 | 0.33
4 | 7/16-20 | 9/16 | 0.172 | 0.454 | 0.360 | 0.39
5 | 1/2-20 | 5/8 | 0.234 | 0.454 | 0.360 | 0.43
6 | 9/16-18 | 11/16 | 0.297 | 0.500 | 0.391 | 0.43
8 | 3/4-16 | 7/8 | 0.391 | 0.562 | 0.438 | 0.49
10 | 7/8-14 | 1 | 0.484 | 0.656 | 0.500 | 0.56
12 | 1 1/16-12 | 1 1/4 | 0.609 | 0.750 | 0.594 | 0.65
14 | 1 3/16-12 | 1 3/8 | 0.719 | 0.750 | 0.594 | 0.65
16 | 1 5/16-12 | 1 1/2 | 0.844 | 0.750 | 0.594 | 0.65
20 | 1 5/8-12 | 1 7/8 | 1.078 | 0.750 | 0.594 | 0.65
24 | 1 7/8-12 | 2 1/8 | 1.312 | 0.750 | 0.594 | 0.65
32 | 2 1/2-12 | 2 3/4 | 1.781 | 0.750 | 0.594 | 0.59
HEAVY DUTY (SEAL-LOK):
2 | 5/16-24 | 1/2 | 0.063 | 0.390 | 0.374 | 0.38
3 | 3/8-24 | 9/16 | 0.125 | 0.390 | 0.374 | 0.39
4 | 7/16-20 | 5/8 | 0.172 | 0.454 | 0.433 | 0.43
5 | 1/2-20 | 11/16 | 0.236 | 0.454 | 0.433 | 0.44
6 | 9/16-18 | 3/4 | 0.264 | 0.500 | 0.472 | 0.47
8 | 3/4-16 | 15/16 | 0.378 | 0.562 | 0.551 | 0.54
10 | 7/8-14 | 1 1/16 | 0.484 | 0.656 | 0.630 | 0.63
12 | 1 1/16-12 | 1 3/8 | 0.609 | 0.750 | 0.728 | 0.73
14 | 1 3/16-12 | 1 1/2 | 0.709 | 0.750 | 0.728 | 0.73
16 | 1 5/16-12 | 1 5/8 | 0.811 | 0.750 | 0.728 | 0.73
20 | 1 5/8-12 | 1 7/8 | 1.024 | 0.750 | 0.728 | 0.73
24 | 1 7/8-12 | 2 1/8 | 1.260 | 0.750 | 0.728 | 0.73
32 | 2 1/2-12 | 2 3/4 | 1.575 | 0.750 | 0.728 | 0.73
Footnotes: "1) See page O3 for SAE O-rings. 2) See page U26 for port details." No groove dimensions on this page.

### (3) Anchor check (against ORD-5700 Table 4-4)
- -4 groove width 0.075: MATCH (G = .075)
- -12 groove width 0.125: MATCH (G = .125)
- -16/-20/-24 groove width 0.125: NOT INDIVIDUALLY PRINTED in the text layer (only .125 on the -12 row; appears to be a spanning cell) — consistent, not independently confirmed; no conflict found.
- -4 groove root dia 0.364: MATCH (F = .364)
- -8 groove root dia 0.660: MATCH (F = .660)
- -12 groove root dia 0.945: MATCH (F = .945)
- -16 groove root dia 1.195: MATCH (F = 1.195)
- -24 groove root dia 1.756: MATCH (F = 1.756)
No conflicts with any anchor.

### (4) Missing / unreadable / absent
- No J1926-2 (or ISO 11926-2) stud-end table with groove + thread length was found in any fetchable text source. Candidate copies exist but were unreachable: fitsch.cn "SAE J1926-2 3 -2010_opt.pdf" (robots.txt disallowed; curl blocked by egress proxy), img.antpedia.com "SAE J1926-2-2023.pdf" (HTTP 403), Air-Way "ORings-for-SAE-J1926-2-3-Stud-Ends-Table.png" and its PDF (image-only; host blocked for curl), iTeh ISO 11926-2 samples (tables not in sample), Scribd (JS-only). No browser extension was connected, and the sandbox egress proxy denied every host except github, so no PDF/image could be viewed directly.
- Checked and confirmed to contain NO stud-end groove table: Parker 4300 pp. U26 (port), U27, U28, T-section p.412, Appendix p.490, Aberdeen "Parker-SAE-Straight-Thread-O-Ring-Port.pdf"; Tompkins SAE ORB port PDF; Midland H_SAE.pdf; Hyvair saeoringport.pdf; ARG SAE O-Ring Boss PDF (garbled text); Seal & Cylinder chart; Hydraulic Megastore guide; Hydraulic Store guide; GageRef; Hydraulic Insight; Delphi; Sannke; Hydraxio; jiayuanfitting(s) pages/PDF; Global O-Ring; Wikipedia; fittingsandadapters.com; Stauff/HydraSpecma PDFs; industrialmonitordirect (its "port" table appears non-standard; disregard).
- In Table 4-4: "K Dia. ±.010" column has no extractable values (MISSING all rows); G not printed on rows -14 through -32; dash -7 absent; thread/stud length not tabulated; the meaning of stray tokens ".005"/".008" is unresolved.
- Parker 4300 G7: header name-to-symbol mapping (which of L4 Min / X / Z Max is "Minimum Thread" vs "Stud Length") could not be resolved from the text layer.

Recommendation: treat ORD-5700 Table 4-4 F/G columns as the groove root dia / groove width source (anchors all match), and obtain a visual of the actual J1926-2 Table 1 (or the ORD-5700 page) to resolve the K column, the -14..-32 groove-width cells, and thread length.