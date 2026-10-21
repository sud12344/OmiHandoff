"""cmp_out.py A B: compare two gen_bent output folders - .bas byte for byte (the header 'generated <date>' line ignored), SW2 tables
cell for cell, summary json by key. Prints one line per file."""
import os, sys, json, difflib, openpyxl


def sw2(p):
    return [list(r) for r in openpyxl.load_workbook(p).active.iter_rows(values_only=True)]


def main(a, b):
    names = sorted(set(os.listdir(a)) | set(os.listdir(b)))
    same = True
    for n in names:
        pa, pb = os.path.join(a, n), os.path.join(b, n)
        if not (os.path.exists(pa) and os.path.exists(pb)):
            print(f'{n}: only in {"A" if os.path.exists(pa) else "B"}'); same = False; continue
        if n.endswith('.xlsx'):
            ok = sw2(pa) == sw2(pb)
        elif n.endswith('.json'):
            ok = json.load(open(pa)) == json.load(open(pb))
        else:
            la = [l for l in open(pa).read().split('\n') if 'generated ' not in l]
            lb = [l for l in open(pb).read().split('\n') if 'generated ' not in l]
            ok = la == lb
            if not ok:
                d = list(difflib.unified_diff(la, lb, lineterm='', n=0))
                print(f'{n}: DIFFER ({sum(1 for x in d if x[:1] in "+-") - 2} changed lines)')
                for x in d[:30]:
                    print('   ', x[:220])
                same = False
                continue
        print(f'{n}: {"identical" if ok else "DIFFER"}')
        same &= ok
    return same


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
