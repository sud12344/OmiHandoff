"""SolidWorks MCP server (stdio) - drive and inspect the running SolidWorks over COM.

Registered in OMi_Handoff/.mcp.json as "solidworks". All COM calls run on one dedicated
thread; a call that outlives its timeout keeps running there and later calls queue behind it.
Never print() in this process - stdout is the MCP channel.
"""
import asyncio
import fnmatch
import io
import json
import math
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import pythoncom

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swcom as S  # noqa: E402
from mcp.server.mcpserver import Image, MCPServer  # noqa: E402

INSTRUCTIONS = """Drive the user's running SolidWorks 2026 (COM). Lengths are inches unless units='mm';
angles are degrees. `doc` arguments take a full path, file name or title; empty = active document.
Verify a part: doc_info -> rebuild -> sweep_configs (every configuration) -> geometry (cylinder
diameters, cone angles, plane offsets) -> screenshot. run_macro runs a .bas build macro headless;
use const_overrides to redirect SAVE_PATH/REPORT_PATH to a scratch folder for a dry run.
run_python is the escape hatch for anything the tools don't cover."""

mcp = MCPServer("solidworks", instructions=INSTRUCTIONS)

_com = ThreadPoolExecutor(max_workers=1, thread_name_prefix="swcom", initializer=pythoncom.CoInitialize)
_job = {"name": None, "since": None}


def _dump(obj):
    return json.dumps(obj, ensure_ascii=False, default=str)


async def com(name, fn, *args, timeout=600):
    """Run fn on the COM thread; turn failures into readable error text."""
    def wrapped():
        _job.update(name=name, since=time.time())
        try:
            return fn(*args)
        finally:
            _job.update(name=None, since=None)

    fut = asyncio.get_running_loop().run_in_executor(_com, wrapped)
    try:
        return await asyncio.wait_for(asyncio.shield(fut), timeout)
    except asyncio.TimeoutError:
        return {"error": f"'{name}' still running in SolidWorks after {timeout}s; later calls will queue behind it."}
    except S.SwError as e:
        return {"error": str(e)}
    except Exception as e:  # COM errors etc. - keep the server alive, show where it failed
        tb = traceback.format_exception(e)
        return {"error": f"{type(e).__name__}: {e}", "trace": "".join(tb[-3:])[-1500:]}


def _doc_brief(d):
    return {"title": d.GetTitle(), "path": d.GetPathName() or None, "type": S.DOC_TYPES.get(d.GetType(), d.GetType()),
            "config": S.active_config(d), "unsaved": bool(d.GetSaveFlag())}


# ================================================================ session / documents
@mcp.tool(structured_output=False)
async def sw_status() -> str:
    """SolidWorks connection check: version, open documents (active config, unsaved flag), active doc,
    and whether a long call (e.g. run_macro) is still running."""
    if _job["name"]:
        return _dump({"busy": _job["name"], "for_s": round(time.time() - _job["since"], 1)})

    def f():
        sw = S.app()
        active = sw.ActiveDoc
        return {"revision": sw.RevisionNumber(), "docs": [_doc_brief(d) for d in S.open_docs()],
                "active": S.W(active, "IModelDoc2").GetTitle() if active is not None else None}
    return _dump(await com("sw_status", f))


@mcp.tool(structured_output=False)
async def open_doc(path: str, config: str = "", read_only: bool = False) -> str:
    """Open (or activate, if already open) a part/assembly/drawing, optionally in a configuration.
    STEP/IGES/Parasolid files are imported as new parts. Opening never modifies the file on disk."""
    def f():
        d = S.get_doc(path)                 # opens paths that are not open yet
        S.activate(d)
        S.use_config(d, config)
        return _doc_brief(d)
    return _dump(await com("open_doc", f, timeout=300))


@mcp.tool(structured_output=False)
async def close_doc(doc: str = "", all_docs: bool = False, discard_unsaved: bool = False) -> str:
    """Close one document (default: active) or all. Refuses to drop unsaved changes unless discard_unsaved=True."""
    def f():
        sw = S.app()
        if all_docs:
            dirty = [d.GetTitle() for d in S.open_docs() if d.GetSaveFlag()]
            sw.CloseAllDocuments(discard_unsaved)
            left = [d.GetTitle() for d in S.open_docs()]
            return {"closed_all": True, "left_open": left, "unsaved_kept": [] if discard_unsaved else dirty}
        d = S.get_doc(doc)
        if d.GetSaveFlag() and not discard_unsaved:
            raise S.SwError(f"'{d.GetTitle()}' has unsaved changes - save_doc first or pass discard_unsaved=True")
        title = d.GetTitle()
        sw.CloseDoc(title)
        return {"closed": title}
    return _dump(await com("close_doc", f))


