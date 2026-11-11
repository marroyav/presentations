"""Freeze the completed electrical results and the 27 October SC extension."""
from pathlib import Path
import hashlib
import json
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ANALYSIS=HERE.parents[2]/'ground-shake-data/analysis'
EVIDENCE=HERE/'evidence'
FIGURES=HERE/'figures'


def main():
    sources={}
    for source,name in [
        ('electrical-pattern-20261023/results.json','electrical-fit-results.json'),
        ('electrical-pattern-20261023/sequence-results.json','electrical-sequence-results.json'),
        ('sc-correlation-20261027/report-data.json','SC-report-data.json'),
        ('sc-correlation-20261027/summary.json','SC-summary.json'),
        ('sc-correlation-20261027/plan.json','SC-plan.json'),
        ('sc-correlation-20261027/previous-results-audit.json','previous-results-audit.json'),
    ]:
        p=ANALYSIS/source;shutil.copy2(p,EVIDENCE/name)
        sources[source]=hashlib.sha256(p.read_bytes()).hexdigest()
    for ext in ['pdf','png']:
        p=ANALYSIS/f'sc-correlation-20261027/SC-replication.{ext}'
        shutil.copy2(p,FIGURES/f'09-SC-correlation.{ext}')
        sources[str(p.relative_to(ANALYSIS))]=hashlib.sha256(p.read_bytes()).hexdigest()
    data=json.loads((EVIDENCE/'electrical-fit-results.json').read_text())
    get=lambda train:next(r for r in data['summary']if r['split']=='other_run' and r['trained_region']==train
                         and r['tested_region']=='early' and r['model']=='FIR3')
    early,main_fit=get('early'),get('main')
    colors=json.loads((HERE.parents[1]/'templates/dune-professional/design-tokens.json').read_text())['colors']
    c=lambda name:colors[name]['hex']
    blue,orange,ink,gray=c('editorial-muted'),c('editorial-accent-deep'),c('editorial-text'),c('border')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':18,'axes.labelsize':18,'axes.titlesize':19,
                         'xtick.labelsize':17,'ytick.labelsize':17,'text.color':ink,'axes.labelcolor':ink,
                         'axes.edgecolor':gray,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    outputs={}
    def save(fig,name):
        for ext in ['pdf','png']:
            p=FIGURES/f'{name}.{ext}';fig.savefig(p,dpi=180);outputs[str(p.relative_to(HERE))]=hashlib.sha256(p.read_bytes()).hexdigest()
        plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(13,3.8),layout='constrained')
    errors=np.sqrt(1-np.array([early['paired_actual_skill'],early['paired_shuffled_skill']]))
    bars=axs[0].bar([0,1],errors,.55,color=[blue,orange]);axs[0].bar_label(bars,fmt='%.3f',padding=4,fontsize=19)
    axs[0].axhline(1,color=gray,lw=1,ls=':');axs[0].set_xticks([0,1],['Real reference\ninputs','Inputs from\nother events'])
    axs[0].set(title='Run 32739 · lower error is better',ylabel='Relative edge error',ylim=(0,1.3))
    values=[early['pooled_predictive_skill'],main_fit['pooled_predictive_skill']]
    bars=axs[1].bar([0,1],values,.55,color=[blue,orange]);axs[1].bar_label(bars,labels=[f'{v:.3f}'for v in values],padding=4,fontsize=19)
    axs[1].axhline(0,color=gray,lw=1);axs[1].set_xticks([0,1],['Fit from\nearly pulses','Fit from\nmain shakes'])
    axs[1].set(title='Both fits tested on early pulses',ylabel='Prediction score',ylim=(-.32,.36))
    save(fig,'07-cross-run-electrical')
    channels=np.array([10*a+c for a in range(5)for c in range(8)])
    selected=[12,15,40,42,20,22,24];x=np.array([0,1,3,4,6,7,8])
    values=[early['channel_skill'][int(np.flatnonzero(channels==ch)[0])]for ch in selected]
    fig,ax=plt.subplots(figsize=(13,3.8),layout='constrained')
    bars=ax.bar(x,values,.64,color=[blue]*4+[orange]*3)
    ax.bar_label(bars,labels=[f'{v:.2f}'for v in values],padding=4,fontsize=18)
    ax.set_xticks(x,[str(ch)for ch in selected]);ax.set(xlabel='DAPHNE input',ylabel='Prediction score',ylim=(0,.95))
    for center,label in [(.5,'AFE 1'),(3.5,'AFE 4'),(7,'AFE 2')]:ax.text(center,.87,label,ha='center',fontsize=20)
    save(fig,'08-electronics-groups')
    manifest={'source_root':str(ANALYSIS),'source_sha256':sources,'figure_sha256':outputs,
              'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'meaning':'Prediction score = 1 minus squared edge error / observed squared edge size. Not an optical/electrical fraction.'}
    (EVIDENCE/'extension-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Added cross-run electrical, channel-group and SC figures.')


if __name__=='__main__':main()
