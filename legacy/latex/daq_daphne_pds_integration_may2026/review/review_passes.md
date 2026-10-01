# Review Passes

Presentation: `daq_daphne_pds_integration_may2026/main.tex`

## Pass 1: Scientific Claim

Objective: make the central result explicit.

- The talk now separates the tested DAQ data-taking baseline from calibration automation.
- The success claim is scoped to the VD coldbox DAPHNE/SSP workflow and fddaq v5.5.0.
- The deck states what is validated, what is operationally required, and what remains a reviewer risk.

Outcome: kept the opening claim short and made the success criteria measurable.

## Pass 2: Repository Evidence

Objective: make the three DAQ repository changes reviewable.

- `fddetdataformats` is described as the owner of the persistent DAPHNE Ethernet frame contract.
- `rawdatautils` is described as the owner of Python/analysis-facing decoding arrays.
- `daphnemodules` is described as the controller and monitoring integration point.
- The deck distinguishes clean upstreamable changes from local or historical operational experiments.

Outcome: each repository has a contract slide, so a reviewer can map claims to code ownership.

## Pass 3: Operational Reproducibility

Objective: let a new collaborator reproduce the run context.

- The deck includes the SSH chain, tmux session name, run workarea, and required source scripts.
- The proxy rule is explicit: enable only for package downloads, disable before runtime.
- Validation run numbers are included: 44355 as the no-local-module control and 44356 as the clean override success case.

Outcome: the operational path is concrete enough to be repeated without relying on memory.

## Pass 4: Diagrams And Flow

Objective: make the chain visible before details.

- The baseline DAQ path is drawn as detector electronics to fragments to persisted frames to decoder output.
- The standalone path is drawn separately to prevent confusing direct hardware calibration with DAQ operation.
- The `pds-run` path shows seed JSON, scan JSON, minimal patch, XML overlay, SSP configuration, and `drunc`.

Outcome: diagrams now define the talk structure rather than decorating it.

## Pass 5: Editorial And LaTeX Readability

Objective: keep the deck formal and readable.

- Slides use compact bullets and repo-specific tables rather than long paragraphs.
- Commands are isolated on fragile frames where needed.
- Reviewer concerns are called out explicitly instead of being buried in narrative text.
- Remaining risk is stated: board identity and configuration target must be checked for `daphne-14`.

Outcome: the deck compiles cleanly with `latexmk -xelatex`; the final log has no overfull, underfull, LaTeX warning, package warning, or error matches. Selected diagram-heavy pages were rendered to PNG for visual checking.
