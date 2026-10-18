"""one-off edit of unblock.py (2026-10-08): either/or gates as alternatives; normalise '(new) ' question ids."""
p = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\unblock_20261008\unblock.py'
s = open(p, encoding='utf-8').read()
s = s.replace("            NEWQ[c].add(q['id'])", "            NEWQ[c].add(q['id'].replace('(new) ', ''))")
old = """                    gates.add('STEP:' + s['pn'] + (' (or a decision: ' + s['still_needed_for'][:60] + ')' if 'only if' in str(s.get('still_needed_for', '')) else ''))"""
new = """                    snf = str(s.get('still_needed_for', ''))
                    alt = sorted(set(re.findall(r'Q-[A-Z0-9-]*[A-Z0-9]', snf))) if ('only if' in snf or 'not needed at all' in snf) else []
                    gates.add('|'.join(['STEP:' + s['pn']] + alt))"""
assert old in s
s = s.replace(old, new)
a = s.index("none_user = [r for r in rows if not r['gates']]")
b = s.index("s = '\\n'.join(out)")
summary = '''def alts(g):
    return frozenset(family(a) for a in g.split('|'))


AG = [[alts(g) for g in r['gates']] for r in rows]


def freed(done):
    return [i for i, gs in enumerate(AG) if all(a & done for a in gs)]


none_user = freed(set())
p(f'\\nNO user action needed (only my work): {len(none_user)}  {dict(collections.Counter(rows[i]["source"] for i in none_user))}')
bo = freed({'Q-BRENNAN-ONLY'})
p(f'Q-BRENNAN-ONLY = yes ALONE makes {len(bo) - len(none_user)} more rows buildable (with my work): '
  f'{dict(collections.Counter(rows[i]["source"] for i in bo if i not in none_user))}')
p('  by table: ' + str(dict(collections.Counter(rows[i]['table'] for i in bo if i not in none_user).most_common())))
p(f'  Q-BRENNAN-ONLY is one of the gates (or an alternative) of {sum(1 for gs in AG if any("Q-BRENNAN-ONLY" in a for a in gs))} rows')
fams = collections.Counter()
for gs in AG:
    for f in (set().union(*gs) if gs else set()):
        fams[f] += 1
p('\\nrows touched per user action (a row can need several):')
for f, n in fams.most_common(45):
    p(f'  {n:4}  {f:42}  alone frees {len(freed({f})) - len(none_user)}')
p('\\ngreedy order (each step = the action that frees the most rows given the earlier ones; all STEP downloads pooled):')
done = set()
cur = len(none_user)
p(f'  start: {cur} rows need no user action')
for _ in range(25):
    best, bn = None, cur
    for f in fams:
        if f in done:
            continue
        n = len(freed(done | {f}))
        if n > bn:
            best, bn = f, n
    if not best:
        break
    done.add(best)
    p(f'  + {best:42} frees {bn - cur:4}  (cumulative {bn})')
    cur = bn
left = [rows[i] for i, gs in enumerate(AG) if not all(a & done for a in gs)]
p(f'  still blocked after those: {len(left)}; their gates: ' + str(collections.Counter(f for r in left for g in r['gates'] for f in alts(g)).most_common(25)))
'''
s = s[:a] + summary + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('patched')
