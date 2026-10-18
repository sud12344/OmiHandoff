"""w2_runner.py <tools_dir> <json {root: [base_spec_root, overrides]}> - runs gen_tee's __main__ for injected SPEC entries (TEST harness,
copied from wave2_impl_20261009/scripts/gen_test_runner.py; it changes no file of the tools: the SPEC is patched in memory only)."""
import sys, os, json
sys.path.insert(0, os.path.join(sys.argv[1], 'generators')); sys.path.insert(0, sys.argv[1])
import gen_tee as T
inj = json.loads(sys.argv[2])
for root, (base, extra) in inj.items():
    sp = dict(T.SPEC.get(base) or T.SPEC_WAITING[base])
    if 'legs' in extra:
        extra = dict(extra, legs=[tuple(l) for l in extra['legs']])
    sp.update(extra); T.SPEC[root] = sp
src = open(T.__file__, encoding='utf-8').read()
main = src[src.index("if __name__ == '__main__':"):].split('\n', 1)[1]
main = '\n'.join(l[4:] for l in main.split('\n'))
sys.argv = ['gen_tee.py'] + list(inj)
exec(compile(main, 'gen_tee.__main__', 'exec'), T.__dict__)
