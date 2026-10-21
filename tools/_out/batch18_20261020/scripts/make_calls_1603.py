"""SolidWorks dry run of 1603 with the A14 row (batch-18 toolset): build into dryrun/1603, sweep, then sweep the shipped master read-only."""
import json, os
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
B = os.path.join(H, 'tools', '_out', 'batch18_20261020')
D = os.path.join(B, 'dryrun', '1603'); os.makedirs(D, exist_ok=True)
calls = [['sw_status', {}],
         ['run_macro', {'path': os.path.join(B, 'regen', 'tee', 'Build_1603_MASTER.bas'), 'timeout_s': 1750,
                        'const_overrides': {'TABLE_PATH': os.path.join(B, 'regen', 'tee', 'DesignTable_1603_SW2.xlsx'),
                                            'SAVE_PATH': os.path.join(D, '1603_MASTER.SLDPRT'),
                                            'REPORT_PATH': os.path.join(D, 'Build_1603_report.txt')}}],
         ['sweep_configs', {'doc': '1603_MASTER', 'timeout_s': 1700}],
         ['close_doc', {'doc': '1603_MASTER', 'discard_unsaved': True}],
         ['open_doc', {'path': os.path.join(H, '11_MASTERS', '1603_MASTER.SLDPRT'), 'read_only': True}],
         ['sweep_configs', {'doc': '1603_MASTER', 'timeout_s': 1700}],
         ['close_doc', {'doc': '1603_MASTER', 'discard_unsaved': True}]]
json.dump(calls, open(os.path.join(B, 'dryrun', 'calls_1603.json'), 'w'), indent=1)
print('ok')
