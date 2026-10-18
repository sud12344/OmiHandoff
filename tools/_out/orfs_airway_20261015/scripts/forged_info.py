"""forged_info.py (2026-10-15): INFORMATION ONLY - how often Air-Way's NON-forged ORFS rows print the same leg lengths / hexes as
Brennan's forged (-FG) rows of the same size. Nothing is built from this (user rule: no -FG part from non-forged Air-Way rows); it is
the evidence for the user if they want to revisit that rule for ORFS.

Column pairs by drawing meaning (Brennan letters vs Air-Way letters on the same view): leg lengths in side order, JJ FLATS = the
forged body flats (Air-Way S2 / S3 = body hex), C HEX = swivel nut / locknut hex. Where the meaning is unclear the pair is not used.
python -I forged_info.py  ->  ../forged_info.json + printed summary"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import load
from compare_orfs import cmp_num, dashes

from compare_orfs import FORGED_PAIRS as P      # one list of column pairs (moved to compare_orfs.py 2026-10-15)


def main():
    A, B = load.airway(), load.brennan()
    out = {}
    tot = collections.Counter()
    for bs, (ac, pairs) in P.items():
        brow = {}
        for t in B:
            if t['series'] == bs:
                for r in t['rows']:
                    brow.setdefault(dashes(r['pn']), (t, r))
        arow = {}
        for r in A[ac]['rows']:
            arow.setdefault(dashes(r['pn']), r)
        common = [k for k in brow if k in arow]
        per = collections.OrderedDict()
        for bc, acol in pairs:
            res = collections.Counter(cmp_num(arow[k]['values'].get(acol), brow[k][1]['values'].get(bc)) for k in common)
            per[f'{bc} ~ {acol}'] = dict(equal=res['equal'] + res['rounding_only'], different=res['different'], not_compared=res[None])
            tot['equal'] += res['equal'] + res['rounding_only']; tot['different'] += res['different']
        rows_all = sum(1 for k in common if all(cmp_num(arow[k]['values'].get(acol), brow[k][1]['values'].get(bc)) in ('equal', 'rounding_only') for bc, acol in pairs))
        out[bs] = dict(airway=ac, sizes_in_both=len(common), rows_all_equal=rows_all, columns=per)
        print(f'{bs:<17} vs {ac:<9} sizes in both {len(common):>3}  all cells equal on {rows_all:>3}   ' +
              '  '.join(f'{k}: {v["equal"]}/{v["equal"] + v["different"]}' for k, v in per.items()))
    json.dump(dict(note=__doc__, series=out, cells=dict(tot)), open(os.path.join(load.HERE, 'forged_info.json'), 'w', encoding='utf-8'), indent=1)
    print('cells equal', tot['equal'], 'different', tot['different'])


if __name__ == '__main__':
    main()
