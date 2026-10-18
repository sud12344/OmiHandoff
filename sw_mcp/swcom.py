"""COM layer for the SolidWorks MCP server.

Everything here must run on the single COM thread (server.com()). The SolidWorks API
works in metres and radians; tools convert at the edges (inches by default).
Early binding comes from makepy wrappers of sldworks.tlb / swconst.tlb, generated into
%TEMP%\\gen_py on first use - without them pywin32 cannot tell methods from properties.
"""
import ast
import difflib
import fnmatch
import io
import math
import os
import re
import tempfile
import time
import winreg
from collections import Counter

import pywintypes
import win32com.client as wc
from win32com.client import gencache

SW_TLB = "{83A33D31-27C5-11CE-BFD4-00400513BB57}"     # sldworks.tlb
CONST_TLB = "{4687F359-55D0-4CD3-B6CF-2EB42C11F989}"  # swconst.tlb
IN = 0.0254
WORK = os.path.join(tempfile.gettempdir(), "sw_mcp")
os.makedirs(WORK, exist_ok=True)

DOC_TYPES = {1: "part", 2: "assembly", 3: "drawing"}
EXT_TYPES = {".sldprt": 1, ".sldasm": 2, ".slddrw": 3}
FOREIGN = {".step", ".stp", ".igs", ".iges", ".x_t", ".x_b", ".sat", ".stl", ".3mf", ".parasolid"}
VIEWS = {"front": 1, "back": 2, "left": 3, "right": 4, "top": 5, "bottom": 6,
         "isometric": 7, "iso": 7, "trimetric": 8, "dimetric": 9}
MODES = {"shaded_edges": 5, "shaded": 4, "wireframe": 1, "hidden_removed": 2, "hidden_grayed": 3}
SETVALUE_STATUS = {0: "ok", 1: "failure", 2: "invalid value", 3: "driven dimension",
                   4: "model not loaded", 5: "frozen feature owner"}
SYSTEM_FEATURE_TYPES = {"DetailCabinet", "OriginProfileFeature", "MaterialFolder", "EnvFolder",
                        "CommentsFolder", "ConfigCommentsFolder", "FavoriteFolder", "HistoryFolder",
                        "SelectionSetFolder", "SensorFolder", "DocsFolder", "SurfaceBodyFolder",
                        "SolidBodyFolder", "InkMarkupFolder", "EqnFolder", "ConfigTableFolder"}


class SwError(Exception):
    """An expected failure, reported to the caller as a plain message."""


# ---------------------------------------------------------------- type libraries / wrapping
def _latest_typelib(guid):
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, rf"TypeLib\{guid}") as k:
        versions, i = [], 0
        while True:
            try:
                name = winreg.EnumKey(k, i)
            except OSError:
                break
            i += 1
            try:
                major, minor = name.split(".")
                versions.append((int(major, 16), int(minor, 16)))
            except ValueError:
                pass
    if not versions:
        raise SwError(f"type library {guid} is not registered - is SolidWorks installed?")
    return max(versions)


_mod = _const = None


def mods():
    global _mod, _const
    if _mod is None:
        _mod = gencache.EnsureModule(SW_TLB, 0, *_latest_typelib(SW_TLB))
        _const = gencache.EnsureModule(CONST_TLB, 0, *_latest_typelib(CONST_TLB))
    return _mod, _const


def W(obj, iface):
    """Wrap a raw COM object in the early-bound interface class (e.g. 'IModelDoc2')."""
    if obj is None:
        return None
    return getattr(mods()[0], iface)(getattr(obj, "_oleobj_", obj))


def const_name(prefix, value):
    for k, v in vars(mods()[1].constants).items():
        if k.startswith(prefix) and v == value:
            return k[len(prefix):]
    return str(value)


def flag_names(prefix, value):
    if not value:
        return []
    return [k[len(prefix):] for k, v in vars(mods()[1].constants).items()
            if k.startswith(prefix) and v and value & v == v] or [str(value)]


# ---------------------------------------------------------------- units
class Units:
    def __init__(self, units="in"):
        if units not in ("in", "mm"):
            raise SwError("units must be 'in' or 'mm'")
        self.name = units
        self.k = 1 / IN if units == "in" else 1000.0
        self.nd = 5 if units == "in" else 3

    def L(self, m):          # length
        return round(m * self.k, self.nd)

    def A(self, m2):         # area
        return round(m2 * self.k ** 2, self.nd)

    def V(self, m3):         # volume
        return round(m3 * self.k ** 3, self.nd + 1)

    def P(self, pt):         # point / vector of lengths
        return [self.L(x) for x in pt]

    def to_m(self, v):
        return v / self.k


