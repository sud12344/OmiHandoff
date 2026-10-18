"""finalize_rows.py: add the 37 edits_77 rows to rows.csv and the test outcome (test/rows_result.json) to every row's notes. Run after test.py."""
import os, csv, json
OUT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\wave3\adapters'
res = json.load(open(os.path.join(OUT, 'test', 'rows_result.json')))
rows = list(csv.DictReader(open(os.path.join(OUT, 'rows.csv'), encoding='utf-8')))
have = {r['config'] for r in rows}
HOLD_A = {'2502': 'GATE Q-HX (A7: move 2502HX to the generator later): no 2502 generator SPEC', '6400': 'GATE A6 Q-HANDMADE answered (rebuild 6400 with the generator) but no 6400 SPEC in the batch-16 tools yet',
          '6901': 'GATE TOOLCHAIN: no 6901 SPEC in the batch-16 generators'}
pend = {}
for p in csv.DictReader(open(os.path.join(OUT, 'pending_omi_A19.csv'), encoding='utf-8')):
    pend.setdefault(p['config'], []).append(f"{p['column']} {p['table_now']} -> {p['proposed']}")
seen = set()
for e in csv.DictReader(open(os.path.join(OUT, 'edits_77.csv'), encoding='utf-8')):
    c = e['config']
    if c in have or c in seen:
        continue
    seen.add(c)
    g = HOLD_A.get(e['table'], '')
    conf = []
    if c in ('6405-16-06-O', '6405-16-08-O'):
        conf.append('D3: OMi 0.844 (= Brennan B DRILL) wider than the female port it runs into -> capped at the port drill (A11), edit dropped, report to OMi')
    if c in pend:
        conf.append('OMi differs, pending A19-style approval (pending_omi_A19.csv): ' + '; '.join(pend[c]))
    rows.append(dict(table=e['table'], config=c, ready='no' if g else 'yes', missing_columns='', gates=g, conflicts=' ; '.join(conf),
                     notes='(a) Air-Way row wrongly DROP: edits_77.csv (DROP -> BUILD, OMiSKU, OMi values first, Brennan check of 2026-10-16)'))
for r in rows:
    t = res.get(r['config'])
    if t:
        r['notes'] = (r['notes'] + ' | ' if r['notes'] else '') + 'TEST: ' + t['result']
    elif r['table'] == '(no review table)':
        r['notes'] += ' | TEST: no table'
with open(os.path.join(OUT, 'rows.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'ready', 'missing_columns', 'gates', 'conflicts', 'notes']); w.writeheader(); w.writerows(rows)
import collections
print(len(rows), collections.Counter((r['ready'], 'CONFIG' in r['notes']) for r in rows))
