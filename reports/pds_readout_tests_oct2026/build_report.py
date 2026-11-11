"""Generate the report tables from the recorded results; no DAQ access."""
from pathlib import Path
import json
r=Path(__file__).resolve().parent
a=json.loads((r/'evidence/measurements.json').read_text())
lines=[]
for points in zip(*(a['baseline'][k]['rows'] for k in ['v56','v571','v56raw4'])):
 assert len({p['actual_rate_hz'] for p in points})==1
 rate=points[0]['actual_rate_hz']/1000
 lines.append(f'{rate:.3f} & '+' & '.join(f"{p['incoming_loss_pct']:.3f}" for p in points)+r' \\')
(r/'incoming.tex').write_text('\n'.join(lines)+'\n'+chr(92)+'bottomrule\n')
lines=[]
for points in zip(*(a['baseline'][k]['rows'] for k in ['v56','v571','v56raw4'])):
 lines.append(f"{points[0]['actual_rate_hz']/1000:.3f} & "+' & '.join(f"{p['selected_window_loss_pct']:.3f}" for p in points)+r' \\')
(r/'windows.tex').write_text('\n'.join(lines)+'\n'+chr(92)+'bottomrule\n')
labels={'timing571off':'Inline; probes off','timing571on':'Inline; probes on','timing571raw4':'4 raw + 4 TP; probes on','steady571off':'Continuous; probes off','steady571on':'Continuous; probes on'}
lines=[]
for tag,b in a['instrumented'].items():
 for p in b['points']:
  lines.append(f"{b['run']} & {labels[tag]} & {p['actual_rate_hz']/1000:.3f} & {p['loss_pct']:.3f} & {p['selected_loss_pct']:.3f} & {p['nic_missed_packets']:,}"+r' \\')
(r/'instrumented.tex').write_text('\n'.join(lines)+'\n'+chr(92)+'bottomrule\n')
# Every case must have finished decoding before this report is built.
assert all(not b['decode_errors'] for b in a['baseline'].values())
assert all(not b['decode_errors'] for b in a['instrumented'].values())
print('Generated three result tables from eight validated runs.')
