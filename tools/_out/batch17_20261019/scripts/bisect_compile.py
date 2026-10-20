"""bisect_compile.py <macro.bas> <out.bas> <lo> <hi> : a test module = header declarations + every procedure stubbed (signature + End)
except procedures lo..hi-1 (index order in the file) in full + an empty Sub ZZTest. Load it through run_macro (entry ZZTest): a failure means
the compile error is in procedures lo..hi-1 (names stay defined through the stubs). Prints the procedure list with indices."""
import os, re, sys

src, out, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
t = open(src, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
starts = [m.start() for m in re.finditer(r'^(?:Private |Public )?(?:Sub|Function) \w+', t, re.M)]
header = t[:starts[0]]
procs = [t[a:b] for a, b in zip(starts, starts[1:] + [len(t)])]


def stub(p):
    sig = []
    for l in p.split('\n'):
        sig.append(l)
        if not l.rstrip().endswith(' _'):
            break
    kind = 'Function' if re.match(r'(?:Private |Public )?Function', p) else 'Sub'
    return '\n'.join(sig) + f'\nEnd {kind}\n\n'


body = ''.join(p if lo <= j < hi else stub(p) for j, p in enumerate(procs))
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8', newline='\r\n').write(header + body + '\nSub ZZTest()\nEnd Sub\n')
print(len(procs), 'procedures; full:', [re.match(r'(?:Private |Public )?(?:Sub|Function) (\w+)', procs[j]).group(1) for j in range(lo, min(hi, len(procs)))])
