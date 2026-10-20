"""count_ready.py (2026-10-20): how many of OMi's 2,535 carbon-steel parts are (a) in a shipped master now, (b) generated and ready for the
SolidWorks dry runs + ship (batch 17 + the ORFS staging), (c) neither. Read-only.
- universe: the union of OMi's website lists in 07_RAW_EXTRACTS/omi_feed (omi_skus_all / _cs_adapters_full / _orfs / _compression / _testgauge)
- shipped: every configuration of the shipped SW2 tables in 04_DESIGN_TABLES (the batch-16 state; = the built masters)
- generated: every configuration the staging toolset (tools/_out/orfs_gen_20261020/tools = merged batch-17 tools + ORFS) writes from the
  batch-17 stage + the staged ORFS tables (its regress_all.py output regen/new/**), BLOCKED rows excluded; + the O-ring master 4000 as the
  staging gen_ring writes it (tools/_out/orfs_gen_20261020/out/ring: the 21 rows 4000 / 4001, SolidWorks dry run clean 2026-10-14, + the 8
  FS4000 face-seal O-rings, 2026-10-20)
A configuration counts for the OMi part it names ($PRP@OMiSKU where present, else its part number; spaces -> dashes, upper case)."""
import os, glob, json, re, collections
import openpyxl
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
norm = lambda s: re.sub(r'\s+', '-', str(s).strip()).upper()
uni = set()
for f in ('omi_skus_all', 'omi_skus_cs_adapters_full', 'omi_skus_orfs', 'omi_skus_compression', 'omi_skus_testgauge'):
    for l in open(os.path.join(ROOT, '07_RAW_EXTRACTS', 'omi_feed', f + '.txt'), encoding='utf-8'):
        if l.strip(): uni.add(norm(l.split('\t')[0].split(',')[0]))


def sw2_parts(paths):
    out = {}
    for p in paths:
        ws = openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0]
        rows = list(ws.iter_rows(values_only=True)); h = rows[0]
        for r in rows[1:]:
            if not r[0]: continue
            d = dict(zip(h, r))
            if str(d.get('$PRP@DataStatus') or '').upper() == 'BLOCKED': continue
            out[norm(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or r[0])] = os.path.basename(p).replace('DesignTable_', '').replace('_SW2.xlsx', '')
    return out


shipped = sw2_parts(glob.glob(os.path.join(ROOT, '04_DESIGN_TABLES', '*_SW2.xlsx')))
gen = sw2_parts(glob.glob(os.path.join(ROOT, 'tools', '_out', 'orfs_gen_20261020', 'regen', 'new', '*', '*_SW2.xlsx')))
oring = sw2_parts([os.path.join(ROOT, 'tools', '_out', 'orfs_gen_20261020', 'out', 'ring', 'DesignTable_4000_SW2.xlsx')])
ready = {**shipped, **gen, **oring}
res = collections.OrderedDict()
res['universe (OMi website, carbon steel)'] = len(uni)
res['shipped now (configurations in a master), OMi parts'] = len(set(shipped) & uni)
res['generated, waiting for the SolidWorks dry runs + ship'] = len((set(gen) | set(oring)) & uni - set(shipped))
res['  of which ORFS (FS...)'] = len({p for p in (set(gen) & uni) - set(shipped) if p.startswith('FS')})
res['  of which ORFS loose parts FS0306 / FS0318 / FS0319'] = len({p for p in (set(gen) & uni) - set(shipped) if p.startswith(('FS0306', 'FS0318', 'FS0319'))})
res['  of which O-rings 4000 / 4001 / FS4000'] = len((set(oring) & uni) - set(shipped))
res['    (FS4000 face-seal O-rings)'] = len({p for p in (set(oring) & uni) - set(shipped) if p.startswith('FS4000')})
res['= ready after SolidWorks'] = len(set(ready) & uni)
res['not yet (data, STEP, decision or OMi needed)'] = len(uni - set(ready))
res['configurations not matching an OMi part number (not counted)'] = len(set(ready) - uni)
ns = sorted(set(ready) - uni)
json.dump(dict(summary=res, not_in_universe=ns, shipped_not_regenerated=sorted(set(shipped) - set(gen))), open(os.path.join(HERE, 'count_ready.json'), 'w'), indent=1)
for k, v in res.items(): print(f'{k:65} {v:5}')
print('examples not matching:', ns[:15])
