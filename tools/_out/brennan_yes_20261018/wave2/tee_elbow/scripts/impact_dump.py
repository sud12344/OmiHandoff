import json, csv, sys
R = r'C:/Users/sudha/OneDrive/Desktop/OMi_Handoff/'
I = R + 'tools/_out/brennan_catalog_20261001/impact/'
want = {r['config']: r for r in csv.DictReader(open(R + 'tools/_out/brennan_yes_20261018/wave2/rows_tee_elbow.csv'))}
out = {}
for g in ['F1a', 'F1b', 'F2a', 'F2b', 'F3', 'F45D']:
    j = json.load(open(I + g + '.json', encoding='utf-8'))
    for r in j['rows']:
        c = r.get('config') or r.get('pn') or r.get('part_number')
        if c in want:
            out[c] = dict(r, impact_file=g)
json.dump(out, open('impact_rows.json', 'w'), indent=1)
print(len(out), 'of', len(want)); print(sorted(set(want) - set(out)))
k = sys.argv[1] if len(sys.argv) > 1 else '2505-12-12-FG'
print(json.dumps(out.get(k), indent=1)[:6000])
