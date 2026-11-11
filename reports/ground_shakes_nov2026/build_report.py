#!/usr/bin/env python3
"""Check existing results, freeze source identities, and prepare report values."""
from pathlib import Path
import ast
import csv
import datetime
import hashlib
import json
import platform
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ANALYSIS = REPO.parent / 'ground-shake-data/analysis'
SOURCE_PDF = REPO.parent / 'ground-shake-recovery-20261015/edms/ground_shake_200726.pdf'

def load(name):
    return json.loads((ANALYSIS / name).read_text())

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def read_map(name, apa):
    tree = ast.parse((ANALYSIS/'first-pass'/name).read_text())
    assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Name)
                      and n.targets[0].id == f'apa_{apa}_data')
    return [[tuple(ast.literal_eval(arg) for arg in cell.args) for cell in row.elts]
            for row in assignment.value.elts]

# Independently transcribed from EDMS 3493627 v1, pages 18 and 20.
# Rows run top to bottom; cells run left to right in those source views.
source_rows = {
    1: [[0,2,5,7],[6,4,3,1],[30,32,35,37],[36,34,33,31],
        [10,12,15,17],[16,14,13,11],[40,42,45,47],[27,25,22,20],
        [41,43,44,46],[26,24,23,21]],
    2: [[27,25,22,20],[21,23,24,26],[37,35,32,30],[31,33,34,36],
        [7,5,2,0],[1,3,4,6],[17,15,12,10],[11,13,14,16],
        [47,45,42,40],[41,43,44,46]],
}
orientation = {}
for apa, name in [(1,'ProtoDUNE_HD_APA_maps_APA1_104.py'),
                  (2,'ProtoDUNE_HD_APA_maps.py')]:
    endpoint = 104 if apa == 1 else 109
    expected = [[(endpoint,c) for c in row] for row in source_rows[apa]]
    assert read_map(name, apa) == expected, f'APA{apa}: source-map mismatch'
    extracted = load(f'apa1-apa2-response-20261103/apa{apa}-extracted.json')
    assert extracted['order'] == [list(c) for row in expected for c in row]
    assert len({c for row in expected for c in row}) == 40
    orientation[str(apa)] = {'endpoint': endpoint, 'rows_top_to_bottom_left_to_right': source_rows[apa],
                            'matches_analysis_map_and_extracted_order': True}
assert digest(SOURCE_PDF) == '6ff093fe51ee692a33e83718e18abca19840d100d0dd95dec760df78bf50bb54'

inventory = list(csv.DictReader((ANALYSIS/'all-runs/all-runs-summary.csv').open()))
records = sum(int(r['local_events']) for r in inventory)
candidates = sum(int(r['charge_screen_candidates']) for r in inventory)
early = sum(int(r['sharp_PDS_candidate_seen']) for r in inventory)
assert (records,candidates,early) == (1531,1516,1179)
assert sum(int(r['full_4ms_precoverage_events']) for r in inventory) == 0
pairs = load('double-pulse-display/results.json')
assert (pairs['events_with_two_or_more_candidates_in_window'],pairs['local_charge_shakes']) == (101,716)
modules = load('apa1-apa2-response-20261103/module-results.json')
for apa, strongest, n, total in [('1',{3,4},39,49),('2',{1,2},1210,1224)]:
    profile = modules['APA'][apa]['precursor'][0]
    assert profile['events'] == total
    assert sum(m['largest_events'] for m in profile['modules'] if m['module'] in strongest) == n
first = load('module-first-histogram-20261104/results.json')
assert (first['APA']['1']['primary']['tied_events'],first['APA']['1']['primary']['events']) == (12,14)
assert (first['APA']['2']['primary']['tied_events'],first['APA']['2']['primary']['events']) == (280,478)
values = {'records':records, 'candidates':candidates, 'early':early,
          'doubleRecords':101, 'doubleTotal':716}
(HERE/'values.tex').write_text(''.join(f'\\newcommand{{\\{k}}}{{{v:,}}}\n' for k,v in values.items()))

sources = [
 'all-runs/all-runs-summary.csv', 'all-runs/README.txt',
 'double-pulse-display/results.json', 'double-pulse-display/README.txt',
 'pds-shake-timing-20261028/results.json',
 'electrical-pattern-20261023/results.json', 'electrical-pattern-20261023/README.txt',
 'charge-light-matching/event-mixing-results.json',
 'charge-light-matching/interpretation-20261028.json',
 'apa1-apa2-response-20261103/module-results.json',
 'apa1-apa2-response-20261103/apa1-extracted.json',
 'apa1-apa2-response-20261103/apa2-extracted.json',
 'afe-comparison-20261103/results.json', 'afe-comparison-20261103/README.txt',
 'module-first-histogram-20261104/results.json', 'module-first-histogram-20261104/README.txt',
 'sc-correlation-20261027/README.txt',
 'detector-landmarks-20261103/README.txt',
 'first-pass/ProtoDUNE_HD_APA_maps_APA1_104.py', 'first-pass/ProtoDUNE_HD_APA_maps.py',
]
manifest = {
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'purpose':'Two-page plain-language summary of existing ground-shake analyses; no new raw-data analysis.',
 'source_revision': subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
 'source_worktree':subprocess.check_output(['git','status','--short'],cwd=REPO,text=True),
 'host':platform.node(), 'python':platform.python_version(),
 'command':'python3 reports/ground_shakes_nov2026/build_report.py',
 'acceptance':{'inventory_counts':True,'reported_pair_count':True,'module_activity_counts':True,
               'latest_timing_counts_including_M8':True,'all_80_channel_positions_match_source_transcription':True},
 'orientation':orientation,
 'orientation_review':{'source':'EDMS 3493627 v1','pages':[18,20,21],
  'APA2_field_cage_side':'Right in source view; top-right channel 109:20.',
  'photo':'Page 18 explicitly says picture left-right flipped to match plots.',
  'not_physical':'Page 21 intentionally reorders APA1 into APA2 electronics order.',
  'limits':'Historical In Work presentation; no current as-built or beam/compass registration established. July APA1 wiring differs. No engineering approval.'},
 'inputs':[{'path':str(p),'sha256':digest(p)} for p in [SOURCE_PDF,*[ANALYSIS/s for s in sources],HERE/'build_report.py',HERE/'main.tex']],
 'reviewer':None,
}
path=HERE/('evidence-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json')
path.write_text(json.dumps(manifest,indent=2)+'\n')
print('Checked inventory, counts and all 80 historical channel positions. Wrote',path.name)