def _dir(v):
    """Unit direction with a canonical sign (first non-zero component positive), rounded."""
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    d = [x / n for x in v]
    for x in d:
        if abs(x) > 1e-9:
            if x < 0:
                d = [-y for y in d]
            break
    return [round(x, 4) + 0.0 for x in d]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# ---------------------------------------------------------------- application / documents
_app = None


def app():
    global _app
    if _app is not None:
        try:
            _app.RevisionNumber()
            return _app
        except pywintypes.com_error:
            _app = None
    try:
        raw = wc.GetActiveObject("SldWorks.Application")
    except pywintypes.com_error:
        raise SwError("SolidWorks is not running - start it (and sign in to 3DEXPERIENCE), then retry.")
    _app = W(raw, "ISldWorks")
    return _app


def open_docs():
    return [W(d, "IModelDoc2") for d in (app().GetDocuments() or [])]


def _stem(name):
    name = os.path.basename(name or "")
    root, ext = os.path.splitext(name)
    return (root if ext.lower() in EXT_TYPES else name).lower()


def get_doc(spec=""):
    """Active doc when spec is empty; otherwise an open doc matched by path, file name or
    title. A path that is not open yet gets opened."""
    sw = app()
    if not spec:
        d = sw.ActiveDoc
        if d is None:
            raise SwError("No active document - open one with open_doc (or pass doc=...).")
        return W(d, "IModelDoc2")
    is_path = "\\" in spec or "/" in spec
    target = os.path.normcase(os.path.abspath(spec)) if is_path else _stem(spec)
    for d in open_docs():
        path = d.GetPathName()
        if is_path and path and os.path.normcase(path) == target:
            return d
        if not is_path and target in (_stem(path), _stem(d.GetTitle())):
            return d
    if is_path:
        return open_doc(spec)
    raise SwError(f"'{spec}' is not open. Open documents: {[d.GetTitle() for d in open_docs()]}")


def activate(doc):
    app().ActivateDoc3(doc.GetTitle(), False, 1, 0)   # 1 = swDontRebuildActiveDoc
    return doc


def open_doc(path, config="", read_only=False):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise SwError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    sw = app()
    if ext in FOREIGN:
        doc, err = sw.LoadFile4(path, "r", None, 0)
        if doc is None:
            raise SwError(f"Import failed for {path}: {flag_names('swFileLoadError_', err)}")
        return activate(W(doc, "IModelDoc2"))
    if ext not in EXT_TYPES:
        raise SwError(f"Unsupported file type '{ext}'")
    options = 1 | (2 if read_only else 0)             # Silent | ReadOnly
    doc, err, warn = sw.OpenDoc6(path, EXT_TYPES[ext], options, config or "", 0, 0)
    if doc is None:
        raise SwError(f"OpenDoc6 failed for {path}: {flag_names('swFileLoadError_', err)}")
    doc = activate(W(doc, "IModelDoc2"))
    if config and active_config(doc) != config:
        use_config(doc, config)
    return doc


def active_config(doc):
    c = doc.GetActiveConfiguration()
    return W(c, "IConfiguration").Name if c is not None else ""


def config_names(doc):
    return list(doc.GetConfigurationNames() or [])


def use_config(doc, config):
    """Activate a configuration (no-op when empty or already active)."""
    if not config or active_config(doc) == config:
        return
    names = config_names(doc)
    if config not in names:
        close = difflib.get_close_matches(config, names, 6, 0.5)
        raise SwError(f"No configuration '{config}' ({len(names)} configs). Close matches: {close}")
    if not doc.ShowConfiguration2(config):
        raise SwError(f"ShowConfiguration2('{config}') failed")


# ---------------------------------------------------------------- features / errors
def iter_features(doc, sub=False):
    f = doc.FirstFeature()
    while f is not None:
        f = W(f, "IFeature")
        yield f
        if sub:
            s = f.GetFirstSubFeature()
            while s is not None:
                s = W(s, "IFeature")
                yield s
                s = s.GetNextSubFeature()
        f = f.GetNextFeature()


