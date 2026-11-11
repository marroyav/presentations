#!/usr/bin/env python3
"""Reproduce the slide 6 I/O space estimate; does not modify the deck."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PARTS = Path('/home/arroyave/work/kerberos-doc-access/downloads/2401090/4/CE_Interlock_Parts_List.xlsx')
RACKS = Path('/home/arroyave/work/racks/sources/rack-estimates/FD2_Rack_Estimates_May_2025_TMS.xlsx')
DRAWING = Path('/home/arroyave/work/kerberos-doc-access/downloads/2401090/4/F10xxxxxx-Prelim_-_DDSS_Controls.pdf')
POWER = Path('/home/arroyave/work/kerberos-doc-access/downloads/2401090/4/DDSS_Controls_Power_Analysis.xlsx')
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def sheet_cells(path, sheet_name):
    with zipfile.ZipFile(path) as z:
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            shared = [''.join(t.text or '' for t in el.iter('{' + NS['s'] + '}t'))
                      for el in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rel = {el.attrib['Id']: el.attrib['Target']
               for el in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets = ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets', NS)
        sheet = next(el for el in sheets if el.attrib['name'] == sheet_name)
        target = rel[sheet.attrib['{' + NS['r'] + '}id']]
        target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
        cells = {}
        for c in ET.fromstring(z.read(target)).findall('.//s:sheetData/s:row/s:c', NS):
            v = c.find('s:v', NS)
            value = v.text if v is not None else None
            if c.attrib.get('t') == 's' and value is not None:
                value = shared[int(value)]
            elif c.attrib.get('t') == 'inlineStr':
                value = ''.join(t.text or '' for t in c.findall('.//s:t', NS))
            cells[c.attrib['r']] = value
        return cells


parts = sheet_cells(PARTS, 'Interlocks M&S')
aux = sheet_cells(RACKS, 'BDE Aux Rack')
bias = sheet_cells(RACKS, 'Bias HV Rack')

# Scale the six-WIEC reference pattern only. This is not a released VD BOM.
# Channel capacities, aligned widths and typical E-bus currents were checked
# against the official Beckhoff sources listed in assessment.txt.
spec = [
    ('EL1004', 'Fan feedback', 29, 4, 12, 90),
    ('EL2034', 'Fan power outputs', 28, 4, 12, 120),
    ('EL3202-0010', 'RTD inputs', 20, 2, 12, 190),
    ('EL2878-0005', 'Heater outputs', 24, 8, 12, 100),
    ('EK1521', 'PTC fibre links', 25, 1, 23, 350),
]
rows = []
for model, function, row, channels, width, current in spec:
    baseline = int(parts[f'C{row}']) // 25
    vd = baseline * 8 // 6
    assert baseline * 8 % 6 == 0
    delta = vd - baseline
    rows.append(dict(model=model, function=function, source_cell=f'Interlocks M&S!C{row}',
                     six_wiec_count=baseline, eight_wiec_count=vd,
                     added_per_aux=delta, added_for_ten_aux=delta * 10,
                     channels_per_module=channels, added_aligned_width_mm=delta * width,
                     added_typical_ebus_mA=delta * current))

delta_count = sum(r['added_per_aux'] for r in rows)
delta_width = sum(r['added_aligned_width_mm'] for r in rows)
assert delta_count == 9 and delta_width == 130
assert int(aux['C14']) == 12 and int(bias['C15']) == 12
free_aux = sorted(int(float(aux[f'A{i}'])) for i in range(26, 45)
                  if aux.get(f'B{i}') == 'Space')
free_bias = sorted(int(float(bias[f'A{i}'])) for i in range(36, 46)
                   if bias.get(f'B{i}') == 'Space')
assert free_aux == list(range(3, 22)) and free_bias == list(range(3, 13))

# Keep two 4-channel PL506 inhibit terminals for the eight active WIEC feeds.
# The unused four channel positions on the two supplies are not added here.
top_typical_mA = 8 * 90 + 8 * 120 + 8 * 190 + 4 * 100 + 2 * 130
pd_option_mA = 3 * 190 + 2 * 100
assert top_typical_mA == 3860 and top_typical_mA + pd_option_mA == 4630

result = {
    'status': 'Engineering estimate; not reviewed or approved for procurement',
    'scope': 'VD; rebase the historical six-WIEC reference to ten eight-WIEC auxiliary groups',
    'aux_racks': 10,
    'existing_dps_allocation_U_per_aux': 12,
    'unassigned_contiguous_aux_rack_positions': free_aux,
    'unassigned_contiguous_bias_rack_positions': free_bias,
    'bias_rail_occupied_length_mm_from_workbook': 337,
    'module_additions': rows,
    'eight_wiec_rebase': {'added_modules_per_aux': delta_count,
                         'added_modules_ten_aux': delta_count * 10,
                         'added_aligned_width_mm_per_aux': delta_width},
    'pd_flange_option_from_workbook': {
        'source': 'BDE Aux Rack!K20:K21; this note inherits the earlier design assumptions',
        'components': {'EL3202': 3, 'EL2878': 2, 'EL9100': 1},
        'modules_per_aux': 6, 'modules_ten_aux': 60,
        'aligned_width_mm_per_aux': 72},
    'combined_allowance_before_extra_ebus_feed': {
        'modules_per_aux': 15, 'modules_ten_aux': 150,
        'aligned_width_mm_per_aux': 202},
    'ebus_check': {
        'scope': 'Signal terminals on the first bank only; excludes field loads and optical-link bank',
        'two_sections_capacity_mA': 4000,
        'eight_wiec_signal_terminals_typical_mA': top_typical_mA,
        'eight_wiec_plus_pd_option_typical_mA': top_typical_mA + pd_option_mA,
        'extra_EL9410_for_combined_case_minimum': 1,
        'combined_modules_including_extra_feed_per_aux': 16,
        'combined_modules_including_extra_feed_ten_aux': 160,
        'combined_added_aligned_width_including_extra_feed_mm_per_aux': 214,
        'limit': 'Typical-current arithmetic. Partition and actual peak currents must satisfy 2 A per section; field power is separate.'},
    'network_connections': {
        'extra_discrete_or_analog_terminals_for_snmp_or_opcua_alone': 0,
        'note': 'PDU, LV-supply and subsystem software connections do not map one-to-one to physical I/O terminals. Hardwired interfaces are additional.'},
    'central_panel_drawing_estimate': {
        'basis': 'Manual reading of page 2 rendered at 3000 pixels; approximately 123-pixel gap over 681-pixel 19-inch panel width',
        'nominal_gap_mm': round(123 / 681 * 19 * 25.4, 1),
        'cx5140_width_increase_allowance_mm': 20,
        'estimated_gap_after_cpu_change_mm': round(123 / 681 * 19 * 25.4 - 20, 1),
        'geometric_12mm_module_count_after_cpu_change': 5,
        'limit': 'Scaled drawing estimate, not a dimensioned spare-space allocation; excludes wiring and service clearances.'},
    'proposed_space_reservation': {
        'aux_extension_U_per_affected_rack': 4,
        'status': 'Proposed layout allowance; not a completed panel design',
        'note': 'A separate extension panel gives room for the VD rebase and the optional PD hardware without relying on the crowded 2020 reference rails.'},
}
with (HERE / 'module-additions.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
(HERE / 'calculation.json').write_text(json.dumps(result, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.run(['git', *args], cwd=REPO, capture_output=True, text=True, check=True).stdout

record = {
    'question': 'Slide 6: space for added I/O and potential VD module additions',
    'created_at': datetime.now(timezone.utc).isoformat(),
    'status': 'Estimate; reviewer not assigned',
    'source_commit': git('rev-parse', 'HEAD').strip(),
    'dirty_state': git('status', '--short').splitlines(),
    'tracked_diff_sha256': hashlib.sha256(git('diff', '--binary', 'HEAD').encode()).hexdigest(),
    'host': platform.node(), 'python': sys.version,
    'run_path': str(HERE), 'command': f'python3 {HERE / "calculate.py"}',
    'inputs_sha256': {str(f): sha(f) for f in [PARTS, RACKS, DRAWING, POWER, HERE / 'calculate.py', HERE / 'assessment.txt']},
    'outputs_sha256': {f.name: sha(f) for f in [HERE / 'calculation.json', HERE / 'module-additions.csv']},
    'acceptance': ['Workbook rack ranges and allocations reproduced',
                   'VD delta totals 9 modules/130 mm per auxiliary group',
                   'PD option and E-bus additions recorded separately',
                   'No network tag counted as a physical I/O terminal'],
    'result': 'All arithmetic assertions passed',
    'limits': ['No installed-panel measurements', 'No new approved VD panel layout or BOM',
               'Typical E-bus currents do not qualify power or timing performance',
               'Facility hardwired channel count is not fixed by the current matrix'],
}
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
(HERE / f'evidence-{stamp}.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'added_per_aux': delta_count, 'added_for_ten_aux': delta_count * 10,
                  'combined_with_pd_and_feed_per_aux': 16,
                  'aux_empty_block_U': len(free_aux), 'bias_empty_block_U': len(free_bias)}, indent=2))
