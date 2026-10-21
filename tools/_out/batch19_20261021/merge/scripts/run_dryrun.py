"""run_dryrun.py g1 [g2 g3] (on the PC, SolidWorks running and signed in): runs dryrun/calls_<g>.json through sw_mcp/call.py into
dryrun/out_<g>.txt, one group after the other; before each group it checks memory and STOPS (prints why) if SLDWORKS.exe private memory
> 8 GB or free virtual memory < 6 GB - then restart SolidWorks from 3DEXPERIENCE and run the remaining groups."""
import os, subprocess, sys, time
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
D = os.path.join(H, 'tools', '_out', 'batch19_20261021', 'merge', 'dryrun')


def mem():
    ps = ("$p=Get-Process SLDWORKS -ErrorAction SilentlyContinue | Select-Object -First 1; $o=Get-CimInstance Win32_OperatingSystem; "
          "'{0} {1}' -f ($(if ($p) {$p.PrivateMemorySize64/1GB} else {-1})), ($o.FreeVirtualMemory/1MB)")
    out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True).stdout.split()
    return float(out[0]), float(out[1])


for g in sys.argv[1:]:
    sw, free = mem()
    print(f'{time.strftime("%H:%M")} before {g}: SLDWORKS {sw:.1f} GB, free virtual {free:.1f} GB', flush=True)
    if sw < 0 or sw > 8 or free < 6:
        print(f'STOP before {g}: ' + ('SolidWorks not running' if sw < 0 else 'memory - restart SolidWorks, then run the rest'), flush=True)
        break
    with open(os.path.join(D, f'out_{g}.txt'), 'w', encoding='utf-8') as f:
        subprocess.run([sys.executable, os.path.join(H, 'sw_mcp', 'call.py'), '@' + os.path.join(D, f'calls_{g}.json')], stdout=f,
                       stderr=subprocess.STDOUT, cwd=H)
    print(f'{time.strftime("%H:%M")} {g} done -> out_{g}.txt', flush=True)
