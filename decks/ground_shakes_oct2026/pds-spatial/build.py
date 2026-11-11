"""Show existing APA2 PDS snapshots and section histories. No raw-data decoding."""
from pathlib import Path
import csv
import datetime as dt
import hashlib
import json
import platform
import subprocess

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LogNorm, Normalize, ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle, Patch
from matplotlib.ticker import MaxNLocator

HERE = Path(__file__).resolve().parent
DISC = {11, 13, 14, 16}
STAGES = [('Early pulse 1', 'First pulse'), ('Early pulse 2', 'Second pulse'),
          ('Before slow precursor', 'Before slow rise'),
          ('Precursor interval', 'Slow precursor'), ('Main shake', 'Main shake'),
          ('After shake', 'After shake')]
INK, BLUE, ORANGE, GRAY = '#1C2834', '#304E62', '#DE6126', '#D5D9DD'
CMAP = plt.get_cmap('Blues')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                    'text.color': INK, 'axes.labelcolor': INK,
                    'axes.spines.top': False, 'axes.spines.right': False,
                    'pdf.fonttype': 42, 'savefig.facecolor': 'white'})


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stages(event):
    return [(next(s for s in event['stages'] if s['label'] == label), title)
            for label, title in STAGES]


def arrays(event, stage):
    ch = np.array([c for _, c in event['order']])
    v = np.array(stage['signed_median_ADC'], float)
    good = np.isfinite(v) & ~np.array(stage['rail_observed'])
    connected = ~np.isin(ch, list(DISC))
    return ch, v, good, connected


def sections(v, good, connected):
    size, count, best_ch_index = [], [], []
    for m in range(10):
        inds = np.arange(4*m, 4*m+4)
        valid = inds[good[inds] & connected[inds]]
        count.append(len(valid))
        if len(valid):
            i = int(valid[np.argmax(np.abs(v[valid]))])
            size.append(float(abs(v[i])))
            best_ch_index.append(i)
        else:
            size.append(np.nan)
            best_ch_index.append(None)
    return np.array(size), np.array(count), best_ch_index


def upper_limit(values):
    top = max(float(np.nanmax(values)), 1.)
    ticks = MaxNLocator(nbins=3, steps=[1, 2, 3, 5, 10]).tick_values(0, top)
    return float(ticks[-1])


def header(fig, title, event, subtitle):
    fig.text(.045, .95, title, fontsize=25, weight='bold')
    fig.text(.045, .912, f"APA2 · Run {event['run']}, event {event['event']} · DAPHNE 109", fontsize=15)
    fig.text(.045, .875, subtitle, fontsize=13)


