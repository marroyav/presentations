"""Record source evidence and count actual workbook variable rows."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import posixpath
import subprocess
import xml.etree.ElementTree as ET
import zipfile

BASE = Path(__file__).resolve().parent
HOME = Path('/home/arroyave')
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
TABS = ['DAQ', 'OPMON', 'SC', 'PoF', 'SSP', 'WIENER', 'PDU']
DISPLAY_NAMES = {'SSP': 'PDS calibration box'}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def workbook_rows(path):
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        book = ET.fromstring(z.read('xl/workbook.xml'))
        output = {}
        for sheet in book.find('m:sheets', NS):
            target = rels[sheet.get(REL)]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            rows = []
            for row in ET.fromstring(z.read(target)).findall('.//m:sheetData/m:row', NS):
                cells = {}
                for c in row:
                    col = ''.join(x for x in c.get('r', '') if x.isalpha())
                    v = c.find('m:v', NS)
                    if c.get('t') == 'inlineStr':
                        value = ''.join(c.find('m:is', NS).itertext())
                    elif v is not None:
                        value = strings[int(v.text)] if c.get('t') == 's' else v.text
                    else:
                        value = ''
                    cells[col] = value
                rows.append(cells)
            output[sheet.get('name')] = rows
        return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workbook', type=Path, default=HOME/'Downloads/PDS_Operational_Variables_v1.1_Draft.xlsx')
    args = parser.parse_args()
    sheets = workbook_rows(args.workbook)
    counts = {}
    for name in TABS:
        rows = sheets[name]
        role_col = next(k for k, v in rows[0].items() if v == 'Control / Publish')
        status_col = next(k for k, v in rows[0].items() if v == 'Read-path status')
        variables = [r for r in rows[1:] if r.get('B')]
        roles = collections.Counter(r.get(role_col) for r in variables)
        statuses = collections.Counter(r.get(status_col) for r in variables)
        assert set(roles) <= {'Control', 'Publish'}, (name, roles)
        counts[name] = dict(total=len(variables), control=roles['Control'], publish=roles['Publish'],
            known=statuses['Implemented reader'] + statuses['Existing SC binding'],
            pending=statuses['Mapping pending'] + statuses['Not implemented'])
        assert counts[name]['total'] == counts[name]['known'] + counts[name]['pending']
    assert counts['OPMON']['control'] == 0
    total = {k: sum(c[k] for c in counts.values()) for k in counts['DAQ']}
    tex = ['% Generated from workbook variable rows by prepare_evidence.py.']
    for key, macro in [('total','TotalVariables'),('control','TotalControl'),('publish','TotalPublish'),('known','TotalKnown'),('pending','TotalPending')]:
        tex.append(f'\\newcommand{{\\{macro}}}{{{total[key]}}}')
    table = [' & '.join([DISPLAY_NAMES.get(name, name)] + [str(counts[name][k]) for k in ['total','control','publish','pending']]) + r'\\' for name in TABS]
    tex += ['\\newcommand{\\CountsRows}{%', *table, '}']
    (BASE/'counts.tex').write_text('\n'.join(tex)+'\n')
    (BASE/'counts.json').write_text(json.dumps(dict(workbook=str(args.workbook),sha256=sha(args.workbook),tabs=counts,totals=total),indent=2)+'\n')
    files = {
      'S1-services': HOME/'work/icd-sc-pds/sections/03_protocols_services.tex',
      'S1-physical': HOME/'work/icd-sc-pds/sections/02_physical_interface.tex',
      'S1-responsibilities': HOME/'work/icd-sc-pds/sections/01_responsibilities.tex',
      'S1-interactions': HOME/'work/icd-sc-pds/sections/05_proposed_matrix.tex',
      'S1-document': HOME/'work/icd-sc-pds/main.tex',
      'historical-ICD': HOME/'work/racks/sources/power-planning/2025-10-14_EDMS-3309688_DUNE_ICD_SC_PDS_v1.docx',
      'S4-client': HOME/'work/daphne-os/daphne-server/client/ssp_led_control.py',
      'S4-map': HOME/'work/ssp-controller-review-20261005/Registers_v4.2a.xlsx',
      'S5': HOME/'work/daphne-os/docs/kontron-wiener-power-control.md',
      'S6-bindings': HOME/'work/racks/sources/docdb-32655-v8/PDU_UDTs_2026_06_03.json',
      'S6-tests': HOME/'work/racks/sources/docdb-32655-v8/PDU_Test_Matrix_G271_PX3.xlsx',
      'S7': HOME/'work/gizmo-icd/deliverables/GIZMo_Kria_DCS_Intake.xlsx',
      'S8': args.workbook,
      'PoF-rack-plan': HOME/'work/racks/data/fd2-estimate-cells.csv',
      'PoF-rack-workbook': HOME/'work/racks/sources/rack-estimates/FD2_Rack_Estimates_May_2025_TMS.xlsx',
      'PoF-infrastructure': HOME/'work/racks/sources/power-planning/2026-06-10_SC_Infrastructure_and_Installation.pdf',
      'PoF-sizing': BASE/'pof-io-sizing.json',
      'system-counts': BASE/'system-counts.json',
      'system-workbook': HOME/'Downloads/PDS_Operational_Variables_v1.2_System_Draft.xlsx',
      'PDU-rack-guide': HOME/'work/racks/sources/docdb-32655-v8/PX3_Rack_Protection_Setup.pdf',
      'PDU-top-plate-spec': BASE/'source-evidence/PX3-5147R-spec.pdf',
      'PDU-standard-rack-spec': BASE/'source-evidence/PX3-5170V-E2F5-spec.pdf',
    }
    repos = {
      'icd-sc-pds': (HOME/'work/icd-sc-pds', 'bfb2a8b725d9a5a3b7a517f4f9e15fb953eed1f8'),
      'daphne-os': (HOME/'work/daphne-os', 'edc61f126b0a86e9373fb2635f684d053dfde082'),
      'daphnemodules': (HOME/'work/daphnemodules-variable-review','ba6fd3c30b2dbb6e4186242b629fd068208c1e91'),
      'hermesmodules-local': (HOME/'work/pds-trigger-scaffold/hermesmodules','d7de1de6627dff097f282d4753508b588dad10a9'),
    }
    evidence = dict(date='2026-10-14', kind='document and implementation review', no_live_device_checks=True,
        icd=dict(edms_parent='3309688',revision='local draft 0.2',date='2026-09-17',path=str(HOME/'work/icd-sc-pds'),approval='draft for review; not an approved release',figure='section 3.1 DAPHNE service locations and protocol paths'),
        files={key: dict(path=str(p),sha256=sha(p)) for key,p in files.items()}, repositories={})
    for name, (repo, expected) in repos.items():
        actual = subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
        branch = subprocess.check_output(['git','-C',str(repo),'branch','--show-current'],text=True).strip()
        assert actual == expected, (name, actual, expected)
        evidence['repositories'][name] = dict(path=str(repo),revision=actual,branch=branch,
            worktree_status=subprocess.check_output(['git','-C',str(repo),'status','--short'],text=True).strip())
    evidence['implementation_trace'] = str(HOME/'work/daphne-sc-intake-20261014/operational-subset-validation.json')
    evidence['implementation_trace_sha256'] = sha(evidence['implementation_trace'])
    evidence['pof_io_sizing'] = json.loads((BASE/'pof-io-sizing.json').read_text())
    system_counts = json.loads((BASE/'system-counts.json').read_text())
    evidence['expanded_system_counts'] = {k: system_counts[k] for k in ['scope', 'inputs', 'tabs', 'totals', 'additions', 'pdu', 'sources']}
    evidence['pof_inventory_correction'] = dict(date='2026-10-14',source='user correction',working_count='8 temperatures + 8 voltages per eight-channel PoF box',status='PoF mapping pending')
    evidence['editorial_guidance'] = [
      'https://www.gov.uk/guidance/government-design-principles',
      'https://www.gov.uk/service-manual/design/writing-for-user-interfaces',
    ]
    (BASE/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(total))

if __name__ == '__main__':
    main()
