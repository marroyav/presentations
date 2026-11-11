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
RACKS = Path('/home/arroyave/work/racks/sources/rack-estimates/FD2_Rack_Estimates_May_2025_TMS.xlsx')
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


# The starting point is the VD BDE system: ten groups of eight WIECs.
# No HD-to-VD difference belongs in the requested additions count.
aux = sheet_cells(RACKS, 'BDE Aux Rack')
bias = sheet_cells(RACKS, 'Bias HV Rack')
assert int(aux['C14']) == 12 and int(bias['C15']) == 12
assert '8 BDE' in aux['C1'] and 'x 10' in aux['B1']
free_aux = sorted(int(float(aux[f'A{i}'])) for i in range(26, 45)
                  if aux.get(f'B{i}') == 'Space')
free_bias = sorted(int(float(bias[f'A{i}'])) for i in range(36, 46)
                   if bias.get(f'B{i}') == 'Space')
assert free_aux == list(range(3, 22)) and free_bias == list(range(3, 13))
option = {'EL3202': 3, 'EL2878': 2, 'EL9100': 1}
for model, number in option.items():
    assert f'{number} {model}' in aux['K20'] + aux['K21']
rows = [
    {'interface': 'Existing VD BDE protection', 'category': 'VD baseline',
     'additional_modules': 0, 'basis': 'Eight WIECs per group already in the VD baseline'},
    {'interface': 'PDU and LV supply SNMP control/status', 'category': 'Network interface',
     'additional_modules': 0, 'basis': 'No discrete/analog DPS terminal channels for SNMP exchange itself'},
    {'interface': 'Subsystem OPC UA exchange through SC', 'category': 'Network interface',
     'additional_modules': 0, 'basis': 'No discrete/analog DPS terminal channels for OPC UA exchange itself'},
    {'interface': 'New hardwired facility and equipment interfaces', 'category': 'Physical I/O',
     'additional_modules': None, 'basis': 'Needs the VD channel allocation; not counted from HD population differences'},
    {'interface': 'PD flange sensors/heaters', 'category': 'Conditional workbook option',
     'additional_modules': None, 'basis': 'Six-module option recorded in workbook; VD applicability and multiplicity not established'},
    {'interface': 'Additional E-bus supply sections', 'category': 'Support hardware',
     'additional_modules': None, 'basis': 'Depends on actual VD baseline bank loading and added physical modules'},
]
result = {
    'status': 'Corrected VD-only scope; new physical I/O total not established',
    'scope': 'Additional DPS interfaces beyond the existing VD BDE baseline',
    'baseline': {'aux_racks': 10, 'wiecs_per_aux': 8, 'total_wiecs': 80,
                 'pl506_supplies': 20, 'dps_allocation_U_per_aux': 12},
    'additional_interfaces': rows,
    'total_new_physical_io_modules': None,
    'rack_space': {
        'aux_unassigned_contiguous_positions': free_aux,
        'aux_unassigned_contiguous_U': len(free_aux),
        'bias_unassigned_contiguous_positions': free_bias,
        'bias_unassigned_contiguous_U': len(free_bias),
        'bias_dps_allocation_U_per_rack': 12,
        'bias_rail_occupied_length_mm_from_workbook': 337,
        'new_dps_space_reserved_U': None,
        'note': 'Rack positions marked Space are not a reservation for DPS. Auxiliary U9 has a possible ground-plane readout note.'},
    'vd_panel_spare_terminal_capacity': {
        'modules': None, 'rail_length_mm': None,
        'reason': 'The slide 6 drawing is a historical reference. Its gaps and the HD per-group population do not establish free space in the VD eight-WIEC panel.'},
    'pd_flange_option': {
        'source': 'BDE Aux Rack!K20:K21', 'components_as_written': option,
        'modules_per_documented_package': sum(option.values()),
        'vd_new_packages': None, 'vd_new_module_total': None,
        'note': 'Retained as a conditional source item; not multiplied by ten or added to the VD baseline without a VD mapping.'},
    'correction': {
        'excluded_hd_to_vd_conversion_from_new_scope': True,
        'previous_90_150_160_totals_withdrawn': True,
        'previous_mandatory_4U_extension_inference_withdrawn': True,
        'previous_extra_ebus_feed_inference_withdrawn': True,
        'reason': 'They depended on converting the historical six-WIEC pattern and assigning its bank arrangement to VD.'},
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
    'question': 'Slide 6: space and I/O additions beyond the VD BDE baseline',
    'created_at': datetime.now(timezone.utc).isoformat(),
    'status': 'Corrected scope; reviewer not assigned',
    'source_commit': git('rev-parse', 'HEAD').strip(),
    'dirty_state': git('status', '--short').splitlines(),
    'tracked_diff_sha256': hashlib.sha256(git('diff', '--binary', 'HEAD').encode()).hexdigest(),
    'host': platform.node(), 'python': sys.version,
    'run_path': str(HERE), 'command': f'python3 {HERE / "calculate.py"}',
    'inputs_sha256': {str(f): sha(f) for f in [RACKS, HERE / 'calculate.py', HERE / 'assessment.txt']},
    'outputs_sha256': {f.name: sha(f) for f in [HERE / 'calculation.json', HERE / 'module-additions.csv']},
    'acceptance': ['VD baseline is ten groups of eight WIECs',
                   'No HD conversion counted as additional VD scope',
                   'Workbook rack ranges and conditional option reproduced',
                   'Unknown physical I/O totals remain unset, not zero'],
    'result': 'All arithmetic and source-cell assertions passed',
    'limits': ['No installed-panel measurements',
               'Actual VD spare rail capacity and physical additions are not established by the historical reference drawing',
               'Network-interface counts exclude local subsystem readout hardware and any additional wired interlocks'],
}
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
name = f'evidence-{stamp}.json'
(HERE / name).write_text(json.dumps(record, indent=2) + '\n')
(HERE / 'evidence-latest.txt').write_text(name + '\n')
print(json.dumps({'baseline': result['baseline'], 'hd_conversion_counted': False,
                  'total_new_physical_io_modules': None,
                  'aux_empty_block_U': len(free_aux), 'bias_empty_block_U': len(free_bias)}, indent=2))