def map_page(event):
    fig = plt.figure(figsize=(19.2, 10.8))
    header(fig, 'Where the PDS response appears', event,
           'One box per channel, in physical module order. Numbers are channel IDs; time 0 is the main-shake marker.')
    fig.text(.045, .842, 'Field-cage corner: top right of every map, beside channel 20.', fontsize=11, color=BLUE)
    left, width, gap, bottom, height = .075, .137, .015, .31, .45
    for n, (stage, title) in enumerate(stages(event)):
        ch, v, good, connected = arrays(event, stage)
        vmax = upper_limit(np.abs(v[good]))
        norm = Normalize(0, vmax)
        ax = fig.add_axes([left+n*(width+gap), bottom, width, height])
        ax.set(xlim=(-.5, 3.5), ylim=(9.5, -.5))
        ax.set_xticks([])
        ax.set_yticks(range(10), [f'M{i+1}' for i in range(10)] if n == 0 else [])
        ax.tick_params(length=0)
        if n == 0:
            ax.set_ylabel('Physical section (PDS module)', labelpad=12)
        ax.set_title(f'{title}\n{stage["center_us"]:+.1f} µs', fontsize=15, pad=22)
        valid = np.flatnonzero(good & connected)
        peak = int(valid[np.argmax(abs(v[valid]))]) if len(valid) else None
        for i, channel in enumerate(ch):
            x, y = i % 4, i // 4
            color = CMAP(norm(abs(v[i]))) if good[i] else GRAY
            ax.add_patch(Rectangle((x-.5, y-.5), 1, 1, facecolor=color,
                                  edgecolor='#9CA7B0', lw=.6,
                                  hatch='///' if channel in DISC else None))
            ax.text(x, y, str(channel), ha='center', va='center', fontsize=12,
                    color='white' if good[i] and abs(v[i]) > .6*vmax else INK,
                    weight='bold' if i == peak else 'normal')
            if i == peak:
                ax.add_patch(Rectangle((x-.46, y-.46), .92, .92, fill=False,
                                      edgecolor=ORANGE, lw=3))
        cax = fig.add_axes([left+n*(width+gap), .277, width, .012])
        cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=CMAP), cax=cax,
                          orientation='horizontal', ticks=[0, vmax/2, vmax])
        cb.ax.tick_params(labelsize=10, length=3)
        cb.set_label('Signal size (ADC counts)', fontsize=10, labelpad=3)
        fig.text(left+n*(width+gap)+width/2, .202,
                 f'Largest connected: ch {ch[peak]}\n{abs(v[peak]):g} ADC counts',
                 ha='center', fontsize=11)
        fig.text(left+n*(width+gap)+width/2, .174,
                 f'{len(valid)}/36 connected recorded', ha='center', fontsize=11,
                 weight='bold' if len(valid) < 8 else 'normal')
    fig.legend(handles=[Patch(facecolor=GRAY, label='Missing / insufficient samples'),
                        Patch(facecolor='white', edgecolor=INK, hatch='///', label='Reported disconnected'),
                        Patch(facecolor='white', edgecolor=ORANGE, lw=2, label='Largest recorded connected channel')],
               loc='lower center', bbox_to_anchor=(.52, .108), ncol=3, frameon=False, fontsize=12)
    fig.text(.045, .086, 'Each panel has its own colour scale. Signal size is the distance from baseline; pulse sign is ignored.', fontsize=12)
    fig.text(.045, .057, 'Grey does not mean quiet. Sparse coverage before the slow rise and after the shake prevents a full spatial comparison.', fontsize=12)
    fig.text(.045, .026, 'Each snapshot: 0.512 µs. Uncalibrated ADC counts, not photons. Layout: EDMS 3493627 v1, p. 18; not metric coordinates.', fontsize=10, color=BLUE)
    return fig


def bar_page(event):
    fig = plt.figure(figsize=(19.2, 10.8))
    header(fig, 'Which physical section has the largest recorded signal?', event,
           'Each bar is the largest connected-channel signal in that module. Labels give recorded channels out of four.')
    for k, (stage, title) in enumerate(stages(event)):
        ch, v, good, connected = arrays(event, stage)
        vals, counts, best = sections(v, good, connected)
        row, col = divmod(k, 3)
        ax = fig.add_axes([.075+col*.315, .545-row*.365, .273, .245])
        x = np.arange(1, 11)
        top = upper_limit(vals)*1.18
        ax.set(xlim=(.4, 10.6), ylim=(0, top), xticks=x)
        if row == 1:
            ax.set_xlabel('Physical section (module M1 to M10)')
        if col == 0:
            ax.set_ylabel('Signal size (ADC counts)')
        ax.set_title(f'{title} · {stage["center_us"]:+.1f} µs', loc='left', fontsize=16, pad=12)
        for j in range(10):
            if j == 7:
                ax.axvspan(j+.58, j+1.42, facecolor='white', edgecolor='#AAB2B8', hatch='///', lw=0)
                ax.text(j+1, top*.05, 'disc.', rotation=90, va='bottom', ha='center', fontsize=10)
            elif not counts[j]:
                ax.axvspan(j+.58, j+1.42, color=GRAY, zorder=0)
                ax.text(j+1, top*.05, '0/4', rotation=90, va='bottom', ha='center', fontsize=10)
            else:
                color = ORANGE if vals[j] == np.nanmax(vals) else BLUE
                ax.bar(j+1, vals[j], .7, color=color, zorder=3)
                ax.text(j+1, vals[j]+top*.025, f'{counts[j]}/4', ha='center', va='bottom', fontsize=10)
        ax.grid(axis='y', color='#E7EBEE', zorder=0)
        ax.yaxis.set_major_locator(MaxNLocator(4))
    fig.text(.045, .105, 'Compare the bar shapes to see which sections dominate. Vertical scales differ so the small precursor remains visible.', fontsize=12)
    fig.text(.045, .075, 'M8 contains the four reported disconnected channels and is shown separately in the channel maps. Grey means no usable channel.', fontsize=12)
    fig.text(.045, .045, 'A maximum is not a sum or an integral. Fewer recorded channels can hide a stronger response; these bars do not measure total light.', fontsize=12)
    fig.text(.045, .02, 'Module order follows the physical APA2 map. Snapshots are 0.512 µs wide; signal size is |ADC − baseline|.', fontsize=10, color=BLUE)
    return fig