@mcp.tool(structured_output=False)
async def save_doc(doc: str = "", save_as: str = "", as_copy: bool = True, overwrite: bool = False) -> str:
    """Save the document, or export/save-as to `save_as` (format from extension: .SLDPRT .STEP .x_t .STL
    .PDF .png ...). as_copy=True keeps the open document pointing at its original file.
    Refuses to overwrite an existing file unless overwrite=True."""
    def f():
        d = S.get_doc(doc)
        if not save_as:
            ok, err, warn = d.Save3(1, 0, 0)
            if not ok:
                raise S.SwError(f"Save failed: {S.flag_names('swFileSaveError_', err)}")
            return {"saved": d.GetPathName(), "warnings": S.flag_names("swFileSaveWarning_", warn)}
        target = os.path.abspath(save_as)
        if os.path.exists(target) and not overwrite:
            raise S.SwError(f"{target} exists - pass overwrite=True to replace it")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        ext = S.W(d.Extension, "IModelDocExtension")
        ok, err, warn = ext.SaveAs3(target, 0, 1 | (2 if as_copy else 0), None, None, 0, 0)
        if not ok:
            raise S.SwError(f"SaveAs failed: {S.flag_names('swFileSaveError_', err)}")
        return {"saved_as": target, "bytes": os.path.getsize(target), "doc_now": d.GetPathName(),
                "warnings": S.flag_names("swFileSaveWarning_", warn)}
    return _dump(await com("save_doc", f, timeout=900))


# ================================================================ inspection
@mcp.tool(structured_output=False)
async def doc_info(doc: str = "", max_configs: int = 80) -> str:
    """Overview of a document: type, path, units, material, active config and configuration names,
    design table present, feature/body counts, and any rebuild errors/warnings."""
    def f():
        d = S.get_doc(doc)
        names = S.config_names(d)
        info = _doc_brief(d)
        info.update({
            "units": S.const_name("swUnitSystem_", d.GetUserPreferenceIntegerValue(S.mods()[1].constants.swUnitSystem)),
            "material": S.material(d),
            "n_configs": len(names),
            "configs": names[:max_configs] + ([f"... {len(names) - max_configs} more"] if len(names) > max_configs else []),
            "design_table": d.GetDesignTable() is not None,
            "n_features": sum(1 for x in S.iter_features(d) if x.GetTypeName2() not in S.SYSTEM_FEATURE_TYPES),
            "solid_bodies": len(S.solid_bodies(d)),
            "errors": S.feature_errors(d),
        })
        return info
    return _dump(await com("doc_info", f))


@mcp.tool(structured_output=False)
async def list_features(doc: str = "", pattern: str = "*", sub_features: bool = False, config: str = "") -> str:
    """Feature tree in order as 'Name [Type]' plus flags (suppressed / error). pattern is a glob on the
    feature name (e.g. 'THD_*'). System folders are omitted. config activates that configuration first."""
    def f():
        d = S.get_doc(doc)
        S.use_config(d, config)
        rows = []
        for x in S.iter_features(d, sub=sub_features):
            t = x.GetTypeName2()
            if t in S.SYSTEM_FEATURE_TYPES or not fnmatch.fnmatchcase(x.Name, pattern):
                continue
            row = f"{x.Name} [{t}]"
            if x.IsSuppressed():
                row += " SUPPRESSED"
            code, warn = x.GetErrorCode2()
            if code:
                row += f" {'WARNING' if warn else 'ERROR'}:{S.const_name('swFeatureError_', code)}"
            rows.append(row)
        return {"doc": d.GetTitle(), "config": S.active_config(d), "features": rows}
    return _dump(await com("list_features", f))


@mcp.tool(structured_output=False)
async def rebuild(doc: str = "", config: str = "", units: str = "in") -> str:
    """Force a full rebuild (optionally in a configuration) and report errors/warnings, solid body
    count, volume and the tight bounding box."""
    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        S.use_config(d, config)
        t0 = time.time()
        ok = d.ForceRebuild3(False)
        bodies = S.solid_bodies(d)
        mp = S.mass_props(d) if bodies else None
        box = S.exact_box(bodies)
        errors = S.feature_errors(d)
        return {"doc": d.GetTitle(), "config": S.active_config(d), "rebuild_ok": bool(ok) and not S.hard_errors(errors),
                "secs": round(time.time() - t0, 2), "errors": errors, "solid_bodies": len(bodies),
                "volume": u.V(mp["volume"]) if mp else None,
                "box": {"min": u.P(box[:3]), "max": u.P(box[3:]), "size": u.P([box[i + 3] - box[i] for i in range(3)])} if box else None,
                "units": u.name}
    return _dump(await com("rebuild", f))


