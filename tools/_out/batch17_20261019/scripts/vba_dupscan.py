"""vba_dupscan.py <macro.bas> ...: static scan for VBA compile errors vbacheck.py does not catch - per procedure: a name declared twice
(Dim / parameter, case-insensitive), a local name equal to a procedure name, a procedure name equal to a module-level name, a call to a
procedure that does not exist with a different argument count is not checked."""
import re, sys

for f in sys.argv[1:]:
    t = open(f, encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
    t = re.sub(r' _\n\s*', ' ', t)                      # join continuations
    lines = t.split('\n')
    procs = {m.group(1).lower() for m in re.finditer(r'^(?:Private |Public )?(?:Sub|Function) (\w+)', t, re.M)}
    modnames, cur, names, probs = set(), None, {}, []

    def decl_names(s):
        s = re.sub(r'"[^"]*"', '""', s.split("'")[0])
        out = []
        for part in re.split(r',(?![^(]*\))', s):
            m = re.match(r'\s*(?:ByVal |ByRef |Optional )?(\w+)', part)
            if m:
                out.append(m.group(1).lower())
        return out
    for i, l in enumerate(lines, 1):
        code = l.split("'")[0] if not l.strip().startswith("'") else ''
        m = re.match(r'^(?:Private |Public )?(Sub|Function) (\w+)\((.*?)\)', code)
        if m:
            cur, names = m.group(2), {}
            for n in decl_names(m.group(3)):
                if n:
                    names[n] = i
            continue
        if re.match(r'^End (Sub|Function)', code):
            cur = None
            continue
        for st in re.split(r':(?=\s*Dim )', code):
            dm = re.match(r'^\s*(Dim|Const|Static) (.*)', st)
            if not dm:
                continue
            body = dm.group(2)
            if dm.group(1) == 'Const':
                body = body.split('=')[0]
            for n in decl_names(body):
                if cur is None:
                    modnames.add(n)
                    continue
                if n in names:
                    probs.append(f'line {i} {cur}: {n} declared twice (first line {names[n]})')
                names[n] = i
                if n in procs:
                    probs.append(f'line {i} {cur}: local {n} = a procedure name')
    for p in procs & modnames:
        probs.append(f'procedure {p} = a module-level name')
    print(f, len(probs), 'problem(s)')
    for p in probs:
        print('   ', p)
