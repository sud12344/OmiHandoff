import json, csv, sys
R = r'C:/Users/sudha/OneDrive/Desktop/OMi_Handoff/'
d = json.load(open(R + 'tools/_out/brennan_catalog_20261001/catalog_verified.json'))
rows = list(csv.DictReader(open(R + 'tools/_out/brennan_yes_20261018/wave2/rows_tee_elbow.csv')))
want = {r['config'] for r in rows}
hits = {}
for t in d['tables']:
    for rr in t['rows']:
        if rr['pn'] in want:
            hits.setdefault(rr['pn'], []).append((t['table_id'], t['series'], t['title'], t.get('verified'), rr['values']))
for r in rows:
    c = r['config']
    print(c, r['how'], '->', len(hits.get(c, [])))
    for h in hits.get(c, []):
        print('   ', h[0], h[1], h[2], 'verified', h[3], json.dumps(h[4]))