@mcp.tool(structured_output=False)
async def sweep_configs(doc: str = "", configs: list[str] | None = None, dims: list[str] | None = None,
                        units: str = "in", timeout_s: int = 1800) -> str:
    """Activate + rebuild EVERY configuration (or the listed ones) and report per config: rebuild
    errors, solid body count, volume, bounding-box size, and the values of `dims` (full names like
    'D1@DRIVE'). Restores the original configuration. The main 'does the design table work' check."""
    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        original = S.active_config(d)
        names = configs or S.config_names(d)
        rows, bad = [], 0
        try:
            for n in names:
                t0 = time.time()
                S.use_config(d, n)
                d.ForceRebuild3(False)
                errors = S.feature_errors(d)
                bodies = S.solid_bodies(d)
                mp = S.mass_props(d) if bodies else None
                box = S.exact_box(bodies)
                row = {"config": n, "ok": not S.hard_errors(errors) and len(bodies) == 1,
                       "bodies": len(bodies), "volume": u.V(mp["volume"]) if mp else None,
                       "size": u.P([box[i + 3] - box[i] for i in range(3)]) if box else None,
                       "secs": round(time.time() - t0, 2)}
                if errors:
                    row["errors"] = [f"{e['feature']}:{e['error']}{' (warn)' if e['warning'] else ''}" for e in errors]
                if dims:
                    vals = {}
                    for name in dims:
                        try:
                            dim = S.get_parameter(d, name)
                            v = S.dim_value(dim)
                            vals[name] = round(math.degrees(v), 3) if dim.GetType() == 1 else u.L(v)
                        except S.SwError:
                            vals[name] = None
                    row["dims"] = vals
                bad += not row["ok"]
                rows.append(row)
        finally:
            if original:
                S.use_config(d, original)
        return {"doc": d.GetTitle(), "units": u.name, "checked": len(rows), "not_ok": bad, "restored": original,
                "rows": rows}
    return _dump(await com("sweep_configs", f, timeout=timeout_s))


@mcp.tool(structured_output=False)
async def get_dimensions(doc: str = "", feature: str = "*", name: str = "*", config: str = "", units: str = "in") -> str:
    """Dimension values in the active (or given) configuration, keyed by full name 'DimName@Feature'
    (the name set_dimensions / sweep_configs take). feature/name are globs, e.g. feature='DRIVE'.
    Linear values in `units`, angles in degrees; driven (reference) dimensions are listed separately."""
    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        S.use_config(d, config)
        linear, angular, driven = {}, {}, []
        for full, dim in S.iter_dimensions(d, feature):
            if not fnmatch.fnmatchcase(dim.Name, name):
                continue
            v = S.dim_value(dim)
            if dim.GetType() == 1:
                angular[full] = round(math.degrees(v), 4)
            else:
                linear[full] = u.L(v)
            if dim.DrivenState == 1:
                driven.append(full)
        return {"doc": d.GetTitle(), "config": S.active_config(d), "units": u.name,
                "linear": linear, "angular_deg": angular, "driven": driven}
    return _dump(await com("get_dimensions", f))


@mcp.tool(structured_output=False)
async def set_dimensions(values: dict[str, float], doc: str = "", scope: str = "this",
                         configs: list[str] | None = None, units: str = "in") -> str:
    """Set dimensions by full name ({'D1@DRIVE': 1.48, 'SEATB@DRIVE': 37}) then rebuild. Linear in
    `units`, angles in degrees. scope: 'this' (active config), 'all', or 'configs' (the listed ones).
    Changes the model in memory only - nothing is saved. Reports per-dimension status and rebuild errors."""
    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        opt = {"this": 1, "all": 2, "configs": 3}.get(scope)
        if opt is None:
            raise S.SwError("scope must be 'this', 'all' or 'configs'")
        status = {}
        for full, v in values.items():
            dim = S.get_parameter(d, full)
            sysv = math.radians(v) if dim.GetType() == 1 else u.to_m(v)
            r = dim.SetSystemValue3(sysv, opt, configs if opt == 3 else None)
            status[full] = S.SETVALUE_STATUS.get(r, r)
        d.ForceRebuild3(False)
        errors = S.feature_errors(d)
        bodies = S.solid_bodies(d)
        mp = S.mass_props(d) if bodies else None
        return {"status": status, "config": S.active_config(d), "errors": errors, "solid_bodies": len(bodies),
                "volume": u.V(mp["volume"]) if mp else None, "units": u.name}
    return _dump(await com("set_dimensions", f))


