"""wave2 tee_elbow TEST (2026-10-18).
  test/root_untouched/04_DESIGN_TABLES = copy of base (control)
  test/root/04_DESIGN_TABLES          = base + cells.csv applied with the main session's apply_brennan.py (DataStatus ASSUMED on ready rows)
Regenerates the affected gen_tee roots on both (python -I, one process per root, GT_OUT / GS_OUT inside test/), compares SW2 tables
and macros, writes test/compare.txt + test/rows_result.json.     python -I -B test.py [apply|regen|compare|all]
"""
import os, sys, csv, json, shutil, subprocess, re
import openpyxl
R = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
OUT = os.path.join(R, r'tools\_out\brennan_yes_20261018\wave2\tee_elbow')
TEST = os.path.join(OUT, 'test')
BASE = os.path.join(R, r'tools\_out\brennan_yes_20261018\base_root\04_DESIGN_TABLES')
TOOLS = os.path.join(R, r'tools\_out\puckfix_20261009\tools_new')
APPLY = os.path.join(R, r'tools\_out\brennan_yes_20261018\scripts\apply_brennan.py')
SCEN = {'untouched': os.path.join(TEST, 'root_untouched'), 'test': os.path.join(TEST, 'root')}
TEE = ['1501', '1503', '2501', '2505', '2602', '2606', '2609', '2611', '5502', '5504', '5604']
rows = list(csv.DictReader(open(os.path.join(OUT, 'rows.csv'), encoding='utf-8')))
target = {r['config']: r for r in rows}


