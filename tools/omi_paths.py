"""Central path configuration for every OMi tool (generators, checks, measuring scripts, coverage).

All paths derive from the repository root (the OMi_Handoff folder), so the tools run the same on the user's
Windows machine (Claude Code) and anywhere else the folder is copied. Override with environment variables:
  OMI_ROOT   the OMi_Handoff folder (default: the parent of this tools/ folder)
  OMI_DEV    the Windows path of OMi_Handoff that is WRITTEN INTO THE VBA MACROS (TABLE_PATH, SAVE_PATH,
             REPORT_PATH). Default: the user's machine. It is only text inside the .bas files.
  GS_OUT / GT_OUT   output folders of gen_straight2.py / gen_tee.py (default tools/_out/straight, tools/_out/tee)
"""
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.environ.get('OMI_ROOT') or os.path.dirname(TOOLS))
DEV = os.environ.get('OMI_DEV', r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff')

DOCS = os.path.join(ROOT, '00_DOCS')
MASTER_DATA = os.path.join(ROOT, '01_MASTER_DATA')
WORKBOOK = os.path.join(MASTER_DATA, 'OMi_Fitting_Library_MasterData_v1.xlsx')
SCRIPTS = os.path.join(ROOT, '03_SCRIPTS')              # VBA build macros + their reports (the macros write reports here)
DESIGN_TABLES = os.path.join(ROOT, '04_DESIGN_TABLES')  # review tables DesignTable_<root>.xlsx (INPUT) and DesignTable_<root>_SW2.xlsx (generated)
RAW = os.path.join(ROOT, '07_RAW_EXTRACTS')
STEP_DIR = os.path.join(ROOT, '09_STEP_FILES')         # Brennan STEPs, BRENNAN_<part number>.stp
MASTERS = os.path.join(ROOT, '11_MASTERS')

GENERATORS = os.path.join(TOOLS, 'generators')
TEMPLATES = os.path.join(GENERATORS, 'templates')
OUT = os.path.join(TOOLS, '_out')
OUT_STRAIGHT = os.environ.get('GS_OUT', os.path.join(OUT, 'straight'))
OUT_TEE = os.environ.get('GT_OUT', os.path.join(OUT, 'tee'))
SCRATCH = os.path.join(OUT, 'scratch')
COVERAGE_WORK = os.path.join(TOOLS, 'coverage', 'work')


REV_EXTRA = [d for d in os.environ.get('OMI_REV_EXTRA', '').split(os.pathsep) if d]


def review_table(root):
    """the Air-Way/OMi review table of a root (single source of truth: 04_DESIGN_TABLES).
    2026-10-20 (ORFS staging): OMI_REV_EXTRA = extra folders (os.pathsep-separated) searched only for a table that 04_DESIGN_TABLES does
    not have, e.g. the staged FS tables (tools/_out/brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES). Unset = unchanged behaviour."""
    f = os.path.join(DESIGN_TABLES, f'DesignTable_{root}.xlsx')
    if not os.path.exists(f):
        for d in REV_EXTRA:
            g = os.path.join(d, f'DesignTable_{root}.xlsx')
            if os.path.exists(g):
                return g
    return f


def step(pn):
    """a Brennan STEP by part number: 09_STEP_FILES/BRENNAN_<pn>.stp"""
    return os.path.join(STEP_DIR, f'BRENNAN_{pn}.stp')