def section_history(event, data):
    key = f'r{event["run"]}_e{event["event"]}'
    v, rails = data[key+'_adc'], data[key+'_rails']
    ch = np.array([c for _, c in event['order']])
    good = np.isfinite(v) & ~rails & (data[key+'_coverage'] >= 26)
    connected = ~np.isin(ch, list(DISC))
    size = np.full((10, v.shape[1]), np.nan)
    counts = np.zeros((10, v.shape[1]), int)
    for m in range(10):
        inds = np.arange(m*4, m*4+4)
        mask = good[inds] & connected[inds, None]
        counts[m] = mask.sum(axis=0)
        size[m] = np.max(np.where(mask, abs(v[inds]), -np.inf), axis=0)
        size[m, counts[m] == 0] = np.nan
    return size, counts


def history_page(event, data):
    fig = plt.figure(figsize=(19.2, 10.8))
    header(fig, 'Follow the recorded response through APA2', event,
           'Top: largest connected-channel signal in each physical section. Bottom: channels with usable samples.')
    t = data['time_us']
    size, counts = section_history(event, data)
    edges = np.r_[t-.256, t[-1]+.256]
    yedges = np.arange(.5, 11.5)
    ax = fig.add_axes([.085, .43, .81, .35])
    cov = fig.add_axes([.085, .195, .81, .16], sharex=ax)
    cmap = plt.get_cmap('magma').copy()
    cmap.set_bad(GRAY)
    im = ax.pcolormesh(edges, yedges, np.maximum(size, 1), cmap=cmap,
                       norm=LogNorm(1, 16000), rasterized=True, shading='flat')
    ccmap = ListedColormap([GRAY, '#E2EDF5', '#B2CFDF', '#729BB6', BLUE])
    cim = cov.pcolormesh(edges, yedges, counts, cmap=ccmap,
                         norm=BoundaryNorm(np.arange(-.5, 5.5), 5), rasterized=True)
    for axis in [ax, cov]:
        axis.set(xlim=(-320, 80), ylim=(10.5, .5), yticks=np.arange(1, 11),
                 yticklabels=[f'M{i}' for i in range(1, 11)])
        axis.set_ylabel('Physical section')
        axis.axhspan(7.5, 8.5, facecolor='#FAFAFA', edgecolor='#8D969D', hatch='///', lw=0, zorder=4)
        axis.text(-315, 8, 'M8: disconnected', fontsize=10, va='center', zorder=5)
        axis.axvline(0, color='#39A6B9', lw=1.8)
        for stage, _ in stages(event):
            axis.axvline(stage['center_us'], color='#648694', lw=.6, alpha=.65)
    ax.tick_params(labelbottom=False)
    for label, short in [('Early pulse 1', 'Pulse 1'), ('Early pulse 2', 'Pulse 2'),
                         ('Precursor interval', 'Precursor'), ('Main shake', 'Main'), ('After shake', 'After')]:
        stage = next(s for s in event['stages'] if s['label'] == label)
        ax.text(stage['center_us'], 1.02, short, transform=ax.get_xaxis_transform(),
                ha='center', va='bottom', fontsize=11)
    cov.set_xlabel('Time from the main-shake marker (µs)')
    ca = fig.add_axes([.914, .43, .012, .35])
    cb = fig.colorbar(im, cax=ca, ticks=[1, 10, 100, 1000, 10000])
    cb.ax.set_yticklabels(['≤1', '10', '100', '1,000', '10,000'])
    cb.set_label('Signal size (ADC counts; logarithmic scale)')
    ca2 = fig.add_axes([.914, .195, .012, .16])
    cb2 = fig.colorbar(cim, cax=ca2, ticks=np.arange(5))
    cb2.set_label('Channels / 4')
    fig.text(.045, .11, 'Bright bands show large recorded signals. Read them with the coverage panel: a gap cannot show where the signal went.', fontsize=12)
    fig.text(.045, .078, 'The colour scale is fixed over time. The logarithmic scale makes both the small precursor and the large shake visible.', fontsize=12)
    fig.text(.045, .046, 'These are changes in the recorded spatial pattern, not a measured path of a moving source. ADC counts are not calibrated light.', fontsize=12)
    fig.text(.045, .019, 'Existing 0.512 µs channel medians; ≥26 of 32 native samples required. No interpolation. Rail-flagged bins excluded.', fontsize=10, color=BLUE)
    return fig


