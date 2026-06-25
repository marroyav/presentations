# `daphne-firmware` Architecture Assets

This directory is the reusable architecture source-of-truth for
`daphne-firmware`.

It is intentionally not a one-off slide drawing.

The package contains:

- a canonical node table
- a canonical edge table
- reusable view definitions
- a generator that renders Graphviz diagrams
- a dependency matrix derived from the same edge set
- curated publication-oriented views built from the same catalog

## Why this exists

The goal is to make the architecture description:

- presentation-friendly
- document-friendly
- query-friendly
- extensible to other repositories and the full DAQ chain

The intended expansion path is:

- `daphne-firmware`
- `daphne-server`
- `daphnemodules`
- sender / receiver chain
- frame builder / decoding / DAQ reception

without changing the core data model.

## Directory layout

```text
data/
  nodes.csv
  edges.csv
views/
  views.json
scripts/
  render_architecture.py
output/
  *.dot
  *.svg
  *.pdf
  *.png
  dependency_matrix.csv
  dependency_matrix.md
```

## Data model

### Nodes

`data/nodes.csv` columns:

- `id`: stable identifier
- `label`: display label
- `repo`: owning repository
- `kind`: repo, module, ip, block, build, or clock_source
- `layer`: high-level layer used for styling and grouping
- `ownership`: `repo_owned`, `imported`, or `platform`
- `group`: coarse subsystem bucket
- `description`: short meaning

### Edges

`data/edges.csv` columns:

- `src`
- `dst`
- `relation`
- `domain`
- `label`
- `condition`
- `note`

Current relations used here:

- `contains`
- `configures`
- `readiness_prereq`
- `asserts`
- `enables`
- `streams_to`
- `observes`
- `clock_source`
- `clocks`
- `qualifies`
- `drives`
- `produces`

The current view set is intentionally curated, so not every relation appears in every figure.

## Render

From this directory:

```bash
python3 scripts/render_architecture.py
```

This writes the reusable assets into `output/`.

To render just one view:

```bash
python3 scripts/render_architecture.py --view subsystem_hierarchy
python3 scripts/render_architecture.py --view runtime_dataflow
python3 scripts/render_architecture.py --view clock_topology
python3 scripts/render_architecture.py --view readiness_contracts
python3 scripts/render_architecture.py --view build_flow
```

## Current figure set

The current curated views are:

- `subsystem_hierarchy`
- `runtime_dataflow`
- `clock_topology`
- `readiness_contracts`
- `build_flow`

## Scaling to other repositories

Do not fork the script for each repository.

Instead:

1. add more nodes with a different `repo` value
2. add more inter-repo edges
3. add a new view in `views/views.json`

Examples of later views:

- `full_chain_control`
- `daq_reception_path`
- `frame_decode_path`
- `cross_repo_readiness`
- `software_hardware_contracts`

## Dependency matrix

The dependency matrix is generated from the curated readiness/dependency view, not hand-maintained.

That makes it suitable for:

- adjacency inspection
- design structure matrix work
- simple database import
- later graph analytics if this grows into a larger architecture catalog
