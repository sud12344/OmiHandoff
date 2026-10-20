"""run_groups.py g5 g6 ...: waits for out_g4.txt to finish (its closing sw_status), then runs each calls_<g>.json through sw_mcp/call.py
into out_<g>.txt - but first checks memory and STOPS (prints why) if SLDWORKS.exe private memory > 8 GB or free virtual memory < 6 GB
(CLAUDE.md: restart SolidWorks every ~40 builds; the user restarts it from 3DEXPERIENCE)."""
import os, subprocess, sys, time

H = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
B17 = os.path.join(H, r'tools\_out\batch17_20261019')


def finished(p):
    if not os.path.exists(p):
        return False
    s = open(p, encoding='utf-8', errors='replace').read()
    return s.count('=== sw_status') >= 2 and s.rstrip().endswith('s')


def mem():
    ps = ("$p=Get-Process SLDWORKS -ErrorAction SilentlyContinue | Select-Object -First 1; $o=Get-CimInstance Win32_OperatingSystem; "
          "'{0} {1}' -f ($(if ($p) {$p.PrivateMemorySize64/1GB} else {-1})), ($o.FreeVirtualMemory/1MB)")
    out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True).stdout.split()
    return float(out[0]), float(out[1])


while not finished(os.path.join(B17, '' + (os.environ.get('AFTER') or 'out_g4.txt'))):
    time.sleep(30)
for g in sys.argv[1:]:
    sw, free = mem()
    print(f'{time.strftime("%H:%M")} before {g}: SLDWORKS {sw:.1f} GB, free virtual {free:.1f} GB', flush=True)
    if sw < 0 or sw > 8 or free < 6:
        print(f'STOP before {g}: ' + ('SolidWorks not running' if sw < 0 else 'memory'), flush=True)
        break
    with open(os.path.join(B17, f'out_{g}.txt'), 'w', encoding='utf-8') as fh:
        subprocess.run([sys.executable, '-u', os.path.join(H, 'sw_mcp', 'call.py'), '@' + os.path.join(B17, f'calls_{g}.json')],
                       stdout=fh, stderr=subprocess.STDOUT, cwd=H)
    print(f'{time.strftime("%H:%M")} {g} done', flush=True)
    if 'SolidWorks is not running' in open(os.path.join(B17, f'out_{g}.txt'), encoding='utf-8', errors='replace').read():
        print(f'STOP after {g}: SolidWorks went down during it (2026-10-19 23:16 lesson)', flush=True)
        break