def feature_errors(doc):
    out = []
    for f in iter_features(doc):
        code, is_warning = f.GetErrorCode2()
        if code:
            out.append({"feature": f.Name, "type": f.GetTypeName2(),
                        "error": const_name("swFeatureError_", code), "warning": bool(is_warning)})
    return out


def hard_errors(errors):
    return [e for e in errors if not e["warning"]]


def find_features(doc, patterns):
    pats = [patterns] if isinstance(patterns, str) else list(patterns)
    return [f for f in iter_features(doc) if any(fnmatch.fnmatchcase(f.Name, p) for p in pats)]


# ---------------------------------------------------------------- bodies / mass / geometry
def solid_bodies(doc):
    if doc.GetType() != 1:
        return []
    return [W(b, "IBody2") for b in (W(doc, "IPartDoc").GetBodies2(0, False) or [])]


def exact_box(bodies):
    """Tight bounding box from extreme points (GetPartBox/GetBodyBox are loose)."""
    if not bodies:
        return None
    lo, hi = [math.inf] * 3, [-math.inf] * 3
    for b in bodies:
        for axis in range(3):
            for sign in (-1, 1):
                d = [0.0, 0.0, 0.0]
                d[axis] = float(sign)
                ok, x, y, z = b.GetExtremePoint(*d)
                if ok:
                    v = (x, y, z)[axis]
                    lo[axis], hi[axis] = min(lo[axis], v), max(hi[axis], v)
    return lo + hi


def mass_props(doc):
    mp = W(doc.Extension, "IModelDocExtension").CreateMassProperty()
    if mp is None:
        return None
    mp = W(mp, "IMassProperty")
    return {"volume": mp.Volume, "area": mp.SurfaceArea, "mass_kg": mp.Mass,
            "density_kg_m3": mp.Density, "com": list(mp.CenterOfMass)}


def material(doc):
    if doc.GetType() != 1:
        return None
    name, _db = W(doc, "IPartDoc").GetMaterialPropertyName2("", "")
    return name or None


def _is_outer(face, surf, origin, axis, radius):
    """True when a cylinder/cone face points away from its axis (boss), False for a bore.
    Surface normal orientation is not guaranteed, so evaluate it and apply the face sense."""
    ref = min(([1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]), key=lambda v: abs(_dot(v, axis)))
    perp = [axis[1] * ref[2] - axis[2] * ref[1], axis[2] * ref[0] - axis[0] * ref[2], axis[0] * ref[1] - axis[1] * ref[0]]
    n = math.sqrt(_dot(perp, perp))
    perp = [x / n for x in perp]
    normal = surf.EvaluateAtPoint(*[origin[i] + radius * perp[i] for i in range(3)])[:3]
    return (_dot(normal, perp) > 0) != bool(face.FaceInSurfaceSense())


def _axial_range(face, origin, axis):
    """Min/max position along an axis of a face's circular edges and vertices."""
    ts = []
    for e in face.GetEdges() or []:
        e = W(e, "IEdge")
        c = W(e.GetCurve(), "ICurve")
        if c is not None and c.IsCircle():
            p = c.CircleParams[:3]
            ts.append(_dot([p[i] - origin[i] for i in range(3)], axis))
        for v in (e.GetStartVertex(), e.GetEndVertex()):
            if v is not None:
                p = W(v, "IVertex").GetPoint()
                ts.append(_dot([p[i] - origin[i] for i in range(3)], axis))
    return (min(ts), max(ts)) if ts else None


