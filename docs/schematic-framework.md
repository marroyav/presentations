# Standalone electrical schematic framework

The source of truth is the diagram, not the presentation. Each SVG must explain
one concept cleanly on its own; a slide may consume that reviewed artifact
later without rearranging, recoloring, or relabeling it.

The implemented pilot is deliberately narrower than a general drawing app: it
is a checked visual grammar for small, standalone explanatory schematics. Real
hardware authority remains a separate KiCad lane.

## What the reference actually establishes

The benchmark remains slides 12–14 of
[HD & VD Mezzanine QA/QC](https://indico.fnal.gov/event/74170/contributions/342404/attachments/198858/276941/HD_VD_MEZZANINE_QA_QC.pdf).
The PDF metadata identifies Microsoft PowerPoint for Microsoft 365 as the slide
creator and producer, while the inner engineering figures are flattened raster
images. The final slide composition therefore came from PowerPoint, but the
original tool used for those inner figures cannot be recovered from this PDF.
Attributing them specifically to Visio, KiCad, or another editor would be
speculation.

Their quality is reproducible without knowing that tool. The important traits
are restrained monochrome artwork, consistent thin lines, orthogonal routing,
small shape vocabulary, deliberate whitespace, and a single dominant flow.

## Three artifact classes

Do not ask one renderer to impersonate every kind of electrical drawing.

### 1. Illustrative circuit

Use the repository's SchemDraw wrapper for one small explanatory topology or
circuit fragment. SchemDraw supplies vector electrical symbols, anchors,
orthogonal wire shapes, and centralized drawing configuration, but placement
and complex routing remain explicit author decisions; see the official
[placement and wire documentation](https://schemdraw.readthedocs.io/en/latest/usage/placement.html).

Classification: `illustrative-circuit`. It may not claim ERC or manufacturing
authority.

### 2. System or test-stand diagram

Use the same visual contract for a pure composition, interface, or data-flow
view. Small structures may use the SchemDraw wrapper. A larger graph should
pilot D2 with its ELK backend, which supports hierarchical layout, ports,
orthogonal routing, and crossing minimization; see
[D2](https://github.com/terrastruct/d2) and the
[ELK layered algorithm](https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-layered.html).
ELK reduces layout work but does not eliminate the final visual review.

When a GUI is more useful than source code, diagrams.net Desktop is the manual
lane. Its official workflow supports custom libraries and an
[MCP diagram server](https://www.drawio.com/docs/manual/generate/drawio-mcp-server/);
commit both the editable `.drawio` file and reviewed SVG. These connections are
visual, not electrically checked.

Classification: `system-structure` or `system-flow`.

### 3. Hardware-authority schematic

Use KiCad for anything intended to define, validate, build, or troubleshoot
real hardware. KiCad owns symbols, typed pins, nets, hierarchy, footprints,
BOM, and electrical rules. The repository consumes revision-stamped SVG/PDF
exports after ERC; [`kicad-cli`](https://docs.kicad.org/10.0/en/cli/cli.html)
supports headless ERC and vector export.

Required chain:

```text
KiCad source at an immutable revision
  -> ERC report and canonical netlist
  -> reviewed ERC dispositions
  -> monochrome SVG and PDF export
  -> content hashes and named human review
  -> optional presentation inclusion
```

Only this lane may use `erc-clean` or `human-reviewed` without an illustrative
qualifier.

Use [WireViz](https://github.com/wireviz/WireViz) instead when the artifact is a
cable assembly or connector/pinout document. It is deliberately not the tool
for a complete electrical system.

## AI-assisted authoring candidates

Tool review date: 2026-08-28. No reviewed AI schematic maker replaces the two
artifact lanes above. The most useful candidates generate editable KiCad source
upstream of the same verification gates:

- [Copperhead](https://docs.copperhead.sh/reference/schematic-drafting/) is the
  first local pilot. Its deterministic drafter checks placement, spacing,
  alignment, and crossings, emits `.kicad_sch`, and can run KiCad checks. Its
  [repository](https://github.com/copperheadhq/copperhead) also describes the
  project as early, so it remains disposable-branch tooling until proven.
- [CELUS](https://www.celus.io/knowledge/2026.08.19) is the strongest reviewed
  commercial KiCad handoff, but its own
  [terms](https://www.celus.io/legal/terms-of-use-celus-design-platform) treat
  generated designs as machine-generated drafts requiring qualified review.
- [SpeedUp](https://speed-up.ai/ai-schematic-generator/) exports editable KiCad
  projects but explicitly positions them as prototype-stage drafts.
- Microsoft's [SchGen](https://github.com/microsoft/SchGen) produces editable
  KiCad schematics while warning about possible connectivity, component, and
  layout errors. It is a research reference, not an authority source.

Promotion requires deterministic regeneration, canonical-netlist equivalence,
zero unwaived ERC findings, stable KiCad 10 round trips, verified symbols and
footprints, and zero visual collisions. AI remains an authoring accelerator;
KiCad plus named engineering review remains the source of authority.

## Non-negotiable visual contract

The versioned tokens live in `schematics/style.json`.

- one concept and one reading direction per SVG;
- one `1.25` stroke width for wires, component outlines, equipment boundaries,
  junction outlines, and terminal outlines;
- one font family, DejaVu Sans, with a 10-point minimum;
- black primary artwork, secondary gray only for scope/status text, and optional
  near-white fill for containment;
- orthogonal routes on a 0.25-unit grid;
- a minimum reserved clearance around every independent object and text lane;
- repetition shown once by multiplicity or ellipsis, with one representative
  branch expanded;
- unknown values placed locally or stated once in a short source-limit line;
- no prose panels, slide furniture, decorative color cards, raster images, or
  hidden white patches over crossings.

Portable output is part of the contract. The pinned ZiaMath/ZiaFont stack
outlines DejaVu Sans into the SVG, so Windows and Linux do not substitute a
different font. Accessible title/description elements and the layout manifest
retain the diagram's text for review and automation.

Hierarchy comes from placement, whitespace, fill, and gray—not a second line
weight. Power, signal, control, and reference networks become separate
one-concept artifacts when combining them would create competing paths.

## Deterministic checks

Generation has two gates.

The wrapper records the renderer's actual bounds for each symbol group,
connection marker, block, and label. It requires all such objects to be present
before routing begins. The layout ledger then rejects:

- overlapping reserved regions after clearance;
- diagonal, zero-length, or off-grid routes;
- an unjoined wire crossing or an overlapping wire segment;
- a route entering an unrelated object;
- text that escapes a fixed block;
- objects outside the artboard;
- an object added after routing begins, which would make collision checking
  dependent on source order.

The independent SVG audit rejects:

- any visible noncanonical stroke width;
- any stroke, fill, or background outside the canonical monochrome palette;
- mixed fonts or type below the minimum size;
- embedded raster images or HTML `foreignObject` content;
- missing identity/classification metadata;
- a changed artifact hash or invalid recorded layout.

These checks prevent common mechanical failures. They do not judge electrical
truth or replace a visual review at normal and reduced size.

## Current pilot

The framework intentionally starts with two different one-concept artifacts:

1. `S09-01`: a SiPM equivalent with representative microcell branches in
   parallel, labels reserved in one lane, and repetition stated once;
2. `S14-01`: SuperCell composition only, with containment lines explicitly
   distinguished from electrical nets.

Both are native SVG, use the same font and line weight, and pass the same audit.
They test the visual system before any presentation work resumes.

## Development plan

1. Review the two pilots at 100%, 50%, and print scale. Freeze the visual tokens
   only after that review.
2. Create a KiCad 10 project template with fixed text/line rules, built-in font,
   monochrome plot theme, pinned symbol libraries, and CI commands for ERC,
   netlist, SVG, and PDF.
3. Pilot one real hardware sheet in KiCad. It becomes the first authority-grade
   artifact only after ERC, netlist comparison, and named human review.
4. Split the remaining source material into individual concepts: one cold
   amplifier channel, one signal interface, one power/return/ground view, one
   passive-ganging network, and one U/L differential-output view.
5. Add a D2/ELK adapter only when a system topology is large enough to benefit
   from automatic layout. Normalize its SVG to this same token contract.
6. Add rendered SVG regression images so changed geometry requires deliberate
   review, not only a passing source audit.
7. Pilot Copperhead on disposable branches with three golden cases: a
   regulator, an MCU/sensor sheet, and a dense mixed-signal interface. Promote
   it only if editable KiCad output passes the ERC, pin/footprint, netlist, BOM,
   visual, deterministic-build, and IP-review gates; screenshots and PDF-only
   results are not accepted as engineering source.
