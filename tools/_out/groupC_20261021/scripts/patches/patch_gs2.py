"""patch_gs2.py: the GROUP C hooks in gen_straight2.py build_rows / emit (each an inserted block; the only edited existing line is none)"""
import sys
p = sys.argv[1]; s = open(p).read()
def ins_before(anchor, text, count=1):
    global s
    assert s.count(anchor) == count, (anchor[:60], s.count(anchor))
    i = s.index(anchor); s = s[:i] + text + s[i:]
def ins_after(anchor, text):
    global s
    assert s.count(anchor) == 1, (anchor[:60], s.count(anchor))
    i = s.index(anchor) + len(anchor); s = s[:i] + text + s[i:]
def ins_after_line(prefix, text):
    """after the one line that starts with prefix (the rest of the line may differ between the tools_af and the live toolsets)"""
    global s
    lines = s.splitlines(True); hit = [k for k, l in enumerate(lines) if l.startswith(prefix)]
    assert len(hit) == 1, (prefix[:60], len(hit))
    lines.insert(hit[0] + 1, text); s = ''.join(lines)

# 1. thread-major check of a bite end
ins_before("            if E_['kind'] not in ('JICM', 'JICSW', 'JICF', 'ORBM'",     # 2026-10-21: prefix only - the live (batch 20) line also lists 'NWO
"""            if E_['kind'] == 'BITEM':     # GROUP C (compression): the bite end's thread = the BITE library major of its dash
                if r.get(col_) is None or abs(r[col_] - E_['e']['TM']) > 1e-3: chk0.append(f'{col_} {r.get(col_)} does not match the End {sfx_} -{d_:02d} BITEM thread ({E_["e"]["TM"]})')
                continue
""")
# 2. bite end / compression nut checks
ins_after_line("        chk = list(chk0); warn = ",     # tools_af: warn = []; live (batch 20): warn = list(warn0)

"""        if sp.get('bite'):
            # GROUP C (compression): tube socket / bore / neck / hex gates of every bite end; the row's Brennan bite cells = the BITE library
            mode_, cA_, cB_ = sp['bore']
            for E_, c_ in ((EA, cA_), (EB, cB_ if mode_ == 'mid' else cA_)):
                if E_['kind'] != 'BITEM': continue
                c2_, w2_ = bite_checks(E_, r.get(c_) if isinstance(c_, str) else None, rB, hexb); chk += c2_; warn += w2_
            chk += bite_rowcheck(r, EA, None) if EA['kind'] == 'BITEM' else []
        if sp.get('cnut'):
            # GROUP C (C0318): thread length / cone start / wall checks of the compression nut
            if not (EA['cs'] + 0.02 < EA['F'] <= EB['E'] + 1e-9): chk.append(f'thread length F {EA["F"]} not between the countersink depth {EA["cs"]:.4f} and the cone start E {EB["E"]}')
            if hexb / 2 - EA['e']['TM'] / 2 < 0.03: chk.append(f'wall between the thread major dia {EA["e"]["TM"]} and the hex flats {hexb} only {hexb / 2 - EA["e"]["TM"] / 2:.4f}')
            if abs(EB['rmin'] - EA['rmin']) > 1e-9: chk.append('End A / End B thread minor differ')
""")
# 3. compression nut bore
ins_before("        elif mode == 'nut_thru':\n            # 2026-10-02 (0306 locknut)",
"""        elif mode == 'cnut_thru':
            # GROUP C (C0318): the thread-minor bore from the End A face to the cone start E removes the DRIVE construction core (the cavity of End B
            # starts with the 45deg cone at the minor there)
            cols['DA@BORE_A'] = round(2 * EA['rmin'], 5); cols['DEPTH@BORECUT_A'] = EB['E']
""")
# 4. emit: DRIVE dimensions of a bite end
ins_before("        elif k == 'HOSEB':\n            dr(g(s['s1'])",
"""        elif k == 'BITEM':
            # GROUP C (compression): tip face -> thread major (THDZ) -> 45deg ramp -> relief neck (NECKR x NECKL) -> hex face
            dr(g(s['thd']), f'THDMAJR_{sfx}', E['rM'], mid(g(s['thd'])), -0.3)
            dl(g(s['thd']), f'BITE{sfx}_THDZ', E['TZ'], mid(g(s['thd'])), rB + 0.35)
            da(g(s['ramp']), g(s['thd']), f'BITE{sfx}_RAMPANG', BITE_RAMPANG, V[g(s['ramp'])][0] + 0.1 * side, rB + 0.1)
            dr(g(s['neck']), f'BITE{sfx}_NECKR', E['rN'], mid(g(s['neck'])), -0.2)
            dl(g(s['neck']), f'BITE{sfx}_NECKL', E['e']['NL'], mid(g(s['neck'])), rB + 0.15)
""")
# 5. emit: compression nut End B cavity
ins_before("""        else:
            m = E['m']
            dp(k + 1, 'False', axis, f'JICF{sfx}_CSR', m['RCS'], L + 0.1, m['RCS'] / 2)""",
"""        elif E['kind'] == 'CNUTB':
            # GROUP C (C0318 End B): face -> tube hole (k+1) -> 45deg cone up to the minor (k+2) -> flat construction core end (k+3, vertical) -> axis
            dr(k + 1, f'CNUT{sfx}_HOLER', E['rD'], mid(k + 1), -0.3)
            dl(k + 1, f'CNUT{sfx}_HOLEL', E['xs'], mid(k + 1), rB + 0.3)
            da(k + 2, axis, f'CNUT{sfx}_CONEANG', 45, mid(k + 2), E['rmin'] + 0.1)
            dp(k + 2, 'True', axis, f'CNUT{sfx}_MINR', E['rmin'], E['E'] - 0.05, E['rmin'] / 2)
            assert k + 4 == axis, (k, axis)
""")
# 6. emit: tube socket pockets (before the bores)
ins_before("    if EB.get('socket'):\n        # 2026-10-02 (PLUGS): internal hex socket",
"""    for E, sfx, fromB, fr in ((EA, 'A', 'False', fA), (EB, 'B', 'True', fB)):
        if E['kind'] == 'BITEM':     # GROUP C (compression): the tube socket at the bite tip (the tube stop), cut from the tip face
            F.append(f'    Call BoreCut("POCKET_{sfx}", "SOCKDIA", {E["td"]*IN:.9f}, {cols[f"DEPTH@POCKETCUT_{sfx}"]*IN:.9f}, 0#, "POCKETCUT_{sfx}", {fromB}, {fr*IN:.9f})')
    if mode == 'cnut_thru':     # GROUP C (C0318): thread-minor bore from the End A face to the cone start (removes the construction core)
        F.append(f'    Call BoreCut("BORE_A", "DA", {cols["DA@BORE_A"]*IN:.9f}, {cols["DEPTH@BORECUT_A"]*IN:.9f}, 0#, "BORECUT_A", False, {fA*IN:.9f})')
""")
# 7. emit: open-axis checks
ins_before("    # threads\n    T = []\n",
"""    for E, sfx in ((EA, 'A'), (EB, 'B')):
        if E['kind'] == 'BITEM':     # GROUP C: tube socket open, bore runs on through its bottom
            xk_ = cols[f'DEPTH@POCKETCUT_{sfx}'] if sfx == 'A' else L - cols[f'DEPTH@POCKETCUT_{sfx}']
            OPEN.append(f'    Check "End {sfx} tube socket bottom open to the bore (x={xk_:.4f})", Not AxisCovered({xk_*IN:.9f})')
    if mode == 'cnut_thru':
        OPEN.append(f'    Check "construction core removed (no face across the axis at x={EB["E"] - 0.01:.4f} / {EB["E"] + 0.01:.4f})", Not AxisCovered({(EB["E"] - 0.01)*IN:.9f}) And Not AxisCovered({(EB["E"] + 0.01)*IN:.9f})')
""")
open(p, 'w').write(s)
print('patched', p)