def body_geometry(body, u, max_items=60):
    """Faces grouped into distinct cylinders / cones / planes / tori, in units u."""
    counts = Counter()
    cyl, cone, plane, torus = {}, {}, {}, {}
    for f in body.GetFaces() or []:
        f = W(f, "IFace2")
        s = W(f.GetSurface(), "ISurface")
        area = f.GetArea()
        if s.IsPlane():
            counts["plane"] += 1
            p = s.PlaneParams                      # normal(3), point(3)
            n = _dir(p[:3])
            key = (tuple(n), u.L(_dot(n, p[3:6])))
            e = plane.setdefault(key, {"normal": n, "offset": key[1], "faces": 0, "area": 0.0})
            e["faces"] += 1
            e["area"] += area
        elif s.IsCylinder():
            counts["cylinder"] += 1
            p = s.CylinderParams                   # origin(3), axis(3), radius
            a = _dir(p[3:6])
            o = p[:3]
            foot = [o[i] - _dot(o, a) * a[i] for i in range(3)]   # axis point nearest origin
            inward = not _is_outer(f, s, o, list(p[3:6]), p[6])
            key = (u.L(2 * p[6]), tuple(a), tuple(u.P(foot)), inward)
            e = cyl.setdefault(key, {"dia": key[0], "axis": a, "through": u.P(foot),
                                     "side": "inner" if inward else "outer", "faces": 0, "span": None})
            e["faces"] += 1
            r = _axial_range(f, foot, a)
            if r:
                lo, hi = (u.L(r[0]), u.L(r[1]))
                e["span"] = [lo, hi] if e["span"] is None else [min(lo, e["span"][0]), max(hi, e["span"][1])]
        elif s.IsCone():
            counts["cone"] += 1
            p = s.ConeParams                       # origin(3), axis(3), radius, half angle
            a = _dir(p[3:6])
            inward = not _is_outer(f, s, p[:3], list(p[3:6]), p[6])
            key = (round(math.degrees(p[7]), 3), tuple(a), inward, u.L(2 * p[6]))
            e = cone.setdefault(key, {"half_angle_deg": key[0], "included_deg": round(2 * key[0], 3),
                                      "axis": a, "ref_dia": key[3], "ref_point": u.P(p[:3]),
                                      "side": "inner" if inward else "outer", "faces": 0})
            e["faces"] += 1
        elif s.IsTorus():
            counts["torus"] += 1
            p = s.TorusParams                      # centre(3), axis(3), major r, minor r
            key = (u.L(p[6]), u.L(p[7]), tuple(_dir(p[3:6])))
            e = torus.setdefault(key, {"major_r": key[0], "minor_r": key[1], "axis": list(key[2]), "faces": 0})
            e["faces"] += 1
        elif s.IsSphere():
            counts["sphere"] += 1
        else:
            counts["other (spline/helical)"] += 1

    def top(d, sort_key):
        rows = sorted(d.values(), key=sort_key)
        return rows[:max_items] + ([f"... {len(rows) - max_items} more"] if len(rows) > max_items else [])

    for e in plane.values():
        e["area"] = u.A(e["area"])
    return {"face_counts": dict(counts),
            "cylinders": top(cyl, lambda e: (e["axis"], -e["dia"])),
            "cones": top(cone, lambda e: (e["axis"], e["half_angle_deg"])),
            "planes": top(plane, lambda e: (e["normal"], e["offset"])),
            "tori": top(torus, lambda e: (e["axis"], e["major_r"]))}


def body_faults(body):
    fe = body.Check3
    return W(fe, "IFaultEntity").Count if fe is not None else 0


# ---------------------------------------------------------------- dimensions
def dim_name(dim):
    """'M1@LEG1' - FullName without the trailing '@<doc>.Part'; the form Parameter() takes."""
    parts = dim.FullName.split("@")
    return "@".join(parts[:-1]) if len(parts) > 2 else dim.FullName


def iter_dimensions(doc, feature_pattern="*"):
    """Yield (full_name, IDimension) once per dimension owned by matching features. A sketch's
    dimensions are also listed under the feature that absorbs it, hence the de-duplication."""
    seen = set()
    for f in iter_features(doc):
        dd = f.GetFirstDisplayDimension()
        while dd is not None:
            dd = W(dd, "IDisplayDimension")
            dim = W(dd.GetDimension2(0), "IDimension")
            if dim is not None:
                name = dim_name(dim)
                owner = name.split("@")[1] if "@" in name else f.Name
                if name not in seen and fnmatch.fnmatchcase(owner, feature_pattern):
                    seen.add(name)
                    yield name, dim
            dd = f.GetNextDisplayDimension(dd)


def dim_value(dim):
    return dim.GetSystemValue3(1, None)[0]           # 1 = swThisConfiguration


def get_parameter(doc, name):
    dim = doc.Parameter(name)
    if dim is None:
        raise SwError(f"No dimension '{name}' (use full names like 'D1@DRIVE')")
    return W(dim, "IDimension")


# ---------------------------------------------------------------- images
def save_image(doc, path):
    ext = W(doc.Extension, "IModelDocExtension")
    ok, err, _warn = ext.SaveAs3(path, 0, 1 | 2, None, None, 0, 0)   # Silent | Copy
    if not ok or not os.path.exists(path):
        raise SwError(f"Image export failed ({flag_names('swFileSaveError_', err)})")
    return path


