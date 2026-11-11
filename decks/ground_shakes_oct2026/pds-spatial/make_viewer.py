"""Create a self-contained player for the existing APA2 channel and section data."""
from pathlib import Path
import json
import hashlib
import numpy as np

HERE=Path(__file__).resolve().parent
TEMPLATE=r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>APA2 PDS activity by section</title>
<style>
*{box-sizing:border-box}body{font:16px Arial,"DejaVu Sans",sans-serif;color:#1c2834;max-width:1400px;margin:25px auto;padding:0 24px;background:white}
h1{font-size:30px;margin:0 0 8px}p{line-height:1.5;margin:8px 0}a{color:#205f91}nav,.controls,.stages{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:16px 0}
button,select{font:inherit;padding:8px 12px;background:#f3f6f8;border:1px solid #8195a3;border-radius:3px;cursor:pointer}button:focus,select:focus,input:focus{outline:3px solid #de6126}
#play{background:#304e62;color:white;min-width:80px}#time{flex:1;min-width:220px}#clock{font-size:24px;font-variant-numeric:tabular-nums;min-width:155px}
svg{width:100%;height:auto;display:block;border:1px solid #ced9e1}small{color:#304e62}.note{background:#eff5fa;padding:10px 14px;margin:14px 0}#status{font-weight:600;min-height:24px}
.stages button{font-size:14px}.downloads{padding:16px 0;border-top:1px solid #ced9e1}.legend{display:flex;gap:22px;flex-wrap:wrap;margin:12px 0;font-size:14px}
.swatch{display:inline-block;width:24px;height:16px;border:1px solid #8f9ca5;margin-right:6px;vertical-align:middle}
</style>
<h1>Follow PDS activity through APA2</h1>
<p>The map shows individual channels. The bars show the largest recorded connected-channel signal in each physical section.</p>
<p><a href="population/viewer.html"><strong>Compare all available APA2 events: histograms and M6-to-corner checks</strong></a></p>
<p><a href="apa1-comparison/viewer.html">Compare APA1 and APA2: physical positions, electronics order and first response</a></p>
<nav><label>Event <select id="event"></select></label><button id="play">Play</button><button id="back" aria-label="Previous frame">←</button><button id="next" aria-label="Next frame">→</button>
<label>Speed <select id="speed"><option value="100">Slow</option><option value="50" selected>Normal</option><option value="25">Fast</option></select></label>
<a href="../../../../ground-shake-data/analysis/whole-event-spatial/viewer.html">Original viewer: APA1 and APA2</a></nav>
<div class="controls"><input id="time" type="range" min="0" max="1" step="1" aria-label="Time from main shake"><strong id="clock"></strong></div>
<div class="stages" id="stages"></div><p id="status"></p>
<svg id="display" viewBox="0 0 1200 720" role="img" aria-label="Physical APA2 channel map and bars for ten PDS modules"></svg>
<div class="legend"><span><i class="swatch" style="background:#d5d9dd"></i>Missing or excluded samples, not zero signal</span><span><i class="swatch" style="background:repeating-linear-gradient(135deg,#fff,#fff 3px,#84939c 4px,#fff 5px)"></i>Reported disconnected</span><span><i class="swatch" style="border:3px solid #de6126"></i>Largest recorded connected channel</span></div>
<p class="note">The colour scale stays fixed during playback. Signal size is the distance from baseline, in ADC counts. It is not calibrated light. Bars use a logarithmic scale so small and large signals remain visible.</p>
<p>Each frame spans 0.512 µs. Grey cells have missing or excluded samples. R marks an extreme digitiser code; these bins are excluded. We do not fill gaps. A changing pattern does not establish that a source moves.</p>
<small>Module layout: EDMS 3493627 v1, p. 18. Field-cage corner is beside channel 20. Time 0 is the TPC main-shake marker. Module 8 contains reported disconnected channels 11, 13, 14 and 16.</small>
<div class="downloads"><a href="apa2-pds-sections.pdf">All maps and section histograms (PDF)</a> · <a id="mapfile">Current event: physical map</a> · <a id="timefile">Current event: section history</a> · <a href="leading-channels.pdf">Which channels lead?</a></div>
<script>
const DATA=__DATA__, $=id=>document.getElementById(id), disc=new Set([11,13,14,16]), times=DATA.time;
let index=0,timer=null,playing=false,snapshot=null;
const lo=times.findIndex(t=>t>=-320), hi=times.findLastIndex(t=>t<=80);
$('time').min=lo;$('time').max=hi;
DATA.events.forEach((e,i)=>$('event').add(new Option('Run '+e.run+' · event '+e.event,i)));
function current(){return DATA.events[Number($('event').value)]}
function nearest(t){let best=lo;for(let i=lo+1;i<=hi;i++)if(Math.abs(times[i]-t)<Math.abs(times[best]-t))best=i;return best}
function stop(){clearTimeout(timer);timer=null;playing=false;$('play').textContent='Play'}
function draw(){
 const e=current(), values=snapshot?snapshot.values.map((v,i)=>snapshot.rails[i]?null:v):e.values.map((row,i)=>e.rails[i][index]?null:row[index]), good=[];
 values.forEach((v,i)=>{if(v!==null&&!disc.has(e.channels[i]))good.push(i)});
 const peak=good.length?good.reduce((a,b)=>Math.abs(values[a])>=Math.abs(values[b])?a:b):null;
 const scaled=v=>Math.min(1,Math.max(0,Math.log10(Math.max(1,Math.abs(v)))/Math.log10(16000)));
 const colour=v=>{if(v===null)return '#d5d9dd';const x=scaled(v);return `rgb(${Math.round(245-210*x)},${Math.round(249-171*x)},${Math.round(252-154*x)})`};
 let s='<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="10" height="10"><path d="M-2,2L2,-2M0,10L10,0M8,12L12,8" stroke="#84939c" stroke-width="1.2"/></pattern></defs>';
 const text=(x,y,t,size=16,anchor='start',fill='#1c2834',weight='normal')=>`<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="${fill}" font-weight="${weight}">${t}</text>`;
 s+=text(70,32,'Physical APA2 layout',23)+text(650,32,'Largest signal in each section',23);
 s+=text(70,58,'Each cell: channel number and signal size (ADC counts)',14)+text(650,58,'Connected channels only · M1 to M10',14);
 s+=text(515,85,'Field-cage corner ↓',13,'end');
 const left=70,top=100,cw=112,ch=50,bx=650,bw=390;
 for(let i=0;i<40;i++){
  const col=i%4,row=Math.floor(i/4),x=left+col*cw,y=top+row*ch,v=values[i],id=e.channels[i],dark=v!==null&&scaled(v)>.65;
  s+=`<rect x="${x}" y="${y}" width="${cw}" height="${ch}" fill="${colour(v)}" stroke="#9eacb5"/>`;
  if(disc.has(id))s+=`<rect x="${x}" y="${y}" width="${cw}" height="${ch}" fill="url(#hatch)"/>`;
  s+=text(x+cw/2,y+20,'ch '+id,15,'middle',dark?'white':'#1c2834');
  const flagged=snapshot?snapshot.rails[i]:e.rails[i][index];
  s+=text(x+cw/2,y+40,v===null?(flagged?'R':'—'):Math.abs(v).toFixed(1),15,'middle',dark?'white':'#1c2834','bold');
  if(i===peak)s+=`<rect x="${x+2}" y="${y+2}" width="${cw-4}" height="${ch-4}" fill="none" stroke="#de6126" stroke-width="4"/>`;
 }
 for(let m=0;m<10;m++){
  const y=top+m*ch,ids=[4*m,4*m+1,4*m+2,4*m+3].filter(i=>good.includes(i));
  s+=text(57,y+31,'M'+(m+1),17,'end')+text(bx-12,y+31,'M'+(m+1),17,'end');
  if(m===7){s+=`<rect x="${bx}" y="${y+8}" width="${bw}" height="34" fill="url(#hatch)"/>`+text(bx+10,y+31,'Disconnected inputs',15);continue}
  if(!ids.length){s+=`<rect x="${bx}" y="${y+8}" width="${bw}" height="34" fill="#d5d9dd"/>`+text(bx+10,y+31,'No recorded channel',15)+text(1150,y+31,'0/4',15,'end');continue}
  const best=ids.reduce((a,b)=>Math.abs(values[a])>=Math.abs(values[b])?a:b),v=Math.abs(values[best]);
  s+=`<rect x="${bx}" y="${y+8}" width="${Math.max(1,scaled(v)*bw)}" height="34" fill="${best===peak?'#de6126':'#304e62'}"/>`;
  s+=text(1150,y+22,v.toFixed(1)+' ADC',14,'end')+text(1150,y+40,ids.length+'/4 recorded',12,'end');
 }
 for(const val of [1,10,100,1000,10000]){const x=bx+scaled(val)*bw;s+=`<path d="M${x},605v7" stroke="#304e62"/>`+text(x,632,val.toLocaleString(),13,'middle')}
 s+=text(bx+bw/2,659,'Signal size (ADC counts; logarithmic scale)',14,'middle');
 for(let k=0;k<160;k++){const value=Math.pow(16000,k/159);s+=`<rect x="${70+k*2.8}" y="630" width="3" height="15" fill="${colour(value)}"/>`}
 for(const val of [1,10,100,1000,10000])s+=text(70+scaled(val)*448,665,val.toLocaleString(),13,'middle');
 s+=text(294,695,'Fixed colour scale (ADC counts)',14,'middle');
 $('display').innerHTML=s;$('time').value=index;$('clock').textContent=(snapshot?snapshot.time:times[index]).toFixed(3)+' µs';
 $('status').textContent=good.length+'/36 connected channels have usable samples'+(peak===null?'':'; largest recorded signal: channel '+e.channels[peak]+', module M'+(Math.floor(peak/4)+1))+'.';
}
function load(){stop();const e=current();$('stages').replaceChildren();
 e.stages.forEach(stage=>{const b=document.createElement('button');b.textContent=stage.title+' ('+stage.time.toFixed(1)+' µs)';b.onclick=()=>{stop();index=nearest(stage.time);snapshot=stage;draw()};$('stages').append(b)});
 const stem='run'+e.run+'_event'+e.event;$('mapfile').href=stem+'_physical-map.png';$('timefile').href=stem+'_section-time.png';index=lo;snapshot=null;draw();
}
function tick(){if(!playing)return;if(index>=hi){stop();return}snapshot=null;index++;draw();const atStage=current().stages.some(s=>nearest(s.time)===index);timer=setTimeout(tick,atStage?650:Number($('speed').value))}
$('event').onchange=load;$('time').oninput=()=>{stop();snapshot=null;index=Number($('time').value);draw()};
$('play').onclick=()=>{if(playing){stop();return}if(index>=hi)index=lo;playing=true;$('play').textContent='Pause';tick()};
$('back').onclick=()=>{stop();snapshot=null;index=Math.max(lo,index-1);draw()};$('next').onclick=()=>{stop();snapshot=null;index=Math.min(hi,index+1);draw()};
document.addEventListener('keydown',ev=>{if(ev.key==='ArrowLeft'||ev.key==='ArrowRight'){ev.preventDefault();$(ev.key==='ArrowLeft'?'back':'next').click()}});load();
</script></html>'''


def main():
    snapshots=json.loads((HERE/'input-snapshots.json').read_text())
    z=np.load(HERE/'input-time-series.npz')
    events=[]
    names={'Early pulse 1':'First pulse','Early pulse 2':'Second pulse','Before slow precursor':'Before slow rise',
           'Precursor interval':'Precursor','Main shake':'Main shake','After shake':'After'}
    for e in snapshots['events']:
        key=f'r{e["run"]}_e{e["event"]}'
        values=[[None if not np.isfinite(v) else float(v) for v in row] for row in z[key+'_adc']]
        events.append({'run':e['run'],'event':e['event'],'channels':[c for _,c in e['order']],
                       'values':values,'rails':z[key+'_rails'].astype(int).tolist(),
                       'stages':[{'title':names[s['label']],'time':s['center_us'],
                                  'values':s['signed_median_ADC'],'rails':s['rail_observed']}
                                 for s in e['stages'] if s['label'] in names]})
    data={'time':z['time_us'].tolist(),'events':events}
    (HERE/'viewer.html').write_text(TEMPLATE.replace('__DATA__',json.dumps(data,separators=(',',':'))))
    print('Built self-contained APA2 section player.')


if __name__=='__main__':main()
