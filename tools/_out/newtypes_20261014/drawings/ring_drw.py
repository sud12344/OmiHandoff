# ring_drw.py (2026-10-15): dimension-check drawing of ONE O-ring configuration (gen_ring.py ORING master).  Runs inside the
# SolidWorks MCP run_python namespace after exec(geo3.py) + exec(drw3.py) of tools\_out\drawings_20261008\scripts (helpers:
# arr, mpt, place, shift, outline, add_dia, add_note, fill_sheet_format, textw, set_places, dval, LOG, constants).
#
# The ring's face is split along its silhouettes (SPLIT_AXIAL / SPLIT_SIDE in the master), so the I.D. / O.D. are real circular
# model edges at x = 0 and the cross-section W is a real circle in the Front Plane - every dimension is a reference dimension
# on a model edge, as on the 62 fitting drawings.  Views: FRONT (ring edge-on, W circle), RIGHT (along the ring axis: I.D. and
# O.D.), ISOMETRIC.  Title block material = the row's $PRP@Material (not carbon steel).
import math, os, time
from fractions import Fraction


def ring_edges(body):
    """the I.D. / O.D. circles (axis X, centre x = 0) and the upper cross-section circle (axis Z, centre y > 0)"""
    ax, sec = [], []
    for e in body.GetEdges() or []:
        e = W(e, 'IEdge')
        c = W(e.GetCurve(), 'ICurve')
        if not c.IsCircle():
            continue
        p = list(c.CircleParams)
        cen, n, r = p[0:3], p[3:6], p[6]
        if abs(abs(n[0]) - 1) < 1e-6 and abs(cen[0]) < 1e-7:
            ax.append((r, e))
        elif abs(abs(n[2]) - 1) < 1e-6 and cen[1] > 0:
            sec.append((r, e, cen))
    ax.sort(key=lambda t: t[0])
    if len(ax) < 2 or not sec:
        raise RuntimeError(f'split-line edges not found (axial circles {len(ax)}, section circles {len(sec)}) - master without SPLIT_*?')
    return dict(id=ax[0], od=ax[-1], w=sec[0])


def all_edges(body):
    return [W(e, 'IEdge') for e in (body.GetEdges() or [])]


def hide_edges(dr, dd, view, edges):
    """hide model edges in one drawing view (the split-line edges a view does not need); returns how many were selected"""
    W(dd, 'IDrawingDoc').ActivateView(view.Name)
    dr.ClearSelection2(True)
    n = 0
    for e in edges:
        if view.SelectEntity(e, n > 0):
            n += 1
    if n:
        dd.HideEdge()
    dr.ClearSelection2(True)
    return n