def autocrop(img, pad=0.06):
    """Crop the viewport background away: the model is where the image has edges."""
    from PIL import ImageFilter
    w, h = img.size
    edges = img.convert("L").filter(ImageFilter.FIND_EDGES).crop((4, 4, w - 4, h - 4))
    bb = edges.point(lambda v: 255 if v > 40 else 0).getbbox()
    if not bb:
        return img
    x0, y0, x1, y1 = bb[0] + 4, bb[1] + 4, bb[2] + 4, bb[3] + 4
    px, py = int((x1 - x0) * pad) + 12, int((y1 - y0) * pad) + 12
    return img.crop((max(0, x0 - px), max(0, y0 - py), min(w, x1 + px), min(h, y1 + py)))


def compose(images, labels, width):
    """One image, or a 2-column labelled grid, scaled to `width` pixels wide."""
    from PIL import Image, ImageDraw
    cols = 1 if len(images) == 1 else 2
    rows = math.ceil(len(images) / cols)
    cell_w = width // cols
    cell_h = max(int(cell_w * min(im.height / im.width for im in images)), 1)
    cell_h = min(max(cell_h, int(cell_w * 0.55)), int(cell_w * 1.2))
    sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (im, label) in enumerate(zip(images, labels)):
        im = im.convert("RGB")
        im.thumbnail((cell_w - 8, cell_h - 8))
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        sheet.paste(im, (x + (cell_w - im.width) // 2, y + (cell_h - im.height) // 2))
        if len(images) > 1:
            draw.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline=(200, 200, 200))
        if label:
            draw.text((x + 8, y + 6), label, fill=(20, 20, 120))
    return sheet


def capture(doc, views, mode="shaded_edges", section_plane="", section_offset_m=0.0,
            reverse_section=False, crop=True):
    """Render views of doc; returns list of PIL images."""
    from PIL import Image
    bad = [v for v in views if v.lower() not in VIEWS]
    if bad:
        raise SwError(f"Unknown view(s) {bad}; use {sorted(VIEWS)}")
    if mode not in MODES:
        raise SwError(f"Unknown display mode '{mode}'; use {sorted(MODES)}")
    activate(doc)
    view = W(doc.ActiveView, "IModelView")
    old_mode = view.DisplayMode
    mvm = W(doc.ModelViewManager, "IModelViewManager")
    sectioned = False
    images = []
    try:
        view.DisplayMode = MODES[mode]
        if section_plane:
            plane = W(doc, "IPartDoc").FeatureByName(section_plane) if doc.GetType() == 1 else None
            if plane is None:
                raise SwError(f"No plane feature named '{section_plane}' (e.g. 'Front Plane')")
            svd = W(mvm.CreateSectionViewData(), "ISectionViewData")
            svd.FirstPlane = plane
            svd.FirstOffset = section_offset_m
            svd.FirstReverseDirection = reverse_section
            sectioned = bool(mvm.CreateSectionView(svd))
            if not sectioned:
                raise SwError("CreateSectionView failed")
        for v in views:
            doc.ShowNamedView2("", VIEWS[v.lower()])
            doc.ViewZoomtofit2()
            path = os.path.join(WORK, f"view_{int(time.time() * 1000)}_{v}.png")
            save_image(doc, path)
            with Image.open(path) as im:
                im.load()
                images.append(autocrop(im) if crop else im.copy())
            os.remove(path)
    finally:
        if sectioned:
            mvm.RemoveSectionView()
        view.DisplayMode = old_mode
        doc.GraphicsRedraw2()
    return images


# ---------------------------------------------------------------- macros
def _read_text(path):
    raw = open(path, "rb").read()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


def _vba_literal(v):
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, (int, float)):
        return repr(v)
    return '"' + str(v).replace('"', '""') + '"'


MSGBOX_SHIM = '''

' ---- added by sw_mcp: MsgBox is logged to a file instead of blocking SolidWorks
Private Function MsgBox(Optional ByVal Prompt As Variant, Optional ByVal Buttons As Variant, _
        Optional ByVal Title As Variant, Optional ByVal HelpFile As Variant, Optional ByVal Context As Variant) As Long
    Dim mcpFn As Integer
    mcpFn = FreeFile
    Open "{log}" For Append As #mcpFn
    Print #mcpFn, "MSGBOX: " & CStr(Prompt)
    Close #mcpFn
    MsgBox = 1
End Function
'''


