import re, sys

KEYWORDS = set('''If Then Else ElseIf End For Next To Step Do Loop While Until Wend Set Dim ReDim Preserve As New Call Exit Sub Function
Select Case With On Error Resume GoTo Not And Or Xor Mod Is Nothing True False Empty Null Me Print Open Close Output Append Input
Private Public Const Option Explicit Attribute Debug Each In Let Get Put Type Enum Static Byval ByVal ByRef Optional Integer Long
Double Single String Boolean Variant Object Date Byte Currency'''.split())


def procs(text):
    out = []
    lines = text.split('\n')
    cur = None
    for i, l in enumerate(lines):
        m = re.match(r'^\s*(?:Private |Public )?(Sub|Function)\s+(\w+)\s*\((.*?)\)', l)
        if m and cur is None:
            cur = dict(kind=m.group(1), name=m.group(2), params=m.group(3), start=i, body=[])
            continue
        if cur is not None:
            if re.match(r'^\s*End (Sub|Function)\s*$', l):
                cur['end'] = i; out.append(cur); cur = None
            else:
                cur['body'].append(l)
    return out


def check(text):
    errs = []
    text = text.replace('\r\n', '\n')
    ps = procs(text)
    names = [p['name'] for p in ps]
    for n in set(names):
        if names.count(n) > 1: errs.append(f'duplicate procedure {n}')
    # module-level declarations (outside procedures)
    inproc = set()
    for p in ps: inproc.update(range(p['start'], p['end'] + 1))
    modvars = set()
    for i, l in enumerate(text.split('\n')):
        if i in inproc: continue
        m = re.match(r'^\s*(?:Dim|Private|Public|Const)\s+(.*)$', l)
        if m:
            for part in re.split(r',(?![^(]*\))', m.group(1)):
                v = re.match(r'\s*(?:Const\s+)?(\w+)', part)
                if v: modvars.add(v.group(1))
    known = modvars | set(names)
    for p in ps:
        local = set()
        for part in p['params'].split(','):
            v = re.match(r'\s*(?:Optional\s+)?(?:ByVal\s+|ByRef\s+)?(\w+)', part)
            if v: local.add(v.group(1))
        for l in p['body']:
            code = l.split("'")[0] if '"' not in l else re.sub(r'"[^"]*"', '""', l).split("'")[0]
            for m in re.finditer(r'\b(?:Dim|Static|ReDim(?:\s+Preserve)?)\s+(.*)$', code):
                for part in re.split(r',(?![^(]*\))', m.group(1)):
                    v = re.match(r'\s*(\w+)', part)
                    if v: local.add(v.group(1))
        for l in p['body']:
            code = re.sub(r'"[^"]*"', '""', l).split("'")[0]
            for stmt in code.split(':'):
                m = re.match(r'^\s*(?:Set\s+)?(\w+)(?:\([^)]*\))?\s*=', stmt)
                if m:
                    v = m.group(1)
                    if v not in local and v not in known and v not in KEYWORDS and v != p['name']:
                        errs.append(f'{p["name"]}: assignment to undeclared {v}')
                m = re.match(r'^\s*For\s+(\w+)\s*=', stmt)
                if m and m.group(1) not in local and m.group(1) not in known:
                    errs.append(f'{p["name"]}: loop variable {m.group(1)} undeclared')
            m = re.match(r'^\s*Call\s+(\w+)', code)
            if m and m.group(1) not in names: errs.append(f'{p["name"]}: Call to missing {m.group(1)}')
            m = re.match(r'^\s*(\w+)\s+(?!=)[^=(]', code)
            if m and m.group(1) in ('Progress', 'Trace', 'Check') and m.group(1) not in names: errs.append(f'{p["name"]}: {m.group(1)} missing')
    # every called helper that looks like a statement call must exist
    for m in re.finditer(r'^\s*(Progress|Trace|Check|LoadLeg|DrawProfile|DrawProfileU)\b', text, re.M):
        if m.group(1) not in names: errs.append(f'missing procedure {m.group(1)}')
    # VBA refuses to compile a statement with more than 24 line continuations (2026-09-25: 6504 / 6565)
    run = 0
    for i, l in enumerate(text.split('\n')):
        run = run + 1 if l.rstrip().endswith(' _') else 0
        if run == 25: errs.append(f'more than 24 line continuations in one statement (line {i + 1})')
    bal = text.count('\nSub ') + text.count('\nFunction ') + text.count('\nPrivate Sub ') + text.count('\nPrivate Function ')
    ends = len(re.findall(r'^\s*End (Sub|Function)\s*$', text, re.M))
    if bal != ends: errs.append(f'Sub/Function count {bal} vs End {ends}')
    return sorted(set(errs)), len(ps)


if __name__ == '__main__':
    bad = 0
    for f in sys.argv[1:]:
        e, n = check(open(f, encoding='latin-1', newline='').read())
        print(f, n, 'procedures', 'OK' if not e else e[:8])
        bad += bool(e)
    sys.exit(1 if bad else 0)
