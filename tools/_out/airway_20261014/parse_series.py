"""parse_series.py (2026-10-14): turn an Air-Way series API response (parts.air-way.com/api/series/<id>, saved as JSON)
into a pipe-delimited table (header + one line per part, values verbatim as Air-Way stores them).

python -I parse_series.py <series.json> [--keys]     (--keys: print the JSON structure instead)"""
import json, sys


def walk_keys(o, path='', depth=0, out=None):
    out = [] if out is None else out
    if depth > 4:
        return out
    if isinstance(o, dict):
        for k, v in o.items():
            t = type(v).__name__ + (f'[{len(v)}]' if isinstance(v, (list, dict)) else '')
            out.append(f'{path}.{k}: {t}')
            if isinstance(v, (dict, list)):
                walk_keys(v, f'{path}.{k}', depth + 1, out)
    elif isinstance(o, list) and o:
        walk_keys(o[0], path + '[0]', depth + 1, out)
    return out


def table(d):
    """columns in Air-Way's own order (SeriesProperties), rows in Air-Way's display order (Sequence)"""
    props = d['Series']['SeriesProperties']
    cols = [(str(p['Id']), (p['DisplayName'] or '').strip()) for p in props]
    rows = []
    for part in sorted(d['Series']['Products'], key=lambda p: p.get('Sequence') or 0):
        vals = {k: (v or {}).get('Value') for k, v in (part.get('AssocTableValues') or {}).items()}
        rows.append([part.get('ItemNumber')] + [vals.get(i) for i, _ in cols]
                    + [part.get('AirwayPartNumber'), 'yes' if part.get('Has3DModel') else 'no'])
    return ['Part #'] + [c for _, c in cols] + ['Air-Way stock no.', '3D model'], rows


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')      # the tables carry +/- and degree signs; the Windows console default is cp1252
    d = json.load(open(sys.argv[1], encoding='utf-8'))
    if '--keys' in sys.argv:
        print('\n'.join(walk_keys(d)))
    else:
        head, rows = table(d)
        print(' | '.join(head))
        for r in rows:
            print(' | '.join('' if v is None else str(v) for v in r))
