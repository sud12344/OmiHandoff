# Progress lines for the OMi build macros (2026-09-24, after the "5406 looks stuck" report).
import re
# The all-config sweep rebuilds every configuration with the helical threads live and wrote nothing until it finished;
# VBA also writes the report in 512-byte blocks, so the file on disk lagged behind. This adds:
#   - Sub Progress: writes the line, closes + reopens the report (so the line reaches the disk at once),
#     puts the line in the SolidWorks status bar and lets Windows repaint (DoEvents)
#   - one Progress line per configuration in the sweep (n/N, name, seconds) and one per spot-check configuration
# Geometry, checks and dimensions are untouched.

SWEEP_OLD = '''    sw_bad = 0: sw_n = 0
    For sw_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(sw_i) <> "Default" Then
            swModel.ShowConfiguration2 sw_names(sw_i)
            swModel.ForceRebuild3 False
            sw_n = sw_n + 1
'''
SWEEP_NEW = '''    sw_bad = 0: sw_n = 0
    Dim sw_t0 As Single, sw_tot As Long
    sw_tot = 0
    For sw_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(sw_i) <> "Default" Then sw_tot = sw_tot + 1
    Next sw_i
    Progress "All-config sweep: rebuilding " & sw_tot & " configurations one at a time with the threads live. SolidWorks does not redraw until it is done - one line per configuration follows."
    For sw_i = LBound(sw_names) To UBound(sw_names)
        If sw_names(sw_i) <> "Default" Then
            sw_t0 = Timer
            swModel.ShowConfiguration2 sw_names(sw_i)
            swModel.ForceRebuild3 False
            sw_n = sw_n + 1
            Progress "sweep " & sw_n & "/" & sw_tot & "  " & sw_names(sw_i) & "  rebuilt in " & Format(Timer - sw_t0, "0.0") & " s"
'''
CX_OLD = ('''    For cx_q = 0 To {n}
        swModel.ShowConfiguration2 cx_c(cx_q)
''')
CX_NEW = ('''    For cx_q = 0 To {n}
        Progress "config check " & (cx_q + 1) & ": " & cx_c(cx_q)
        swModel.ShowConfiguration2 cx_c(cx_q)
''')
TRACE_OLD = '''Sub Trace(what As String)
    Debug.Print "      " & what
    On Error Resume Next
    Print #fnRep, "      " & what
End Sub
'''
TRACE_NEW = TRACE_OLD + '''Sub Progress(what As String)
    ' progress line: written to the report at once (close + reopen - VBA otherwise writes the file in 512-byte blocks),
    ' shown in the SolidWorks status bar, and Windows gets a chance to repaint (do not click in SolidWorks meanwhile)
    Trace what
    On Error Resume Next
    Close #fnRep
    Open REPORT_PATH For Append As #fnRep
    Dim fr As Object
    Set fr = swApp.Frame
    fr.SetStatusBarText "OMi build: " & what
    DoEvents
End Sub
'''
MARK = 'Sub Progress(what As String)'


def add_progress(s):
    """Return the macro text with progress lines. Idempotent; raises if a block is not found exactly once."""
    if MARK in s:
        return s
    nl = '\r\n' if '\r\n' in s else '\n'
    t = s.replace('\r\n', '\n')
    assert t.count(SWEEP_OLD) == 1, ('sweep block', t.count(SWEEP_OLD))
    t = t.replace(SWEEP_OLD, SWEEP_NEW)
    ncx = 0
    for n in ('0', '1', '2', '3'):
        o = CX_OLD.format(n=n)
        if o in t:
            assert t.count(o) == 1
            t = t.replace(o, CX_NEW.format(n=n)); ncx += 1
    assert ncx == 1, ('config-check loop', ncx)
    assert t.count(TRACE_OLD) == 1, ('Trace sub', t.count(TRACE_OLD))
    t = t.replace(TRACE_OLD, TRACE_NEW)
    assert t.count(MARK) == 1 and t.count('Progress "sweep ') == 1 and t.count('Progress "config check') == 1
    return t.replace('\n', nl)


# 2026-09-25: leave the master in its REFERENCE configuration at the save. SolidWorks opens a part in the configuration that was
# active when it was saved; after the all-config sweep the macros showed the first name in the list = the smallest size (e.g. the
# 5504 master opened as 5504-02-02-FG, where the 0.26 collar dominates the short leg). The reference configuration is the size the
# macro builds first and the one compared with the Brennan STEPs. Geometry, checks and dimensions are untouched.
POSTSWEEP_OLD = '    swModel.ShowConfiguration2 sw_names(LBound(sw_names) + IIf(sw_names(LBound(sw_names)) = "Default", 1, 0))\n'
REFMARK = "leave the master in its reference configuration"
_PRESWEEP = re.compile(r'\n    swModel\.ShowConfiguration2 "([^"]+)"\n    swModel\.ForceRebuild3 False\n\n    \' ---- all-config rebuild sweep')


def ref_config_at_save(s):
    """Return the macro text that re-activates the reference configuration after the sweep. Idempotent; raises when a block is not found exactly once."""
    if REFMARK in s:
        return s
    nl = '\r\n' if '\r\n' in s else '\n'
    t = s.replace('\r\n', '\n')
    assert t.count(POSTSWEEP_OLD) == 1, ('post-sweep line', t.count(POSTSWEEP_OLD))
    refs = _PRESWEEP.findall(t)
    assert len(refs) == 1, ('pre-sweep reference configuration', refs)
    ref = refs[0]
    new = (f"    ' 2026-09-25: {REFMARK} ({ref}) - SolidWorks opens a part in the configuration that is active when it is saved;\n"
           f"    ' before this the master was left in the first name of the list (the smallest size)\n"
           f'    swModel.ShowConfiguration2 "{ref}"\n'
           f'    Trace "Master left in its reference configuration {ref} for the save (it opens in this size)"\n')
    t = t.replace(POSTSWEEP_OLD, new)
    assert t.count(REFMARK) == 1
    return t.replace('\n', nl)
