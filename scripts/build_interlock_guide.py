#!/usr/bin/env python3
"""Build the readable DUNE interlock views; retain all DPS source row IDs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "decks/detector_wide_interaction_matrix_sep2026/human"
GROUPS = {
    "protection": "What protects people or equipment?",
    "coordination": "Which activities or changes must wait?",
    "data": "What may continue with a data-quality record?",
    "together": "What needs to operate together?",
    "decisions": "Which detector interactions still need a decision?",
    "history": "What did ProtoDUNE operators do?",
}
STAGES = {
    "installation": "Installation",
    "commissioning": "Commissioning and integration",
    "run": "Run",
}
STATUS_HELP = {
    "Source + open details": "A reviewed source supports the general behavior. Production details still need agreement.",
    "Source conflict": "The proposed rule and an existing document disagree. Owners must reconcile them.",
    "Classification needs review": "The action is in a source, but the stated reason needs to be classified correctly.",
    "Decision needed": "The responsible teams have not settled the required conditions or response.",
    "Draft proposal": "A proposed operating rule that still needs agreement and detailed implementation.",
    "Past practice only": "Historical behavior, not a present-day detector requirement.",
}


def jdump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def mdcell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def references(data: dict, keys: list[str], markup: str = "html") -> str:
    result = []
    for key in keys:
        source = data["sources"][key]
        label = source["title"]
        if "url" in source:
            if markup == "html":
                label = f'<a href="{html.escape(source["url"], quote=True)}">{html.escape(label)}</a>'
            else:
                label = f'[{label}]({source["url"]})'
        elif markup == "html":
            label = html.escape(label)
        result.append(label)
    return "; ".join(result)


def validate(data: dict, snapshot: dict) -> None:
    rows = data["rules"]
    ids = [r["id"] for r in rows]
    source_ids = [r["id"] for r in snapshot["rows"]]
    if len(ids) != len(set(ids)) or len(source_ids) != len(set(source_ids)):
        raise ValueError("Duplicate rule IDs in the guide or source")
    if set(ids) != set(source_ids):
        raise ValueError(f"Coverage mismatch: missing {set(source_ids) - set(ids)}, extra {set(ids) - set(source_ids)}")
    teams = {team["id"] for team in data["teams"]}
    for row in rows:
        for key in ("id", "title", "why", "action", "restart", "open", *STAGES):
            if not row.get(key):
                raise ValueError(f"{row['id']} has no {key}")
        if not row["teams"] or not set(row["teams"]) <= teams:
            raise ValueError(f"Invalid team assignment: {row['id']}")
        if not row["sources"] or not set(row["sources"]) <= data["sources"].keys():
            raise ValueError(f"Invalid source reference: {row['id']}")
        if row["group"] not in GROUPS or row["status"] not in STATUS_HELP:
            raise ValueError(f"Invalid group/status: {row['id']}")
    for team in teams:
        if not any(team in row["teams"] for row in rows):
            raise ValueError(f"No rules for {team}")


def source_snapshot(register: Path) -> dict:
    fields = ("id", "title", "consequence_class", "enforcement_class", "required_response", "evidence_status")
    with register.open(newline="", encoding="utf-8") as handle:
        rows = [{key: row[key] for key in fields} for row in csv.DictReader(handle)]
    return {
        "source_file": "planning/" + register.name,
        "source_repository": "daphne_slow_controls_plan (local working draft)",
        "sha256": hashlib.sha256(register.read_bytes()).hexdigest(),
        "review_date": "2026-09-08",
        "note": "Selected original fields, preserved for comparison. This snapshot is not approval or proof of an upstream release.",
        "rows": rows,
    }


def matrix_markdown(data: dict) -> str:
    out = ["# DUNE interlocks in everyday detector language", "", f'{data["revision"]} · {data["date"]} · {len(data["rules"])} of {len(data["rules"])} source rows included', "",
           "Discussion draft. The actions below are proposals or summaries of reviewed sources; use approved detector procedures for operation.", "",
           "[Start here](README.md) · [Find your subsystem](subsystems.md) · [Search and filter](index.html) · [Review findings](review-notes.md)", "",
           "Each row answers: what happened, what we propose, and how settled the source is. The detailed entries below include the reason, teams, stage differences and return conditions.", ""]
    for group, title in GROUPS.items():
        out += [f"## {title}", "", "| Situation | Proposed action | Source status |", "|---|---|---|"]
        for r in data["rules"]:
            if r["group"] == group:
                out.append(f'| [{r["id"]}: {mdcell(r["title"])}](#{r["id"].lower()}) | {mdcell(r["action"])} | {r["status"]} |')
        out.append("")
    out += ["## Read the source status", ""]
    out += [f'- **{label}:** {explanation}' for label, explanation in STATUS_HELP.items()]
    out += ["", "## Details for each rule", ""]
    teams = {t["id"]: t["name"] for t in data["teams"]}
    for r in data["rules"]:
        out += [f'<a id="{r["id"].lower()}"></a>', f'### {r["id"]} · {r["title"]}', "",
                f'**Why it matters:** {r["why"]}', "", f'**What we propose:** {r["action"]}', "",
                f'**Before returning:** {r["restart"]}', "",
                "| Stage | What this means |", "|---|---|"]
        out += [f'| {name} | {mdcell(r[key])} |' for key, name in STAGES.items()]
        out += ["", "**Teams to agree the rule:** " + "; ".join(teams[t] for t in r["teams"]) + ".", "",
                f'**{r["status"]}. Still to agree:** {r["open"]}', "",
                "**Evidence:** " + references(data, r["sources"], "md") + ".", ""]
    return "\n".join(out)


def subsystems_markdown(data: dict) -> str:
    out = ["# Find your subsystem", "", f'{data["revision"]} · {data["date"]}', "",
           "Start with your team. These are the teams to consult, not an already approved assignment of responsibility. A rule can appear under several teams because they need to agree it together.", "",
           "[Start here](README.md) · [Full matrix](matrix.md) · [Searchable guide](index.html) · [Review form](review-form.md)", ""]
    for team in data["teams"]:
        out += [f'## {team["name"]}', "", team["headline"], "",
                f'**Tell the other teams:** {team["share"]}', "",
                f'**Agree with the other teams:** {team["agree"]}', "",
                "| Rule to review | What it means for coordination |", "|---|---|"]
        for r in data["rules"]:
            if team["id"] in r["teams"]:
                out.append(f'| [{r["id"]}: {mdcell(r["title"])}](matrix.md#{r["id"].lower()}) | {mdcell(r["action"])} |')
        out.append("")
    return "\n".join(out)


def html_guide(data: dict) -> str:
    esc = html.escape
    tokens = json.loads((ROOT / "templates/dune-professional/design-tokens.json").read_text(encoding="utf-8"))["colors"]
    team_names = {team["id"]: team["name"] for team in data["teams"]}
    team_options = "".join(f'<option value="{t["id"]}">{esc(t["name"])}</option>' for t in data["teams"])
    group_options = "".join(f'<option value="{key}">{esc(name)}</option>' for key, name in GROUPS.items())
    stage_options = "".join(f'<option value="{key}">{name}</option>' for key, name in STAGES.items())
    sections = []
    for group, title in GROUPS.items():
        cards = []
        for r in data["rules"]:
            if r["group"] != group:
                continue
            stages = "".join(f'<p class="stage" data-stage="{key}"><strong>{name}:</strong> {esc(r[key])}</p>' for key, name in STAGES.items())
            names = "; ".join(team_names[t] for t in r["teams"])
            search_text = esc(" ".join(str(v) for v in r.values()) + " " + names, quote=True)
            cards.append(f'''<article id="{r["id"]}" class="rule" data-teams="{' '.join(r['teams'])}" data-group="{group}" data-search="{search_text}">
<div class="rule-heading"><h3>{esc(r["title"])}</h3><a class="rule-id" href="#{r['id']}">{r['id']}</a></div>
<p class="action">{esc(r["action"])}</p>
<p class="status"><strong>{esc(r["status"])}</strong> · {esc(STATUS_HELP[r["status"]])}</p>
<div class="selected-stage"></div>
<details><summary>Why, who, stages and return conditions</summary>
<p><strong>Why it matters:</strong> {esc(r["why"])}</p>
<p><strong>Before returning:</strong> {esc(r["restart"])}</p>
<p><strong>Teams to agree the rule:</strong> {esc(names)}.</p>
{stages}
<p class="open"><strong>Still to agree:</strong> {esc(r["open"])}</p>
<p class="sources"><strong>Evidence:</strong> {references(data, r["sources"])}.</p>
</details></article>''')
        sections.append(f'<section class="rule-group" data-group="{group}"><h2>{title}</h2>{"".join(cards)}</section>')
    team_json = json.dumps(data["teams"], ensure_ascii=False).replace("<", "\\u003c")
    count = len(data["rules"])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DUNE interlocks — find your subsystem</title>
<style>
:root{{--ink:{tokens['background']['hex']};--muted:#44515e;--paper:{tokens['paper']['hex']};--sky:{tokens['sky']['hex']};--coral:{tokens['coral']['hex']};--line:#c4cdd3;--bg:#f5f7f8}}
*{{box-sizing:border-box}}body{{margin:0;color:var(--ink);background:var(--bg);font:17px/1.55 system-ui,-apple-system,'Segoe UI',sans-serif}}
header{{background:{tokens['title-surface']['hex']};color:{tokens['text']['hex']};padding:30px max(24px,calc((100vw - 1080px)/2))}}
header a{{color:var(--sky)}}h1{{font-size:clamp(30px,5vw,48px);line-height:1.1;margin:12px 0 20px;letter-spacing:-.025em}}
h2{{font-size:26px;line-height:1.3;margin-top:32px}}h3{{font-size:21px;line-height:1.3;margin:0}}p{{margin:10px 0}}
main{{max-width:1130px;padding:20px 24px 64px;margin:auto}}a{{color:#125673;text-underline-offset:3px}}a:hover{{text-decoration-thickness:2px}}
.intro{{max-width:820px}}.kicker{{font-size:14px;font-weight:700;letter-spacing:.04em}}.notice{{border-left:5px solid var(--coral);background:var(--paper);padding:14px 20px}}
.examples{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:24px 0}}.example{{padding:20px;background:white;border:1px solid var(--line);border-radius:8px}}.example strong{{display:block;font-size:19px;margin-bottom:8px}}
.filters{{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:12px;background:white;border:1px solid var(--line);padding:18px;border-radius:8px}}label{{display:block;font-size:14px;font-weight:700}}select,input,button{{font:inherit;border:1px solid #77838e;border-radius:4px;background:white;color:var(--ink);padding:9px;width:100%;margin-top:6px}}.search{{grid-column:1 / -1}}button{{width:auto;cursor:pointer}}button:hover{{background:var(--paper)}}:focus-visible{{outline:3px solid #125673;outline-offset:3px}}
.team-summary{{background:var(--sky);padding:18px 22px;border-radius:8px;margin:20px 0}}.team-summary h2{{margin-top:0}}
.toolbar{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin:16px 0}}
.rule{{background:white;border:1px solid var(--line);border-radius:8px;padding:20px 24px;margin:16px 0;scroll-margin-top:18px}}.rule-heading{{display:flex;gap:20px;justify-content:space-between}}.rule-id{{white-space:nowrap;font-size:14px}}.action{{font-size:18px;max-width:960px}}
.status{{color:var(--muted);font-size:14px}}details{{margin-top:12px;border-top:1px solid var(--line);padding-top:10px}}summary{{cursor:pointer;font-weight:650;color:#125673}}.open{{background:var(--paper);padding:12px 16px}}.sources{{font-size:14px}}.selected-stage p{{background:#e8f5f8;padding:10px 14px}}.selected-stage:empty{{display:none}}
[hidden]{{display:none!important}}footer{{font-size:14px;border-top:1px solid var(--line);margin-top:40px;padding-top:18px}}.empty{{padding:24px;background:var(--paper)}}
@media(max-width:760px){{.examples,.filters{{grid-template-columns:1fr}}.search{{grid-column:auto}}header{{padding:28px 24px}}.rule{{padding:18px}}.rule-heading{{display:block}}}}
@media print{{@page{{size:A4;margin:16mm}}body{{font-size:10pt;background:white}}header{{background:white;color:var(--ink);padding:0}}header a{{color:var(--ink)}}h1{{font-size:26pt}}main{{padding:0;max-width:none}}.filters,.toolbar button,.nav,.selected-stage{{display:none}}.examples{{display:block}}.example{{padding:8px 12px;margin:8px 0}}h2{{font-size:16pt;break-after:avoid}}h3{{font-size:12pt}}.rule{{break-inside:avoid;padding:12px;margin:10px 0}}.action{{font-size:10pt}}.status,.sources{{font-size:9pt}}details{{display:block}}summary{{display:none}}.team-summary,.notice,.open{{background:white;border:1px solid var(--line)}}}}
</style></head><body>
<header><div class="kicker">DUNE · {esc(data['revision'])} · {data['date']}</div>
<h1>What needs to happen<br>before your subsystem can run?</h1>
<p class="intro">Choose your subsystem. Each rule says what happens, why it matters, who needs to agree it, and what must be checked before returning.</p>
<p class="nav"><a href="../main.pdf">Presentation</a> · <a href="guide.pdf">Short PDF guide</a> · <a href="README.md">Start here</a> · <a href="review-form.md">Review form</a> · <a href="review-notes.md">Review findings</a></p></header>
<main><p class="notice"><strong>Discussion draft for collaboration review.</strong> All {count} source rules are included. This guide is not an operating procedure.</p>
<div class="examples"><div class="example"><strong>Protect equipment</strong>Confirm the required cryogenic conditions before starting cathode HV.</div><div class="example"><strong>Take turns</strong>PDS and camera lights or external lasers must not overlap in the agreed region.</div><div class="example"><strong>Keep running; label data</strong>Purity-monitor activity affects PDS data quality. It does not require PDS bias off in this draft.</div></div>
<p><strong>Two details matter:</strong> PDS must define the exact state excluded by external light. Power-over-fiber and PDS-owned calibration light have their own rules. The old PDS interface's purity-monitor and camera-light wording needs review.</p>
<div class="filters" role="search" aria-label="Filter interlock rules"><label>Your subsystem<select id="team"><option value="">All subsystems</option>{team_options}</select></label><label>Detector stage<select id="stage"><option value="">All stages</option>{stage_options}</select></label><label>Your question<select id="group"><option value="">All questions</option>{group_options}</select></label><label class="search">Find a situation, subsystem or rule<input id="search" type="search" placeholder="For example: purity, cooling, power loss, P-019"></label></div>
<section id="team-summary" class="team-summary" hidden aria-live="polite"></section>
<div class="toolbar"><p id="count" role="status">Showing {count} of {count} rules</p><div><button id="reset" type="button">Show all rules</button> <button id="expand" type="button" aria-expanded="false">Show details</button> <button id="print" type="button">Print this view</button></div></div>
<p id="empty" class="empty" hidden>No rules match these filters. Try a broader search or choose “Show all rules”.</p>
{''.join(sections)}
<footer>{esc(data['basis'])}<p>Teams listed are participants to consult, not an approved responsibility assignment. Source links may require collaboration access. Local working-source details and disagreements are recorded in <a href="review-notes.md">review findings</a> and <a href="source-map.json">the source snapshot</a>.</p></footer></main>
<script id="team-data" type="application/json">{team_json}</script>
<script>
const teams=JSON.parse(document.querySelector('#team-data').textContent);
const controls=['team','stage','group','search'].map(id=>document.getElementById(id));
const cards=[...document.querySelectorAll('.rule')];
const escapeHTML=value=>value.replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function syncDetailsButton(){{
  const visible=cards.filter(c=>!c.hidden);
  const allOpen=visible.length>0&&visible.every(c=>c.querySelector('details').open);
  const button=document.querySelector('#expand');
  button.textContent=allOpen?'Hide details':'Show details';
  button.setAttribute('aria-expanded',String(allOpen));
}}
function filter(){{
  const [team,stage,group,query]=controls.map(c=>c.value);
  const words=query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let n=0;
  for(const card of cards){{
    card.hidden=Boolean((team&&!card.dataset.teams.split(' ').includes(team))||(group&&card.dataset.group!==group)||!words.every(w=>card.dataset.search.toLowerCase().includes(w)));
    if(!card.hidden)n++;
    const line=stage?card.querySelector(`[data-stage="${{stage}}"]`):null;
    card.querySelector('.selected-stage').innerHTML=line?line.outerHTML:'';
  }}
  for(const section of document.querySelectorAll('.rule-group'))section.hidden=![...section.querySelectorAll('.rule')].some(c=>!c.hidden);
  document.querySelector('#count').textContent=`Showing ${{n}} of ${{cards.length}} rules${{stage?' · '+controls[1].selectedOptions[0].textContent:''}}`;
  document.querySelector('#empty').hidden=n!==0;
  const selected=teams.find(t=>t.id===team), box=document.querySelector('#team-summary');
  box.hidden=!selected;
  if(selected)box.innerHTML=`<h2>${{escapeHTML(selected.name)}}</h2><p><strong>${{escapeHTML(selected.headline)}}</strong></p><p><strong>Tell the other teams:</strong> ${{escapeHTML(selected.share)}}</p><p><strong>Agree together:</strong> ${{escapeHTML(selected.agree)}}</p>`;
  syncDetailsButton();
}}
controls.forEach(c=>c.addEventListener('input',filter));
cards.forEach(c=>c.querySelector('details').addEventListener('toggle',syncDetailsButton));
document.querySelector('#reset').addEventListener('click',()=>{{controls.forEach(c=>c.value='');filter();}});
document.querySelector('#expand').addEventListener('click',event=>{{const open=event.target.getAttribute('aria-expanded')!=='true';cards.filter(c=>!c.hidden).forEach(c=>c.querySelector('details').open=open);event.target.textContent=open?'Hide details':'Show details';event.target.setAttribute('aria-expanded',String(open));}});
let printState=[];
window.addEventListener('beforeprint',()=>{{printState=cards.map(c=>c.querySelector('details').open);cards.forEach(c=>c.querySelector('details').open=true);}});
window.addEventListener('afterprint',()=>cards.forEach((c,i)=>c.querySelector('details').open=printState[i]||false));
document.querySelector('#print').addEventListener('click',()=>window.print());
function openLink(){{const card=document.getElementById(location.hash.slice(1));if(card&&card.classList.contains('rule')){{controls.forEach(c=>c.value='');filter();card.querySelector('details').open=true;card.scrollIntoView();}}}}
const params=new URLSearchParams(location.search);
controls.forEach(c=>{{if(params.has(c.id))c.value=params.get(c.id);}});
window.addEventListener('hashchange',openLink);filter();openLink();
</script></body></html>
'''


def quick_guide_html(data: dict) -> str:
    """A short handout: one overview page, then two subsystem summaries per page."""
    esc = html.escape
    pages = []
    for start in range(0, len(data["teams"]), 2):
        teams = []
        for team in data["teams"][start:start + 2]:
            ids = [r["id"] for r in data["rules"] if team["id"] in r["teams"]]
            refs = ", ".join(f'<a href="index.html#{rule}">{rule}</a>' for rule in ids)
            teams.append(f'''<article><h2>{esc(team["name"])}</h2>
<p class="headline">{esc(team["headline"])}</p>
<p><strong>Tell the other teams:</strong> {esc(team["share"])}</p>
<p><strong>Agree together:</strong> {esc(team["agree"])}</p>
<p class="refs"><strong>Related rules:</strong> {refs}.</p>
<p><a href="index.html?team={team['id']}">Open the full rules for this team</a></p></article>''')
        pages.append('<section class="page">' + "".join(teams) + '</section>')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DUNE interlocks — a short guide for detector teams</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;color:#101820;background:#e9eef1;font:17px/1.5 system-ui,-apple-system,'Segoe UI',sans-serif}}
.page{{max-width:850px;margin:24px auto;padding:40px 46px;background:white}}h1{{font-size:34px;line-height:1.12;margin:16px 0}}h2{{font-size:23px;line-height:1.25;margin:0 0 14px}}p{{margin:12px 0}}a{{color:#125673;text-underline-offset:3px}}
.kicker,.refs{{font-size:13px}}.headline{{font-weight:700;font-size:19px}}.notice{{background:#f3eadb;padding:12px 16px}}article{{padding:24px 0;border-bottom:1px solid #b9c6d0}}article:first-child{{padding-top:0}}table{{border-collapse:collapse;width:100%;margin:20px 0}}td,th{{border-bottom:1px solid #b9c6d0;text-align:left;vertical-align:top;padding:10px}}th{{background:#a8ddeb}}
@media(max-width:600px){{.page{{padding:24px;margin:0}}h1{{font-size:28px}}}}
@media print{{@page{{size:A4;margin:17mm}}body{{font-size:11pt;background:white}}.page{{margin:0;padding:0;max-width:none;break-after:page}}.page:last-child{{break-after:auto}}h1{{font-size:25pt}}h2{{font-size:17pt}}.headline{{font-size:12pt}}.kicker,.refs{{font-size:9pt}}article{{break-inside:avoid;padding:16px 0}}p{{margin:9px 0}}td,th{{padding:8px}}}}
</style></head><body><section class="page">
<p class="kicker">DUNE · {esc(data['revision'])} · {data['date']}</p>
<h1>What can run together?<br>What must wait?<br>What needs protection?</h1>
<p class="notice">Discussion draft for collaboration review, not an operating procedure.</p>
<p>Read this page and the summary for your subsystem. The full guide contains every one of the 40 source rules, with actions, detector stages, source disagreements and return conditions.</p>
<table><thead><tr><th>Situation</th><th>What we propose</th></tr></thead><tbody>
<tr><td>Cryogenics has not confirmed HV readiness</td><td>Keep cathode HV off until the agreed checks pass. Protect the equipment.</td></tr>
<tr><td>Camera lights or an external laser with PDS</td><td>Take turns. Block the second request and verify light-off before PDS returns.</td></tr>
<tr><td>Purity monitor with PDS</td><td>Keep PDS running and mark the affected data. PDS bias stays on for this interaction.</td></tr>
</tbody></table>
<p><strong>Define the actual PDS state.</strong> The photon detection system (PDS) team must say which powered, biased or acquiring state excludes external light. PDS-owned calibration light and power-over-fiber have their own rules.</p>
<p><strong>Use the procedure for the detector stage.</strong> Installation needs work and isolation checks. Commissioning and integration need an agreed test plan and owner. A run needs the right equipment states and data-quality records.</p>
<p><strong>Some answers remain open.</strong> The old PDS interface conflicts with the proposed purity-monitor rule. Cathode-loss response, power-loss ordering and several electronics conditions still need detector decisions.</p>
<p><a href="index.html">Search the complete guide by subsystem</a> · <a href="review-form.md">Send a rule review</a> · <a href="review-notes.md">Read the findings and sources</a></p>
</section>{''.join(pages)}</body></html>
'''


def render_pdf() -> None:
    browser = shutil.which("chromium") or shutil.which("google-chrome")
    if not browser:
        raise SystemExit("PDF export needs Chromium or Google Chrome. The Markdown and HTML views are already built.")
    with tempfile.TemporaryDirectory(prefix="dune-guide-print-") as profile:
        command = [browser, "--headless", "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
                   "--disable-background-networking", "--no-first-run", "--no-pdf-header-footer",
                   "--user-data-dir=" + profile, "--print-to-pdf=" + str(GUIDE / "guide.pdf"),
                   (GUIDE / "quick-guide.html").as_uri()]
        result = subprocess.run(command, text=True, capture_output=True, timeout=45)
        if result.returncode:
            raise SystemExit(result.stderr)
    digest = hashlib.sha256((GUIDE / "quick-guide.html").read_bytes()).hexdigest()
    (GUIDE / "guide-pdf-source.sha256").write_text(digest + "  quick-guide.html\n", encoding="utf-8")
    print("Short subsystem guide PDF updated.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, help="Recheck against the working DPS CSV and refresh the source snapshot")
    parser.add_argument("--check", action="store_true", help="Validate without changing generated files")
    parser.add_argument("--pdf", action="store_true", help="Also print the short subsystem handout using a local Chromium browser")
    args = parser.parse_args()
    if args.check and args.pdf:
        parser.error("--check does not write files; use --pdf separately")
    data = json.loads((GUIDE / "rules.json").read_text(encoding="utf-8"))
    snapshot = source_snapshot(args.register) if args.register else json.loads((GUIDE / "source-map.json").read_text(encoding="utf-8"))
    validate(data, snapshot)
    outputs = {"source-map.json": jdump(snapshot), "matrix.md": matrix_markdown(data),
               "subsystems.md": subsystems_markdown(data), "index.html": html_guide(data),
               "quick-guide.html": quick_guide_html(data)}
    for name, content in outputs.items():
        path = GUIDE / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Generated view is out of date: {path.relative_to(ROOT)}")
        else:
            path.write_text(content, encoding="utf-8")
    if args.pdf:
        render_pdf()
    if args.check:
        expected = hashlib.sha256((GUIDE / "quick-guide.html").read_bytes()).hexdigest() + "  quick-guide.html\n"
        marker = GUIDE / "guide-pdf-source.sha256"
        if not (GUIDE / "guide.pdf").exists() or not marker.exists() or marker.read_text(encoding="utf-8") != expected:
            raise SystemExit("Short guide PDF is missing or out of date; rebuild with --pdf")
    print(f'Interlock guide: {len(data["rules"])}/{len(snapshot["rows"])} source rows; {len(data["teams"])} subsystem views; generated views {"verified" if args.check else "updated"}.')


if __name__ == "__main__":
    main()