def make_ring_drawing(part_path, cfg, out_dir, title, row, material, notes_extra=None):
    global MATERIAL
    LOG.clear()
    t0 = time.time()
    r = sw.OpenDoc6(part_path, 1, 3, cfg, 0, 0)
    part = W(r[0] if isinstance(r, tuple) else r, 'IModelDoc2')
    part.ShowConfiguration2(cfg)
    if W(part.GetActiveConfiguration(), 'IConfiguration').Name != cfg:
        raise RuntimeError(f'configuration {cfg} not active')
    body = W(W(part, 'IPartDoc').GetBodies2(C.swSolidBody, True)[0], 'IBody2')
    E = ring_edges(body)
    idr, odr, wr = E['id'][0], E['od'][0], E['w'][0]
    od, w = 2 * odr, 2 * wr
    for s in (4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 0.375, 0.25):
        if od * s <= 4.4 * IN:
            break
    fr = Fraction(s).limit_denominator(8); num, den = fr.numerator, fr.denominator
    dr = W(sw.NewDocument(TEMPLATE, C.swDwgPaperBsize, SHW, SHH), 'IModelDoc2')
    dd = W(dr, 'IDrawingDoc')
    dd.SetupSheet5('Sheet1', C.swDwgPaperBsize, C.swDwgTemplateCustom, float(num), float(den), False, FORMAT, SHW, SHH, 'Default', True)
    ext = W(dr.Extension, 'IModelDocExtension')
    ext.SetUserPreferenceInteger(C.swUnitSystem, 0, C.swUnitSystem_IPS)
    ext.SetUserPreferenceInteger(C.swUnitsLinearDecimalPlaces, 0, 4)
    ext.SetUserPreferenceInteger(C.swDetailingLinearDimPrecision, 0, 4)
    for pref, opt, val in ((C.swDetailingDimTrailingZero, 0, C.swDimShowTrailingZeroes),
                           (C.swDetailingDimensionTextAndLeaderStyle, 0, C.swSolidLeaderHorizontalText),
                           (C.swDetailingDimensionTextAndLeaderStyle, C.swDetailingDiameterDimension, C.swSolidLeaderHorizontalText)):
        try:
            ext.SetUserPreferenceInteger(pref, opt, val)
        except Exception as ex_:
            log(f'  doc pref {pref}/{opt}: {ex_}')
    for t in (C.swDisplayCurves, C.swDisplaySketches, C.swDisplayAxes, C.swDisplayPlanes, C.swDisplayOrigins,
              C.swDisplayReferencePoints, C.swDisplayTemporaryAxes):
        try:
            ext.SetUserPreferenceToggle(t, 0, False)
        except Exception as ex_:
            log(f'  toggle {t}: {ex_}')
    try:
        ext.SetUserPreferenceToggle(C.swDetailingDimANSIBentLeader, 0, True)
    except Exception as ex_:
        log(f'  bent leader: {ex_}')

    def mkview(vname, mode, tangent):
        v = W(dd.CreateDrawViewFromModelView3(part_path, vname, 8.3 * IN, 6 * IN, 0), 'IView')
        v.ReferencedConfiguration = cfg
        v.UseSheetScale = True
        v.SetDisplayMode3(False, mode, False, True)        # (use parent, mode, facetted, edges shown)
        try:
            v.SetDisplayTangentEdges2(tangent)
        except Exception as ex_:
            log(f'  tangent edges {vname}: {ex_}')
        return v

    # the split edges are tangent edges (between smooth faces): visible in the views that dimension them, phantom elsewhere
    vf = mkview('*Front', C.swHIDDEN, C.swTangentEdgesVisible)
    vr = mkview('*Right', C.swHIDDEN, C.swTangentEdgesVisible)
    vi = mkview('*Isometric', C.swSHADED, C.swTangentEdgesHidden)       # shaded with edges
    dr.ForceRebuild3(False)
    W(dd.GetCurrentSheet(), 'ISheet').SetScale(float(num), float(den), True, False)
    dr.ForceRebuild3(False)
    y1 = (YMAX + YMIN) / 2 + 0.6
    place(vf, COLS[1], y1); place(vr, COLS[2], y1); place(vi, COLS[0], y1)
    dr.ForceRebuild3(False)
    o_f = mpt(vf, (0, 0, 0)); o_r = mpt(vr, (0, 0, 0))
    shift(vr, 0, o_f[1] - o_r[1])                     # projection: RIGHT view level with the FRONT view (ring centre)
    dr.ForceRebuild3(False)
    # the split lines exist only to give the drawings real edges: RIGHT view keeps only the I.D. / O.D. circles (the pitch
    # circles and the edge-on section circles would read as a third diameter / ticks); FRONT view drops the I.D. / O.D.
    # circles seen edge-on (a line through the middle of the ring)
    keep_r = {id(E['id'][1]), id(E['od'][1])}
    ax_x0 = []
    for e in all_edges(body):
        c = W(e.GetCurve(), 'ICurve')
        if c.IsCircle():
            p = list(c.CircleParams)
            if abs(abs(p[3]) - 1) < 1e-6 and abs(p[0]) < 1e-7:
                ax_x0.append(e)
    ids_keep = [E['id'][1], E['od'][1]]
    hide_r = [e for e in all_edges(body) if not any(e.IsSame(k) if hasattr(e, 'IsSame') else False for k in ids_keep)]
    log(f'hidden in RIGHT view: {hide_edges(dr, dd, vr, [e for e in hide_r if not any(sw.IsSame(e, k) == 0 for k in ids_keep)])}')
    log(f'hidden in FRONT view: {hide_edges(dr, dd, vf, ax_x0)}')
    dr.ForceRebuild3(False)
    dims = []
    # RIGHT view (along the ring axis): O.D. leader up-right, I.D. leader down-left - both just outside the view box
    olr = outline(vr); cr = mpt(vr, (0, 0, 0))
    half = (olr[2] - olr[0]) / 2
    for key, ang, lab in (('od', 45.0, 'O.D.'), ('id', 225.0, 'I.D.')):
        rr, edge = E[key][0], E[key][1]
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        at = (cr[0] + (half + 0.45 * IN) * ca, cr[1] + (half + 0.45 * IN) * sa)
        txt = f'{2 * rr / IN:.3f}'
        d = add_dia(dr, vr, edge, at, textw(txt) + 0.4 * IN, left=ca < 0)
        dtext(d, suffix=f' {lab}')
        dims.append(dict(label=lab, view='RIGHT VIEW', value=None if d is None else round(dval(d), 4), model=round(2 * rr / IN, 4)))
    # FRONT view (ring edge-on): the upper cross-section circle = W
    olf = outline(vf); cc = mpt(vf, E['w'][2])
    at = (olf[2] + 0.55 * IN, cc[1] + 0.35 * IN)
    d = add_dia(dr, vf, E['w'][1], at, textw('0.087') + 0.6 * IN)
    dtext(d, suffix=' W (SECTION)')
    dims.append(dict(label='W', view='FRONT VIEW', value=None if d is None else round(dval(d), 4), model=round(w / IN, 4)))
    # title block (material from the row), view labels, notes
    MATERIAL = material
    log(f'sheet format fields: {fill_sheet_format(dd, title, cfg)}')
    for v, txt in ((vf, 'FRONT VIEW'), (vr, 'RIGHT VIEW'), (vi, 'ISOMETRIC VIEW')):
        ol = outline(v)
        add_note(dr, dd, txt, (ol[0] + ol[2]) / 2, ol[1] - 0.62 * IN, center=True)
    lines = [f'{cfg}  {title}',
             'ALL DIMENSIONS ARE REFERENCE VALUES IN INCHES MEASURED ON THE 3D MODEL (NOMINAL SIZES).',
             'VALUES CARRY THE DECIMALS OF THE SOURCE DATA.  W = CROSS-SECTION DIAMETER OF THE RING.']
    lines += notes_extra or []
    lines.append(f'3D MODEL: {os.path.basename(part_path)[:-7]}, CONFIGURATION {cfg}.  SCALE {num:g}:{den:g}')
    wrapped = []
    for ln in lines:
        while len(ln) > 92:
            cut = ln.rfind(' ', 0, 92)
            cut = cut if cut > 40 else 92
            wrapped.append(ln[:cut].rstrip()); ln = '   ' + ln[cut:].lstrip()
        wrapped.append(ln)
    add_note(dr, dd, '\n'.join(wrapped), 0.6 * IN, 2.42 * IN, height=9)
    dr.ClearSelection2(True)
    dr.ForceRebuild3(False)
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, cfg)
    r1 = dr.Extension.SaveAs(base + '.SLDDRW', 0, 1, None, 0, 0)
    r2 = dr.Extension.SaveAs(base + '.PDF', 0, 1, None, 0, 0)
    res = dict(cfg=cfg, scale=f'{num:g}:{den:g}', dims=dims, log=list(LOG), pdf=base + '.PDF',
               saved=[r1 if not isinstance(r1, tuple) else r1[0], r2 if not isinstance(r2, tuple) else r2[0]],
               drawing_title=dr.GetTitle(), part_title=part.GetTitle(), seconds=round(time.time() - t0, 1))
    MATERIAL = 'CARBON STEEL'
    return res