@mcp.tool(structured_output=False)
async def mass_properties(doc: str = "", config: str = "", units: str = "in") -> str:
    """Volume, surface area, mass/density (material), centre of mass and tight bounding box."""
    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        S.use_config(d, config)
        mp = S.mass_props(d)
        if mp is None:
            raise S.SwError("No mass properties (empty model?)")
        box = S.exact_box(S.solid_bodies(d))
        mat = S.material(d)
        out = {"doc": d.GetTitle(), "config": S.active_config(d), "units": u.name, "material": mat,
               "volume": u.V(mp["volume"]), "surface_area": u.A(mp["area"]), "center_of_mass": u.P(mp["com"]),
               "box": {"min": u.P(box[:3]), "max": u.P(box[3:]), "size": u.P([box[i + 3] - box[i] for i in range(3)])} if box else None}
        if mat:     # without a material SolidWorks reports a placeholder density
            out.update(mass_kg=round(mp["mass_kg"], 6), density_kg_m3=round(mp["density_kg_m3"], 2))
        return out
    return _dump(await com("mass_properties", f))


@mcp.tool(structured_output=False)
async def geometry(doc: str = "", config: str = "", units: str = "in", max_items: int = 60) -> str:
    """Measured B-rep geometry per solid body, for checking a model against catalog numbers:
    distinct cylinders (diameter, axis, inner=bore/outer=boss, axial span), cones (half & included angle,
    reference diameter), planes (normal + offset from origin; hex flats sit at +/- AF/2 from the hex axis),
    tori, face counts, and geometry-check fault count."""
    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        S.use_config(d, config)
        bodies = S.solid_bodies(d)
        if not bodies:
            raise S.SwError("No solid bodies")
        out = []
        for i, b in enumerate(bodies):
            g = S.body_geometry(b, u, max_items)
            box = S.exact_box([b])
            g = {"body": i, "name": b.Name, "faults": S.body_faults(b),
                 "box": {"min": u.P(box[:3]), "max": u.P(box[3:])}, **g}
            out.append(g)
        return {"doc": d.GetTitle(), "config": S.active_config(d), "units": u.name, "bodies": out}
    return _dump(await com("geometry", f, timeout=900))


# ================================================================ visual check
@mcp.tool(structured_output=False)
async def screenshot(doc: str = "", views: list[str] | None = None, config: str = "",
                     display: str = "shaded_edges", section_plane: str = "", section_offset: float = 0.0,
                     reverse_section: bool = False, width: int = 1100, units: str = "in") -> list:
    """Picture of the model as SolidWorks renders it. views: any of isometric, trimetric, dimetric, front,
    back, left, right, top, bottom (several -> labelled grid; default isometric). display: shaded_edges,
    shaded, wireframe, hidden_removed, hidden_grayed. section_plane (e.g. 'Front Plane') + section_offset
    (in `units`) gives a section view - the way to see bores, grooves and thread runouts.
    The PNG is also saved; its path is in the text result."""
    names = views or ["isometric"]

    def f():
        u = S.Units(units)
        d = S.get_doc(doc)
        S.use_config(d, config)
        images = S.capture(d, names, display, section_plane, u.to_m(section_offset), reverse_section)
        sheet = S.compose(images, names if len(names) > 1 else [""], max(300, min(width, 2000)))
        path = os.path.join(S.WORK, f"shot_{S._stem(d.GetTitle())}_{time.strftime('%H%M%S')}.png")
        sheet.save(path)
        buf = io.BytesIO()
        sheet.save(buf, "PNG")
        return buf.getvalue(), {"doc": d.GetTitle(), "config": S.active_config(d), "views": names,
                                "section": section_plane or None, "saved": path}
    r = await com("screenshot", f, timeout=300)
    if isinstance(r, dict):
        return [_dump(r)]
    png, meta = r
    return [Image(data=png, format="png"), _dump(meta)]


# ================================================================ changing the model
@mcp.tool(structured_output=False)
async def activate_config(config: str, doc: str = "") -> str:
    """Make a configuration active (rebuilds it) and report errors."""
    def f():
        d = S.get_doc(doc)
        S.use_config(d, config)
        d.ForceRebuild3(False)
        return {"doc": d.GetTitle(), "config": S.active_config(d), "errors": S.feature_errors(d)}
    return _dump(await com("activate_config", f))