def main():
    record = json.loads((HERE/'input-snapshots.json').read_text())
    data = np.load(HERE/'input-time-series.npz')
    checks, rows, channel_rows, history_arrays, outputs = [], [], [], {}, []
    with PdfPages(HERE/'apa2-pds-sections.pdf') as pdf:
        for event in record['events']:
            for kind, make in [('physical-map', lambda: map_page(event)),
                               ('section-bars', lambda: bar_page(event)),
                               ('section-time', lambda: history_page(event, data))]:
                fig = make()
                stem = f'run{event["run"]}_event{event["event"]}_{kind}'
                for ext in ['pdf', 'png']:
                    path = HERE/f'{stem}.{ext}'
                    fig.savefig(path, dpi=170)
                    outputs.append(path)
                pdf.savefig(fig)
                plt.close(fig)
            size, counts = section_history(event, data)
            key = f'r{event["run"]}_e{event["event"]}'
            history_arrays[key+'_maximum_ADC'] = size
            history_arrays[key+'_recorded_channels'] = counts
            assert np.all(np.isnan(size[counts == 0]))
            assert np.all(counts[7] == 0)
            for stage, title in stages(event):
                ch, v, good, connected = arrays(event, stage)
                sizes, count, best = sections(v, good, connected)
                for i in range(40):
                    channel_rows.append({'run':event['run'], 'event':event['event'], 'stage':title,
                        'time_us':stage['center_us'], 'module':i//4+1, 'channel':int(ch[i]),
                        'signed_ADC':float(v[i]) if np.isfinite(v[i]) else '',
                        'coverage_fraction':stage['coverage_fraction'][i],
                        'rail_flag':stage['rail_observed'][i], 'reported_disconnected':not bool(connected[i])})
                for m in range(10):
                    rows.append({'run':event['run'], 'event':event['event'], 'stage':title,
                                 'time_us':stage['center_us'], 'module':m+1,
                                 'largest_recorded_connected_ADC':float(sizes[m]) if count[m] else '',
                                 'recorded_connected_channels':int(count[m]),
                                 'connected_channels_in_module':0 if m == 7 else 4,
                                 'largest_channel':int(ch[best[m]]) if best[m] is not None else ''})
            checks.append({'run':event['run'], 'event':event['event'],
                           'missing_sections_remain_missing':True, 'disconnected_M8_excluded_from_section_values':True})
    outputs.append(HERE/'apa2-pds-sections.pdf')
    history_arrays['time_us'] = data['time_us']
    np.savez_compressed(HERE/'section-time-values.npz', **history_arrays)
    for name, values in [('section-values.csv', rows), ('channel-values.csv', channel_rows)]:
        with (HERE/name).open('w') as f:
            writer = csv.DictWriter(f, fieldnames=list(values[0]))
            writer.writeheader()
            writer.writerows(values)
    now = dt.datetime.now(dt.timezone.utc)
    repo = HERE.parents[2]
    evidence = {'created_utc':now.isoformat(), 'question':'Where does the recorded APA2 PDS response appear and how does its distribution change?',
                'command':'python3 build.py', 'cwd':str(HERE), 'host':platform.node(),
                'python':platform.python_version(), 'numpy':np.__version__, 'matplotlib':matplotlib.__version__,
                'git_head':subprocess.check_output(['git','rev-parse','HEAD'], cwd=repo, text=True).strip(),
                'git_status':subprocess.check_output(['git','status','--short'], cwd=repo, text=True),
                'input_sha256':{str(HERE/n):digest(HERE/n) for n in ['build.py','input-snapshots.json','input-time-series.npz','input-time-series-source.json']},
                'output_sha256':{p.name:digest(p) for p in outputs}, 'checks':checks,
                'metric':'Maximum absolute baseline-subtracted recorded nonrail connected-channel median per physical module. Not a sum, integral or photon yield.',
                'selection':'Two existing user-selected APA2 examples; six existing snapshots per event plus existing 512 ns time series.',
                'limits':record['limits']+['Section maxima depend on channel coverage; the companion coverage panel is required.',
                                          'No propagation direction or source location is fitted. No across-event spatial population claim.'],
                'reviewer':None}
    path = HERE/f'evidence-{now.strftime("%Y%m%dT%H%M%S%fZ")}.json'
    path.write_text(json.dumps(evidence, indent=2)+'\n')
    print('Built 6-page APA2 supplement, 6 PNG figures and exact channel/section values.')
    print(path)


if __name__ == '__main__':
    main()
