"""records.py (group C, 2026-10-21): Brennan CAD parameter records of OMi's compression parts.
Reads tools/_out/partcommunity_20261021/pc_final.csv (the PARTcommunity reversemap answers, exact / alias matches only) and
returns {part: {code: value}}; bite_lib() = the per-tube-dash bite-type end chain, checked to be identical on every record that
carries that dash (the B1 codes of every family and the B2 codes of the bite-x-bite families)."""
import csv, os, re, collections
H = os.path.dirname(os.path.abspath(__file__)); STAGE = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(STAGE, '..', '..', '..'))
PC = os.path.join(ROOT, 'tools', '_out', 'partcommunity_20261021', 'pc_final.csv')
SKUS = os.path.join(ROOT, '07_RAW_EXTRACTS', 'omi_feed', 'omi_skus_compression.txt')


def parse(s):
    d = {}
    for kv in re.split(r";(?=[A-Z0-9_]+=)", s or ''):
        if '=' in kv:
            k, v = kv.split('=', 1); d[k] = v
    return d


def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None


def records():
    out = {}
    for r in csv.DictReader(open(PC, encoding='utf-8')):
        if r['part'].startswith('C') and r['match'] in ('exact', 'alias') and r['params']:
            d = parse(r['params']); d['_family'] = r['family']; d['_pn'] = r['pn']; d['_match'] = r['match']
            out[r['part']] = d
    return out


def skus():
    return [l.strip() for l in open(SKUS, encoding='utf-8') if l.strip()]


BITE_CODES = ('THD', 'D', 'A', 'K', 'C', 'E', 'B', 'M', 'DN', 'F', 'OD')   # suffix-free letters: <L>B1 / B1THD / B1D
NAMES = dict(THD='thread major (B1THD)', D='through bore (B1D)', A='tube socket dia (AB1)', K='tube socket depth (KB1)',
             C='relief neck length (CB1)', E='relief neck dia (EB1)', B='hex face to nut face (BB1)', M='nut face to body tip (MB1)',
             DN='nut length (DB1)', F='nut hex (FB1)', OD='nut tube hole (ODB1)')


def bite_of(d, n):
    """the bite-end codes of end n (1 or 2) of a record, or None if the record has no bite end n"""
    g = lambda k: num(d.get(k))
    e = dict(THD=g(f'B{n}THD'), D=g(f'B{n}D'), A=g(f'AB{n}'), K=g(f'KB{n}'), C=g(f'CB{n}'), E=g(f'EB{n}'), B=g(f'BB{n}'),
             M=g(f'MB{n}'), DN=g(f'DB{n}'), F=g(f'FB{n}'), OD=g(f'ODB{n}'))
    return e if e['A'] is not None and e['K'] is not None else None


def bite_lib():
    """dash -> (chain dict, [parts it was read from]); raises on any disagreement between records"""
    seen = collections.defaultdict(list)
    for p, d in records().items():
        if d['_family'].split('/')[-1] in ('c0318', 'c0319'): continue
        dash = int(d['DN'])
        e = bite_of(d, 1)
        if e: seen[dash].append((p, 'B1', e))
        e2 = bite_of(d, 2)
        if e2: seen[int(d.get('B2', dash)) if str(d.get('B2', '')).isdigit() else dash].append((p, 'B2', e2))
    lib, bad = {}, []
    for dash, L in sorted(seen.items()):
        ref = {k: v for k, v in L[0][2].items() if k != 'D'}
        for p, n, e in L:
            for k, v in ref.items():
                if e[k] != v: bad.append((dash, p, n, k, e[k], v))
        lib[dash] = (dict(L[0][2]), sorted({p for p, n, e in L}))
    if bad: raise ValueError('bite-end records disagree: ' + repr(bad[:10]))
    return lib


if __name__ == '__main__':
    lib = bite_lib()
    for dash, (e, ps) in lib.items():
        print(f'-{dash:02d}', ' '.join(f'{k}={v}' for k, v in e.items()), f'| {len(ps)} records')
