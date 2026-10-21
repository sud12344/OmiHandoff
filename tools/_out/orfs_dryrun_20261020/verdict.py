"""verdict.py (2026-10-20): read the call.py logs out_*.txt of the ORFS dry runs -> VERDICT.txt, one line per root:
macro report OK / FAIL counts, sweep (configurations, not ok), thread check (bad configurations), screenshot path.
usage: python verdict.py [out_g1.txt ...]   (default: every out_*.txt here)"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def parse(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    res = {}
    for blk in re.split(r'^=== ', txt, flags=re.M)[1:]:
        head, _, body = blk.partition('\n')
        tool = head.split(' ', 1)[0]
        body = body.split('\n--- ')[0].strip()
        img = re.findall(r'\[image [^\]]*-> ([^\]]+)\]', body)
        js = next((l for l in body.splitlines() if l.startswith('{')), None)
        try:
            j = json.loads(js) if js else {}
        except ValueError:
            j = {'_raw': js[:300]}
        if tool == 'run_macro':
            m = re.search(r'Build_(\w+?)_MASTER\.bas', head)
            root = m.group(1)
            rep = j.get('report') or {}
            res[root] = dict(ran=j.get('ok'), err=j.get('error'), secs=j.get('secs'), ok=rep.get('ok'), fail=rep.get('fail'),
                             fail_lines=rep.get('fail_lines', []), msg=(j.get('msgbox') or [''])[0])
        elif tool == 'sweep_configs':
            root = j.get('doc', '').replace('_MASTER', '')
            rows = [r for r in j.get('rows', []) if r.get('config') != 'Default']
            res.setdefault(root, {}).update(cfgs=len(rows), sweep_bad=[r['config'] for r in rows if not r.get('ok') or r.get('bodies') != 1],
                                             sweep_err=j.get('error'))
        elif tool == 'run_python':
            r = j.get('result') or {}
            root = str(r.get('thdcheck', '')).replace('_MASTER', '')
            if root:
                res.setdefault(root, {}).update(thd_n=r.get('n'), thd_bad=r.get('bad'), thd_rows=r.get('rows'))
            elif j.get('error'):
                res.setdefault('_python_errors', []).append(j.get('error'))
        elif tool == 'screenshot':
            root = j.get('doc', '').replace('_MASTER', '')
            res.setdefault(root, {})['shot'] = j.get('saved') or (img[0] if img else None)
    return res


def main(files):
    allres = {}
    for f in files:
        allres.update(parse(f))
    lines = []
    for root, r in allres.items():
        if root.startswith('_'):
            lines.append(f'{root}: {r}')
            continue
        good = (r.get('ran') and not r.get('fail') and r.get('cfgs') and not r.get('sweep_bad') and r.get('thd_bad') == [])
        lines.append(f"{'PASS' if good else 'CHECK'}  {root:9} macro ok {r.get('ok')} fail {r.get('fail')}  configs {r.get('cfgs')}"
                     f"  sweep bad {r.get('sweep_bad')}  thread-check bad {len(r.get('thd_bad') or []) if r.get('thd_bad') is not None else 'n/a'}"
                     f"  {r.get('secs')} s")
        for fl in r.get('fail_lines') or []:
            lines.append(f'        {fl}')
        for b in r.get('thd_bad') or []:
            lines.append(f'        thread: {b}')
        if r.get('err'):
            lines.append(f"        macro error: {r['err']}")
        if r.get('shot'):
            lines.append(f"        shot: {r['shot']}")
    out = '\n'.join(lines)
    open(os.path.join(HERE, 'VERDICT.txt'), 'w', encoding='utf-8').write(out + '\n')
    print(out)


if __name__ == '__main__':
    main(sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, 'out_*.txt'))))
