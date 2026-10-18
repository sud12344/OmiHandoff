p = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018\wave3\orfs\scripts\build.py'
s = open(p, encoding='utf-8').read()
old = "            add(col, val, src, 'brennan-dim')\n"
new = """            res, ex = confirm.get((stem, col), (collections.Counter(), []))
            nn = sum(res.values())
            if nn and (res['equal'] + res['rounding_only']) * 2 < nn:
                conflicts.append(f'{col}: Brennan "{bcol}" agrees with Air-Way {col} on only {res["equal"] + res["rounding_only"]}/{nn} rows of this table '
                                 f'({"; ".join(ex)}) - same meaning on both drawings, different sizes: this row would be Brennan-sized in an Air-Way-sized table')
            add(col, val, src, 'brennan-dim')
"""
assert s.count(old) == 1
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
