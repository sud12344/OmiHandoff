"""make_calls.py (2026-10-20): call files for the ORFS SolidWorks dry runs (CLAUDE.md verify loop), run with
    python sw_mcp/call.py @tools/_out/orfs_dryrun_20261020/calls_<group>.json > tools/_out/orfs_dryrun_20261020/out_<group>.txt
Per root: run_macro (TABLE / SAVE / REPORT -> staging + this folder, 11_MASTERS untouched), sweep_configs, a thread check
(every configuration: 1 body with THD_* suppressed and live, threads live without error and removing material), a section
screenshot of the reference configuration, close_doc (discard).
usage: python make_calls.py <group> <root> [<root> ...]"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
GEN = os.path.join(REPO, 'tools', '_out', 'orfs_gen_20261020', 'out')

THDCHECK = r'''
def _thdcheck(title):
    d = get_doc(title)
    cfgs = [c for c in d.GetConfigurationNames() if c != 'Default']
    ref = d.ConfigurationManager.ActiveConfiguration.Name
    rows = []
    for cfg in cfgs:
        d.ShowConfiguration2(cfg)
        thd = [f for f in iter_features(d) if f.Name.startswith('THD_')]
        for f in thd: f.SetSuppression2(0, 1, None)
        d.ForceRebuild3(False)
        b0 = len(solid_bodies(d)); v0 = mass_props(d)['volume']
        thd = [f for f in iter_features(d) if f.Name.startswith('THD_')]
        for f in thd: f.SetSuppression2(1, 1, None)
        d.ForceRebuild3(False)
        thd = [f for f in iter_features(d) if f.Name.startswith('THD_')]
        b1 = len(solid_bodies(d)); v1 = mass_props(d)['volume']
        live = [f.Name for f in thd if f.IsSuppressed2(1, None)[0] is False]
        errs = [(f.Name, f.GetErrorCode2()[0]) for f in thd if f.GetErrorCode2()[0] != 0]
        for f in thd: f.SetSuppression2(0, 1, None)
        rows.append(dict(cfg=cfg, bodies=(b0, b1), vol_in3=round(v0 / IN ** 3, 4),
                         thd_cut_pct=round(100 * (v0 - v1) / v0, 2) if v0 else None, n_thd=len(thd), live=len(live), thd_err=errs))
    d.ShowConfiguration2(ref); d.ForceRebuild3(False)
    bad = [r for r in rows if r['bodies'] != (1, 1) or r['thd_err'] or r['live'] != r['n_thd']
           or (r['n_thd'] and (not r['thd_cut_pct'] or r['thd_cut_pct'] <= 0))]
    return dict(thdcheck=title, n=len(rows), n_bad=len(bad), bad=bad, rows=[(r['cfg'], r['vol_in3'], r['thd_cut_pct'], r['n_thd']) for r in rows])
result = _thdcheck(%r)
'''


def where(root):
    for sub in ('', 'tee', 'ring'):
        p = os.path.join(GEN, sub, f'Build_{root}_MASTER.bas')
        if os.path.exists(p):
            return os.path.dirname(p)
    raise SystemExit(f'no macro for {root}')


def calls(root):
    src = where(root)
    out = os.path.join(HERE, root)
    os.makedirs(out, exist_ok=True)
    doc = f'{root}_MASTER'
    return [
        ['run_macro', dict(path=os.path.join(src, f'Build_{root}_MASTER.bas'), timeout_s=1750, const_overrides=dict(
            TABLE_PATH=os.path.join(src, f'DesignTable_{root}_SW2.xlsx'),
            SAVE_PATH=os.path.join(out, f'{doc}.SLDPRT'),
            REPORT_PATH=os.path.join(out, f'Build_{root}_report.txt')))],
        ['sweep_configs', dict(doc=doc, timeout_s=1700)],
        ['run_python', dict(code=THDCHECK % doc, timeout_s=1700)],
        ['screenshot', dict(doc=doc, views=['isometric', 'front'], section_plane='Front Plane', width=1000)],
        ['close_doc', dict(doc=doc, discard_unsaved=True)],
    ]


if __name__ == '__main__':
    group, roots = sys.argv[1], sys.argv[2:]
    seq = [['sw_status', {}]] + [c for r in roots for c in calls(r)] + [['sw_status', {}]]
    p = os.path.join(HERE, f'calls_{group}.json')
    json.dump(seq, open(p, 'w', encoding='utf-8'), indent=1)
    print(p, len(roots), 'roots')
