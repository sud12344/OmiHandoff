"""2026-10-08: the bridge for the open-questions doc - fittings freed by each group of answers, in this fixed order.
Reads rows.csv (unblock.py). The 3 unbuilt 5405 rows count as built (project convention: macro ready, re-run Build_5405);
6502-16-12-FG / 6506-12-14 / 6565-32-32 carry tier-1 questions (Q-B-SWELB, the -14 length, Q-THREAD) that the impact
files do not list - they are counted under the smaller questions."""
import csv, collections, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'rows.csv'), encoding='utf-8')))
rows = [r for r in rows if r['config'] not in ('5405-12-08', '5405-16-08', '5405-16-12')]
TIER1 = {'6502-16-12-FG': 'Q-B-SWELB', '6506-12-14': 'Q-TRANSFER-SWOFFSET', '6565-32-32': 'Q-THREAD'}


def fam(a):
    if a.startswith('STEP:') or a in ('STEP', 'OWN-STEP'):
        return 'STEP'
    if a.startswith('CAP:'):
        return 'CAP'
    if a.startswith('OMI:'):
        return 'OMI'
    if a.startswith(('BLOCKED', 'DECIDE:')) or a == '?':
        return 'BLOCKED'
    return a


AG = []
for r in rows:
    gs = [frozenset(fam(a) for a in g.split('|')) for g in r['user_gates'].split(' ; ') if g]
    if r['config'] in TIER1:
        gs.append(frozenset([TIER1[r['config']]]))
    AG.append(gs)
SCOPE = {'Q-SCOPE-TUBE', 'Q-SCOPE-ORING', 'Q-NEW-ORINGSRC', 'Q-NEW-4005CODE'}
ORDER = [
    ('Paused new masters, no decision needed', set()),
    ('OK to use Brennan data on its own?', {'Q-BRENNAN-ONLY'}),
    ('Download ~80 Brennan 3D files', {'STEP'}),
    ('Reuse already-measured end details?', {'Q-TRANSFER-ENDLIB'}),
    ('Approve 6 new shapes for the drawing program', {'CAP'}),
    ('Scope: bent-tube elbows and O-rings', SCOPE),
    ('Parts with no wrench hex from Brennan files?', {'Q-SOP5'}),
    ("Use Air-Way's tap-drill sizes?", {'Q-TRANSFER-TAPDRILL'}),
    ('Answers from OMi', {'OMI'}),
]
done = set()
out, prev = [], 0
for name, g in ORDER:
    done |= g
    n = sum(1 for gs in AG if all(a & done for a in gs))
    out.append(dict(step=name, freed=n - prev))
    prev = n
everything = set().union(*[a for gs in AG for a in gs]) - {'BLOCKED'}
n = sum(1 for gs in AG if all(a & everything for a in gs))
out.append(dict(step='About 40 smaller data questions', freed=n - prev))
prev = n
out.append(dict(step='Blocked by geometry or a part-specific conflict', freed=len(AG) - prev))
print(json.dumps(out, indent=1), 'waiting total', len(AG))
json.dump(dict(built=1044, planned=1804, steps=out), open(os.path.join(HERE, 'bridge.json'), 'w'), indent=1)