def apply():
    os.makedirs(TEST, exist_ok=True)
    assert not os.path.exists(SCEN['untouched']) and not os.path.exists(SCEN['test'])
    shutil.copytree(BASE, os.path.join(SCEN['untouched'], '04_DESIGN_TABLES'))
    p = subprocess.run([sys.executable, '-I', '-B', APPLY, SCEN['test'], os.path.join(OUT, 'cells.csv'), '--rows', os.path.join(OUT, 'rows.csv')],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    open(os.path.join(TEST, 'apply_stdout.txt'), 'w', encoding='utf-8').write(p.stdout + p.stderr)
    print(p.stdout, p.stderr)
    assert p.returncode == 0


def regen(scen):
    out = os.path.join(TEST, f'gen_{scen}')
    assert not os.path.exists(out), out
    os.makedirs(os.path.join(out, 'logs')); os.makedirs(os.path.join(out, 'tee'))
    env = dict(os.environ, OMI_ROOT=SCEN[scen], GS_OUT=os.path.join(out, 'straight'), GT_OUT=os.path.join(out, 'tee'), PYTHONDONTWRITEBYTECODE='1')
    st = {}
    sj = os.path.join(out, 'tee', 'gen_tee_summary.json')
    for r in TEE:
        if os.path.exists(sj): os.remove(sj)
        p = subprocess.run([sys.executable, '-I', '-B', os.path.join(TOOLS, 'generators', 'gen_tee.py'), r], env=env, capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        open(os.path.join(out, 'logs', f'tee_{r}.txt'), 'w', encoding='utf-8').write(p.stdout + ('\n--- STDERR ---\n' + p.stderr if p.stderr else ''))
        if os.path.exists(sj): os.replace(sj, os.path.join(out, 'tee', f'summary_{r}.json'))
        st[r] = dict(rc=p.returncode, err=(p.stderr.strip().splitlines() or [''])[-1][:300] if p.returncode else '',
                     out=' | '.join(l for l in p.stdout.splitlines() if l.startswith(r + ':'))[:300])
        print(scen, r, st[r], flush=True)
    json.dump(st, open(os.path.join(TEST, f'status_{scen}.json'), 'w'), indent=1)


def sw2(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    v = list(ws.iter_rows(values_only=True)); h = v[0]
    return h, {r[0]: dict(zip(h, r)) for r in v[1:] if r[0]}


def macro(p):
    return [l for l in open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n') if not re.search(r'[Gg]enerated|20\d\d-\d\d-\d\d', l)]


def compare():
    rep, res = [], {}
    st = {s: json.load(open(os.path.join(TEST, f'status_{s}.json'))) for s in SCEN}
    for r in TEE:
        gu, ga = os.path.join(TEST, 'gen_untouched', 'tee'), os.path.join(TEST, 'gen_test', 'tee')
        u, a = st['untouched'][r], st['test'][r]
        line = f'{r}: rc {u["rc"]}->{a["rc"]} | untouched: {u["out"] or u["err"]} | test: {a["out"] or a["err"]}'
        tu, ta = os.path.join(gu, f'DesignTable_{r}_SW2.xlsx'), os.path.join(ga, f'DesignTable_{r}_SW2.xlsx')
        hu, ru = sw2(tu) if os.path.exists(tu) else ((), {})
        ha, ra = sw2(ta) if os.path.exists(ta) else ((), {})
        changed = {}
        for cfg, row in ru.items():
            if cfg not in ra:
                changed[cfg] = 'LOST'; continue
            dd = sorted(c for c in set(row) | set(ra[cfg]) if row.get(c) != ra[cfg].get(c))
            if dd: changed[cfg] = dd
        new = [c for c in ra if c not in ru]
        mu, ma = os.path.join(gu, f'Build_{r}_MASTER.bas'), os.path.join(ga, f'Build_{r}_MASTER.bas')
        md = 'n/a'
        if os.path.exists(mu) and os.path.exists(ma):
            lu, la = macro(mu), macro(ma)
            md = 'identical' if lu == la else f'differs ({sum(1 for x, y in zip(lu, la) if x != y) + abs(len(lu) - len(la))} lines)'
        rep.append(line)
        rep.append(f'    configs {len(ru)} -> {len(ra)}; new {len(new)}; pre-existing changed {len(changed)}; macro {md}; columns +{sorted(set(ha) - set(hu))} -{sorted(set(hu) - set(ha))}')
        for c in new:
            rep.append(f'    NEW {c}' + (' (target row)' if c in target else ' (NOT a target row!)'))
        for c, dd in changed.items():
            rep.append(f'    PRE-EXISTING CHANGED {c}: {dd if dd == "LOST" else dd[:12]}')
        sm = os.path.join(ga, f'summary_{r}.json')
        js = json.load(open(sm, encoding='utf-8')) if os.path.exists(sm) else {}
        js = js.get(r, js) if isinstance(js, dict) else {}
        for b in js.get('blocked', []) or []:
            pn = b.split(':')[0]
            if pn in target:
                rep.append(f'    BLOCKED target {b[:400]}')
                res[pn] = 'BLOCKED: ' + b[len(pn) + 2:][:400]
        for s in js.get('skipped', []) or []:
            pn = str(s).split(':')[0].split(' ')[0]
            if pn in target:
                rep.append(f'    SKIPPED target {str(s)[:300]}')
                res.setdefault(pn, 'SKIPPED: ' + str(s)[:300])
        for c in ra:
            if c in target:
                res[c] = f'CONFIG ({r})'
    rep.append('\n===== target rows (generator-covered tables)')
    for c, r in target.items():
        root = '2501' if r['table'] == '2501LL' else r['table']
        if root in TEE:
            rep.append(f'{c:22} ready={r["ready"]:3} -> {res.get(c, "not built (DataStatus not ASSUMED/VERIFIED or not in table)")}')
    json.dump(res, open(os.path.join(TEST, 'rows_result.json'), 'w'), indent=1)
    open(os.path.join(TEST, 'compare.txt'), 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))


if __name__ == '__main__':
    w = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if w in ('apply', 'all'): apply()
    if w in ('regen', 'all'):
        for s in SCEN: regen(s)
    if w in ('compare', 'all'): compare()
