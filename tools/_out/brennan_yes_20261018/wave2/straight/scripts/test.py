"""test.py (wave 2 straight, 2026-10-18): apply ../cells.csv to copies of today's base tables and regenerate EVERY root of the batch-16
generators (puckfix_20261009/tools_new; one process per root, python -I) on three table sets:
  untouched = base copy, nothing applied (control)
  A         = base copy + cells.csv applied with the main session's own apply script (scripts/apply_brennan.py), ready rows -> ASSUMED
  B         = A + ASSUMED also on the complete rows held only by an open decision (test/rows_scenarioB.csv) + the A11 edits of non-empty
              cells (test/edits_A11.csv)  - informative only, NOT a proposal
Outputs (in ../test): root_untouched/, root_A/, root_B/, gen_<s>/, status_<s>.json, compare.txt, rows_result.json, blocked.json
    python -I test.py [apply|regen|compare|all] [scenario ...]
"""
import os, sys, csv, json, shutil, subprocess, re
import openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
BY = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018')
OUTD = os.path.join(BY, r'wave2\straight')
TEST = os.path.join(OUTD, 'test')
BASE_DT = os.path.join(BY, r'base_root\04_DESIGN_TABLES')
TOOLS = os.path.join(ROOT, r'tools\_out\puckfix_20261009\tools_new')
APPLY = os.path.join(BY, r'scripts\apply_brennan.py')
SCEN = {'untouched': os.path.join(TEST, 'root_untouched'), 'A': os.path.join(TEST, 'root_A'), 'B': os.path.join(TEST, 'root_B')}
TARGET = [r for r in csv.DictReader(open(os.path.join(OUTD, 'rows.csv'), encoding='utf-8'))]


def run_apply(stage, rows_csv):
    assert not os.path.exists(stage), stage
    p = subprocess.run([sys.executable, '-I', '-B', APPLY, stage, os.path.join(OUTD, 'cells.csv'), '--rows', rows_csv], capture_output=True, text=True)
    open(os.path.join(TEST, f'apply_{os.path.basename(stage)}.txt'), 'w', encoding='utf-8').write(p.stdout + p.stderr)
    print(os.path.basename(stage), p.stdout.strip()[-300:], p.stderr[-800:])
    assert p.returncode == 0


def edits(stage):
    log = []
    for e in csv.DictReader(open(os.path.join(TEST, 'edits_A11.csv'), encoding='utf-8')):
        pth = os.path.join(stage, '04_DESIGN_TABLES', f"DesignTable_{e['table']}.xlsx")
        wb = openpyxl.load_workbook(pth); ws = wb.active
        hdr = {c.value: c.column for c in ws[2] if c.value}
        r = [c.row for c in ws['A'] if c.value == e['config']][0]
        cell = ws.cell(r, hdr[e['column']])
        assert abs(float(cell.value) - float(e['old'])) < 1e-9, (e, cell.value)
        cell.value = float(e['new'])
        ws.cell(r, hdr['$PRP@DataStatus']).value = 'ASSUMED'; wb.save(pth)
        log.append(f"{e['config']} {e['column']} {e['old']} -> {e['new']} (scenario B only)")
    open(os.path.join(stage, 'edits_log.txt'), 'w').write('\n'.join(log) + '\n')


