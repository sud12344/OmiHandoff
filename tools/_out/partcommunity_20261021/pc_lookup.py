"""pc_lookup.py (2026-10-21, cloud): ask Brennan's CADENAS PARTcommunity catalog (public reversemap service, no login) whether a CAD
model exists for each not-ready OMi part, and keep the model's parameter record (the values that drive Brennan's CAD = the STEP's
source). Read-only towards the library; writes only this folder.

Service: https://webapi.partcommunity.com/service/reversemap?catalog=brennan&part=<pn>&exact=0
 -> {"mident": "{$CADENAS_DATA/23d-libs/brennan/<family>/<file>.prj},... {NB=<pn>},{KEY=value},..."}  or  {"error": "no valid mapping found"}
Tried per OMi part, in order, until one answers: the OMi number, then Brennan's known numbering differences (-TUBE dropped: Brennan's
swept elbows carry no suffix; 6408-HHP-NN-O -> 6408-HNN-O; 5406-HHP -> 5406-HP; 0618 / 0619 -> V0318 / V0319; FS0304-C-NN-ASY ->
FS0304-C-NN). A record found under another number says so (tried_as). One request per second; results are cached in cache.json
(re-runs only ask what is not cached).
Writes: cache.json (raw answers), pc_results.csv (one row per OMi part), pc_summary.json.
Usage: python -I pc_lookup.py <list of part numbers>"""
import os, sys, re, json, csv, time, urllib.request, urllib.parse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache.json')
URL = 'https://webapi.partcommunity.com/service/reversemap?catalog=brennan&part={}&exact=0'
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def ask(pn):
    if pn in cache:
        return cache[pn]
    for attempt in range(4):
        try:
            with urllib.request.urlopen(URL.format(urllib.parse.quote(pn)), timeout=30) as r:
                ans = json.loads(r.read().decode('utf-8', 'replace'))
            break
        except Exception as e:  # network hiccup: back off and retry, then record the failure (not cached)
            ans = {'error': f'request failed: {e}'}; time.sleep(2 ** (attempt + 1))
    if not ans.get('error', '').startswith('request failed'):
        cache[pn] = ans
        if len(cache) % 25 == 0:
            json.dump(cache, open(CACHE, 'w'), indent=0)
    time.sleep(1.0)
    return ans


def variants(p):
    v = [p]
    if p.endswith('-TUBE'): v.append(p[:-5])
    m = re.match(r'^6408-HHP-(\d\d)-O$', p)
    if m: v.append(f'6408-H{m.group(1)}-O')
    if p.startswith('5406-HHP-'): v.append(p.replace('5406-HHP-', '5406-HP-'))
    if re.match(r'^06(18|19)-', p): v.append('V03' + p[2:])
    if p.endswith('-ASY'): v.append(p[:-4])
    # second pass (2026-10-21): Brennan's forged / plain suffix may differ from OMi's (OMi C2404-04-04 = Brennan C2404-04-04-FG)
    for b in list(v):
        if b.endswith('-NWO-FG'): v += [b[:-3], b[:-7]]
        elif b.endswith('-FG'): v.append(b[:-3])
        elif not b.endswith(('-O', '-TUBE')): v += [b + '-FG', b + '-NWO-FG']
    return list(dict.fromkeys(v))


def parse(mident):
    fam = re.match(r'\{\$CADENAS_DATA/23d-libs/brennan/([^}]*)\.prj\}', mident)
    kv = dict(re.findall(r'\{([A-Z0-9_]+)=([^{}]*)\}', mident))
    return (fam.group(1) if fam else ''), kv


parts = [l.strip().upper() for l in open(sys.argv[1]) if l.strip()]
rows = []
for i, p in enumerate(parts, 1):
    hit, tried = None, None
    for v in variants(p):
        a = ask(v)
        if 'mident' in a:
            hit, tried = a, v; break
    if hit:
        fam, kv = parse(hit['mident'])
        rows.append(dict(part=p, found='yes', tried_as=tried if tried != p else '', family=fam, pn=kv.get('PN', kv.get('NB', '')),
                         params=';'.join(f'{k}={v.strip()}' for k, v in kv.items() if k not in ('NB', 'LINA', 'KT', 'PN', 'WBNUMERIC', 'LINEID'))))
    else:
        rows.append(dict(part=p, found='no', tried_as=' / '.join(variants(p)[1:]), family='', pn='', params=''))
    if i % 50 == 0:
        print(f'{i}/{len(parts)} done, {sum(r["found"] == "yes" for r in rows)} found', flush=True)
json.dump(cache, open(CACHE, 'w'), indent=0)
with open(os.path.join(HERE, 'pc_results.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
summ = dict(parts=len(rows), found=sum(r['found'] == 'yes' for r in rows),
            found_by_family=dict(collections.Counter(r['family'] for r in rows if r['found'] == 'yes').most_common()))
json.dump(summ, open(os.path.join(HERE, 'pc_summary.json'), 'w'), indent=1)
print(json.dumps(summ, indent=1))
