"""wave2_split.py: the A-existing Brennan rows not handled in wave 1, split into 3 agent groups -> ../wave2/rows_<group>.csv"""
import csv, os, collections

BY = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018'
B = [r for r in csv.DictReader(open(os.path.join(BY, 'brennan_rows.csv'), encoding='utf-8')) if r['group'] == 'A-existing']
done = set()
for f in ('b15held_rows.csv', 'w1brennan_rows.csv'):
    done |= {r['config'] for r in csv.DictReader(open(os.path.join(BY, 'wave1', f), encoding='utf-8-sig'))}
OMI_TODAY = {'1405-04-06', '1405-08-12', '1502-06-06-FG', '1502-12-08-FG', '1502-12-12-FG', '1502-20-20-FG', '1502-24-24-FG', '1502-32-32-FG',
             '1504-20-20-FG', '1602-02-02-02-FG', '1602-04-04-04-FG', '1602-08-08-08-FG', '1602-16-16-16-FG', '1602-20-20-20-FG', '6410-16-04-O',
             '6410-20-06-O', '6410-20-08-O', '6410-32-12-O', '6410-32-16-O'}
FLANGE_HOSE = {'1700', '1703', '1704', '1800', '1803', '1804', '1824', '1724', '4501', '4503', '4601', '4603'}
STRAIGHT = {'0304', '0306', '1405', '2403', '2403LH', '2404L', '2405', '2406', '2408', '2700', '2705', '2706', '5000', '5404', '5404N', '5405',
            '5406', '5406C', '5406P', '6400', '6405', '6408', '6410', '6420', '6425', '6504', '6505', '6506', '6900', '3474'}
G = collections.defaultdict(list)
for r in B:
    if r['config'] in done or r['config'] in OMI_TODAY:
        continue
    g = 'flange_hose' if r['table'] in FLANGE_HOSE else 'straight' if r['table'] in STRAIGHT else 'tee_elbow'
    G[g].append(r)
os.makedirs(os.path.join(BY, 'wave2'), exist_ok=True)
for g, rows in G.items():
    with open(os.path.join(BY, 'wave2', f'rows_{g}.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(g, len(rows), dict(collections.Counter(r['how'] for r in rows)), sorted(collections.Counter(r['table'] for r in rows).items()))