def regen(scen):
    out = os.path.join(TEST, f'gen_{scen}')
    assert not os.path.exists(out), out
    os.makedirs(os.path.join(out, 'logs'))
    env = dict(os.environ, OMI_ROOT=SCEN[scen], GS_OUT=os.path.join(out, 'straight'), GT_OUT=os.path.join(out, 'tee'), PYTHONDONTWRITEBYTECODE='1')
    code = ("import sys,os,json; t=sys.argv[1]; sys.path[:0]=[os.path.join(t,'generators'),t]; import gen_straight2 as G, gen_tee as T; "
            "print(json.dumps(dict(straight=list(G.SPEC), tee=list(T.SPEC))))")
    k = subprocess.run([sys.executable, '-I', '-B', '-c', code, TOOLS], env=dict(env, GS_OUT=os.path.join(out, '_keys'), GT_OUT=os.path.join(out, '_keys')),
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if k.returncode:
        print(k.stderr); sys.exit(1)
    roots = json.loads(k.stdout.strip().splitlines()[-1])
    json.dump(roots, open(os.path.join(out, 'roots.json'), 'w'))
    status = {}
    for sub, gen in (('straight', 'gen_straight2.py'), ('tee', 'gen_tee.py')):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
        sj = os.path.join(out, sub, 'gen_straight2_summary.json' if sub == 'straight' else 'gen_tee_summary.json')
        for r in roots[sub]:
            if os.path.exists(sj): os.remove(sj)
            p = subprocess.run([sys.executable, '-I', '-B', os.path.join(TOOLS, 'generators', gen), r], env=env, capture_output=True, text=True,
                               encoding='utf-8', errors='replace')
            open(os.path.join(out, 'logs', f'{sub}_{r}.txt'), 'w', encoding='utf-8').write(p.stdout + ('\n--- STDERR ---\n' + p.stderr if p.stderr else ''))
            if os.path.exists(sj): os.replace(sj, os.path.join(out, sub, f'summary_{r}.json'))
            last = (p.stderr.strip().splitlines() or [''])[-1][:300]
            status[f'{sub}:{r}'] = dict(rc=p.returncode, err=last if p.returncode else '', out=(p.stdout.strip().splitlines() or [''])[-1][:300])
            print(scen, sub, r, 'rc', p.returncode, last if p.returncode else '', flush=True)
    json.dump(status, open(os.path.join(TEST, f'status_{scen}.json'), 'w'), indent=1)


def sw2(p):
    ws = openpyxl.load_workbook(p, data_only=True).worksheets[0]
    v = list(ws.iter_rows(values_only=True)); h = v[0]
    return h, {r[0]: dict(zip(h, r)) for r in v[1:] if r[0]}


def macro(p):
    return [l for l in open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n')
            if not re.search(r'[Gg]enerated|20\d\d-\d\d-\d\d', l)]


def compare(scens=('A', 'B')):
    rep = []
    st = {s: json.load(open(os.path.join(TEST, f'status_{s}.json'))) for s in ('untouched',) + tuple(scens)}
    target = {r['config'] for r in TARGET}
    for s in scens:
        rep.append(f'===== scenario {s} vs untouched')
        for key in sorted(st['untouched']):
            sub, r = key.split(':')
            u, a = st['untouched'][key], st[s][key]
            gu, ga = os.path.join(TEST, 'gen_untouched', sub), os.path.join(TEST, f'gen_{s}', sub)
            mu, ma = os.path.join(gu, f'Build_{r}_MASTER.bas'), os.path.join(ga, f'Build_{r}_MASTER.bas')
            tu, ta = os.path.join(gu, f'DesignTable_{r}_SW2.xlsx'), os.path.join(ga, f'DesignTable_{r}_SW2.xlsx')
            line = f'{key:22} rc {u["rc"]}->{a["rc"]}'
            if u['rc'] != a['rc']:
                line += f' | untouched: {u["err"] or u["out"]} | {s}: {a["err"] or a["out"]}'
            have_u, have_a = os.path.exists(tu), os.path.exists(ta)
            if not have_u and not have_a:
                rep.append(line + ' | no SW2 in either'); continue
            hu, ru = sw2(tu) if have_u else ((), {})
            ha, ra = sw2(ta) if have_a else ((), {})
            changed = {}
            for cfg, row in ru.items():
                if cfg not in ra:
                    changed[cfg] = 'LOST'; continue
                d = [c for c in set(row) | set(ra[cfg]) if row.get(c) != ra[cfg].get(c)]
                if d: changed[cfg] = sorted(d)
            new = [c for c in ra if c not in ru]
            same_macro, ndiff = None, 0
            if os.path.exists(mu) and os.path.exists(ma):
                lu, la = macro(mu), macro(ma)
                same_macro = lu == la
                ndiff = sum(1 for x, y in zip(lu, la) if x != y) + abs(len(lu) - len(la))
            line += f' | configs {len(ru)}->{len(ra)} new {len(new)} old-changed {len(changed)} | macro ' + (
                'identical' if same_macro else ('n/a' if same_macro is None else f'differs ({ndiff} lines)'))
            if set(hu) != set(ha) and have_u and have_a:
                line += f' | columns +{sorted(set(ha) - set(hu))} -{sorted(set(hu) - set(ha))}'
            rep.append(line)
            for c in new:
                rep.append(f'      NEW {c}' + (' (target row)' if c in target else ' (NOT a target row!)'))
            for c, d in changed.items():
                rep.append(f'      OLD CONFIG CHANGED {c}: {d if d == "LOST" else d[:12]}')
    # per target row
    rows = {}
    for s in scens:
        for key in st[s]:
            sub, r = key.split(':')
            ta = os.path.join(TEST, f'gen_{s}', sub, f'DesignTable_{r}_SW2.xlsx')
            built = set(sw2(ta)[1]) if os.path.exists(ta) else set()
            sm = os.path.join(TEST, f'gen_{s}', sub, f'summary_{r}.json')
            js = json.load(open(sm, encoding='utf-8')) if os.path.exists(sm) else {}
            for c in target:
                if c in built:
                    rows.setdefault(c, {})[s] = f'CONFIG ({key})'
            for rootk, v in js.items():
                for item in (v.get('skipped', []) + v.get('blocked', [])) if isinstance(v, dict) else []:
                    if item and item[0] in target and s not in rows.get(item[0], {}):
                        rows.setdefault(item[0], {}).setdefault(s + '_why', f'{key}: ' + ' | '.join(str(x) for x in item[1:])[:400])
    json.dump(rows, open(os.path.join(TEST, 'rows_result.json'), 'w'), indent=1)
    rep.append('\n===== target rows (ready from rows.csv)')
    blocked = {}
    for r in TARGET:
        c = r['config']; d = rows.get(c, {})
        rep.append(f"{c:20} ready={r['ready']:3} A: {d.get('A') or d.get('A_why', '-')} | B: {d.get('B') or d.get('B_why', '-')}")
        if r['ready'] == 'yes' and 'A' not in d:
            blocked[c] = d.get('A_why', 'not built (no summary entry)')
    json.dump(blocked, open(os.path.join(TEST, 'blocked_A.json'), 'w'), indent=1)
    open(os.path.join(TEST, 'compare.txt'), 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
    print('\n'.join(l for l in rep if 'NEW' in l or 'CHANGED' in l or 'rc 0->1' in l or 'rc 1->0' in l or l.startswith('=====')))
    print('blocked ready rows:', json.dumps(blocked, indent=1))


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    scens = sys.argv[2:] or ['untouched', 'A', 'B']
    if what in ('apply', 'all'):
        for s in scens:
            if s == 'untouched':
                shutil.copytree(BASE_DT, os.path.join(SCEN[s], '04_DESIGN_TABLES'))
            elif s == 'A':
                run_apply(SCEN['A'], os.path.join(OUTD, 'rows.csv'))
            else:
                run_apply(SCEN['B'], os.path.join(TEST, 'rows_scenarioB.csv')); edits(SCEN['B'])
    if what in ('regen', 'all'):
        for s in scens:
            regen(s)
    if what in ('compare', 'all'):
        compare(tuple(s for s in ('A', 'B') if os.path.exists(os.path.join(TEST, f'status_{s}.json'))))
