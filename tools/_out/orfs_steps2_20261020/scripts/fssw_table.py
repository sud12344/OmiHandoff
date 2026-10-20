"""fssw_table.py (2026-10-20): the per-size female face-seal swivel table (gen_tee FSSW_MEAS) from the measure_fssw readings in ends_survey.json,
mapped exactly as the -08 entry was (tools/_out/orfs_wp2_20261020 build_endlib.py / end_lib_08.json): the -08 row must come out equal to the
generator's FSSW_MEAS[8]. -> fssw_table.json / .txt. Read-only."""
import os, json, math
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(HERE, 'ends_survey.json')))
R4 = lambda x: round(x, 4)
out = {}; lines = []
for name, o in S.items():
    if not name.startswith('FSSW FS6500-') or 'ERROR' in o: 
        if name.startswith('FSSW') and 'ERROR' in o: lines.append(f'{name}: ERROR {o["ERROR"]}')
        continue
    d = int(name.split('-')[1])
    no = o['NUT_OUTSIDE']
    k = [j for j, e in enumerate(no) if e[0] == 'L' and e[1] == 0.0 and abs(e[3] - o['NUT_CORNER_R']) < 1e-3][0]     # the hex corners
    ch = no[k + 1]; sk = no[k + 2]                                                                                         # rear 60deg chamfer, skirt cone
    rel = o['CAV_REL']
    m = dict(AF=round(o['NUT_CORNER_R'] * math.sqrt(3), 3), HEXL=ch[4], SKF=ch[5], SKS=sk[4], SKR=sk[5], NUTL=o['NUTL'], NECKR=o['NECKR'],
             SEAL=o['SEAL_TO_NUTFACE'], BODYS=R4(o['NUTFACE_a'] - o['BODYFACE_a']), TE=o['TE'], RELS=rel[0][3], RELR=rel[0][4], LIPS=rel[0][1], STEMR=o['STEMR'])
    if o['MOUTH'] == 'cb': m.update(CBR=o['CBR'], CBD=o['CBD'], CB_ANG=o['CB_ANG'])
    else: m.update(CSR=o['MOUTH_R'], CS_ANG=o['MOUTH_ANG'])
    m['_notes'] = dict(rear_chamfer_ang=ch[1], skirt_ang=sk[1], mouth=o['MOUTH'], lip=o.get('LIPR'), neck_taper=o.get('NECK_TAPER'), relief_ang=rel[1][0], cone_ang=rel[0][0])
    out[d] = m
    lines.append(f'-{d:02d}: ' + json.dumps(m))
json.dump(out, open(os.path.join(HERE, 'fssw_table.json'), 'w'), indent=1)
open(os.path.join(HERE, 'fssw_table.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
