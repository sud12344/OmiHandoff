import openpyxl, csv, json
R = r'C:/Users/sudha/OneDrive/Desktop/OMi_Handoff/'
wb = openpyxl.load_workbook(R + '07_RAW_EXTRACTS/omi_dimensions/WebsitePartsInfo2026.xlsx', read_only=True, data_only=True)
ws = wb['Items']
rows = list(ws.iter_rows(values_only=True))
hdr = rows[0]; print(hdr)
want = {r['config'] for r in csv.DictReader(open(R + 'tools/_out/brennan_yes_20261018/wave2/rows_tee_elbow.csv'))}
pncol = [i for i, h in enumerate(hdr) if h and 'Part' in str(h)][0]
out = {}
for i, r in enumerate(rows[1:], start=2):
    if r[pncol] in want:
        d = {hdr[j]: r[j] for j in range(len(hdr)) if r[j] not in (None, '')}
        out[r[pncol]] = dict(row=i, **{str(k): v for k, v in d.items()})
json.dump(out, open('omi_rows.json', 'w'), indent=1, default=str)
print(len(out))
for k in sorted(out): print(k, {kk: vv for kk, vv in out[k].items() if kk not in ('Part Number','Description','Title')})
