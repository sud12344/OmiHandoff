"""build_entries.py (2026-10-21): FSM_MEAS / FSBH_MEAS / NWO_FS entries for every size from ../survey.json (survey.py), derived exactly as the
-08 entries were (tools/_out/orfs_wp2_20261020/build_endlib.py): FSM = measure_fsm (GI GO GD FR, THDS = THD_END, RELR, ENDL); FSBH =
the bulkhead leg's first step radius (STEPR), RELL, and the collar cylinder length (COLLARL); NWO_FS = the stud profile after the undercut:
washer face radius WR / thickness WT, lock nut thickness NUTT and A/F AF_B (hex corner radius x 2 cos 30), neck radius NECKR / length NECKL,
undercut length UL (= measure_stud UCL). The -08 values must reproduce the generator's current entries. -> ../entries.json"""
import os, json, math
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(H, 'survey.json')))
R4 = lambda x: round(x, 4)
FSM, FSBH, NWO = {}, {}, {}
for d in (4, 6, 8, 10, 12, 16, 20):
    a, b = m[f'FSM FS2403-{d:02d}-{d:02d} +X'], m[f'FSM FS2403-{d:02d}-{d:02d} -X']
    keys = ('GI', 'GO', 'GD', 'FR', 'THD_END', 'RELR', 'ENDL')
    assert all(abs(a[k] - b[k]) < 0.0011 for k in keys), (d, [(k, a[k], b[k]) for k in keys])        # both ends of the straight agree
    FSM[d] = dict(GI=a['GI'], GO=a['GO'], GD=a['GD'], FR=a['FR'], THDS=a['THD_END'], RELR=a['RELR'], ENDL=a['ENDL'])
for d in (4, 6, 8, 10, 12, 16):
    bh = m[f'FSBH FS2701-{d:02d}-{d:02d}-FG']
    cyl = [s for s in bh['BH_STEPS'] if s[0] == 'cyl']
    step, coll = cyl[0], cyl[1]                                   # the i4 step, then the collar (= row d17 / 2)
    assert abs(step[1] - bh['SHOULDER_R']) < 0.0011
    FSBH[d] = dict(STEPR=step[1], RELL=bh['RELL'], COLLARL=R4(coll[3] - coll[2]))
for d in (4, 6, 8, 10, 12, 16, 20, 24):
    st = m[f'STUD FS6801-{d:02d}-{d:02d}-NWO-FG']
    A = [x[1:] for x in st['AFTER']]                               # (ang, a1, r1, a2, r2) after the undercut shoulder
    wface, wcyl, wstep, ch1, hexc, ch2, back, neck = A[:8]
    assert wface[0] == 90 and wcyl[0] == 0 and ch1[0] == 75 and hexc[0] == 0 and ch2[0] == 75 and neck[0] == 0, (d, A[:8])
    NWO[d] = dict(NECKR=neck[2], NECKL=R4(neck[3] - neck[1]), NUTT=R4(back[1] - wcyl[3]), WR=wcyl[2], WT=R4(wcyl[3] - wcyl[1]),
                  UL=st['UCL'], AF_B=R4(2 * hexc[2] * math.cos(math.radians(30))))
OLD = dict(FSM=dict(GI=0.2125, GO=0.3145, GD=0.052, FR=0.3595, THDS=0.383, RELR=0.3595, ENDL=0.504),
           FSBH=dict(STEPR=0.4005, RELL=0.094, COLLARL=0.20),
           NWO=dict(NECKR=0.375, NECKL=0.039, NUTT=0.41, WR=0.505, WT=0.041, UL=0.146, AF_B=0.938))
for name, new in (('FSM', FSM), ('FSBH', FSBH), ('NWO', NWO)):
    bad = {k: (v, new[8][k]) for k, v in OLD[name].items() if abs(v - new[8][k]) > 0.0011}
    print(name, '-08 reproduces the generator entry:', not bad, bad or '')
json.dump(dict(FSM_MEAS=FSM, FSBH_MEAS=FSBH, NWO_FS=NWO), open(os.path.join(H, 'entries.json'), 'w'), indent=1)
for name, t in (('FSM_MEAS', FSM), ('FSBH_MEAS', FSBH), ('NWO_FS', NWO)):
    for d, v in t.items():
        print(f'{name}[{d}] = {v}')