@mcp.tool(structured_output=False)
async def set_suppression(features: list[str], suppressed: bool, doc: str = "", scope: str = "this") -> str:
    """Suppress/unsuppress features by name or glob (e.g. ['THD_*'] to show or hide threads).
    scope 'this' = active configuration, 'all' = every configuration. Rebuilds; nothing is saved."""
    def f():
        d = S.get_doc(doc)
        opt = {"this": 1, "all": 2}.get(scope)
        if opt is None:
            raise S.SwError("scope must be 'this' or 'all'")
        hits = S.find_features(d, features)
        if not hits:
            raise S.SwError(f"No features match {features}")
        done = {x.Name: bool(x.SetSuppression2(0 if suppressed else 1, opt, None)) for x in hits}
        d.ForceRebuild3(False)
        return {"changed": done, "config": S.active_config(d), "errors": S.feature_errors(d)}
    return _dump(await com("set_suppression", f))


@mcp.tool(structured_output=False)
async def run_macro(path: str, entry: str = "", const_overrides: dict[str, str | float | bool] | None = None,
                    module: str = "", timeout_s: int = 3600) -> str:
    """Run a VBA macro inside SolidWorks without the VBA editor. .bas files (the Build_*_MASTER.bas
    generators) are converted to a temporary .swb: Attribute lines dropped, MsgBox calls logged instead
    of blocking, Consts optionally overridden - e.g. {"SAVE_PATH": "C:\\\\...\\\\scratch\\\\x.SLDPRT",
    "REPORT_PATH": "..."} for a dry run that cannot touch 11_MASTERS. entry defaults to the first
    'Sub Build*()' (else main). .swp runs as-is (needs module). Returns RunMacro2 status, the MsgBox
    texts, a summary of the report file (OK/FAIL counts + FAIL lines) and the documents it opened."""
    def f():
        sw = S.app()
        src = os.path.abspath(path)
        if not os.path.exists(src):
            raise S.SwError(f"File not found: {src}")
        ext = os.path.splitext(src)[1].lower()
        consts, log, ent = {}, None, entry
        if ext in (".bas", ".swb", ".txt"):
            run_path, ent, consts, log = S.prepare_macro(src, entry, const_overrides)
            if os.path.exists(log):
                os.remove(log)
        elif ext == ".swp":
            if const_overrides:
                raise S.SwError("const_overrides only work on text macros (.bas/.swb)")
            if not (entry and module):
                methods = sw.GetMacroMethods(src, 0) or []
                raise S.SwError(f".swp needs module and entry; methods in file: {list(methods)}")
            run_path = src
        else:
            raise S.SwError("Macro must be .bas, .swb or .swp")
        before = {d.GetTitle() for d in S.open_docs()}
        t0 = time.time()
        ok, err = sw.RunMacro2(run_path, module, ent, 1, 0)      # 1 = unload after run
        secs = round(time.time() - t0, 1)
        msgs = [ln[8:] if ln.startswith("MSGBOX: ") else ln
                for ln in (S._read_text(log).splitlines() if log and os.path.exists(log) else [])]
        opened = [_doc_brief(d) for d in S.open_docs() if d.GetTitle() not in before]
        active = sw.ActiveDoc
        failure = None
        if not ok:
            failure = S.const_name("swRunMacroError_", err) if err else \
                "macro did not load/compile - open it in the VBA editor to see the error"
        return {"ran": ent, "ok": bool(ok), "error": failure,
                "secs": secs, "msgbox": msgs, "report": S.summarize_report(consts.get("REPORT_PATH")),
                "save_path": consts.get("SAVE_PATH"), "new_docs": opened,
                "active": S.W(active, "IModelDoc2").GetTitle() if active is not None else None,
                "swb": run_path if run_path != src else None}
    return _dump(await com(f"run_macro {os.path.basename(path)}", f, timeout=timeout_s))


@mcp.tool(structured_output=False)
async def run_python(code: str, timeout_s: int = 600) -> str:
    """Execute Python on the COM thread against the live API (escape hatch). Names available: sw
    (ISldWorks), doc (active IModelDoc2 or None), W(obj,'IFace2') to early-bind a returned object,
    C (swconst constants), IN=0.0254, get_doc, iter_features, solid_bodies, exact_box, mass_props,
    use_config, Units. API units are metres/radians. print() is captured; the last expression (or a
    variable named result) is returned. The namespace persists between calls."""
    def f():
        S._py_ns.pop("result", None)
        out, result = S.run_python(code)
        try:
            json.dumps(result)
        except (TypeError, ValueError):
            result = repr(result)
        return {"stdout": out[-20000:], "result": result}
    return _dump(await com("run_python", f, timeout=timeout_s))


if __name__ == "__main__":
    mcp.run()