def prepare_macro(path, entry="", const_overrides=None):
    """Turn a .bas/.swb into a runnable .swb in WORK. Returns (swb_path, entry, consts, log)."""
    src = _read_text(path)
    lines = [ln for ln in src.splitlines() if not re.match(r"\s*Attribute\s+VB_", ln)]
    consts = {}
    for name, value in (const_overrides or {}).items():
        pat = re.compile(rf"^(\s*(?:(?:Public|Private|Global)\s+)?Const\s+{re.escape(name)}\b[^=]*=\s*)(.*)$", re.I)
        hits = [i for i, ln in enumerate(lines) if pat.match(ln)]
        if not hits:
            raise SwError(f"Const '{name}' not found in {os.path.basename(path)}")
        for i in hits:
            lines[i] = pat.sub(lambda m: m.group(1) + _vba_literal(value), lines[i])
    for ln in lines:                                 # final values of string consts (for reports)
        m = re.match(r'\s*(?:(?:Public|Private|Global)\s+)?Const\s+(\w+)\s+As\s+String\s*=\s*"((?:[^"]|"")*)"', ln, re.I)
        if m:
            consts[m.group(1)] = m.group(2).replace('""', '"')
    subs = re.findall(r"^\s*(?:Public\s+)?Sub\s+(\w+)\s*\(\s*\)", "\n".join(lines), re.M | re.I)
    if not entry:
        entry = next((s for s in subs if s.lower().startswith("build")), None) \
            or next((s for s in subs if s.lower() == "main"), None) or (subs[0] if subs else "")
    if not entry or entry.lower() not in [s.lower() for s in subs]:
        raise SwError(f"Entry sub '{entry}' not found; parameterless subs: {subs}")
    entry = next(s for s in subs if s.lower() == entry.lower())
    stem = os.path.splitext(os.path.basename(path))[0]
    log = os.path.join(WORK, f"{stem}__msgbox.log")
    text = "\n".join(lines)
    has_own_msgbox = re.search(r"^\s*(?:Public\s+|Private\s+)?(?:Function|Sub)\s+MsgBox\b", text, re.M | re.I)
    body = text + ("" if has_own_msgbox else MSGBOX_SHIM.replace("{log}", log))
    if entry.lower() != "main":
        # SolidWorks always starts a .swb at Sub main (RunMacro2's procedure name is ignored),
        # so move any existing main aside and make main call the entry.
        body = re.sub(r"^(\s*(?:Public\s+|Private\s+)?Sub\s+)main(\s*\()", r"\1mcp_orig_main\2", body, flags=re.M | re.I)
        body += f"\n\n' ---- added by sw_mcp: .swb files always start at main\nSub main()\n    {entry}\nEnd Sub\n"
    out = os.path.join(WORK, f"{stem}__mcp.swb")
    with open(out, "w", encoding="cp1252", errors="replace", newline="\r\n") as fh:
        fh.write(body)
    return out, entry, consts, log


def summarize_report(path, max_fail=40, tail=8):
    if not path or not os.path.exists(path):
        return None
    lines = _read_text(path).splitlines()
    fails = [ln.strip() for ln in lines if ln.startswith("FAIL")]
    return {"path": path, "ok": sum(ln.startswith("OK") for ln in lines), "fail": len(fails),
            "fail_lines": fails[:max_fail], "tail": [ln.rstrip() for ln in lines[-tail:]]}


# ---------------------------------------------------------------- python escape hatch
_py_ns = {}


def run_python(code):
    out = io.StringIO()

    def _print(*a, **k):
        k["file"] = out
        print(*a, **k)

    sw = app()
    active = sw.ActiveDoc
    _py_ns.update(sw=sw, doc=W(active, "IModelDoc2") if active is not None else None, W=W,
                  SW=mods()[0], C=mods()[1].constants, IN=IN, print=_print, get_doc=get_doc,
                  iter_features=iter_features, solid_bodies=solid_bodies, exact_box=exact_box,
                  mass_props=mass_props, use_config=use_config, Units=Units)
    tree = ast.parse(code, mode="exec")
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = ast.Expression(tree.body.pop().value)
    exec(compile(tree, "<run_python>", "exec"), _py_ns)
    result = eval(compile(last, "<run_python>", "eval"), _py_ns) if last else _py_ns.get("result")
    return out.getvalue(), result
