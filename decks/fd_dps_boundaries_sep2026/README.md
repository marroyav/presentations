# FD DPS: define the boundaries first

Draft 0.1 · 22 September 2026 · Prepared for Manuel Arroyave

Audience: detector, Slow Controls, facility and project engineers. Outcome: agree what each system owns and where it hands information, power or action to another system.

This pack starts with definitions and responsibility boundaries. Detailed protocols, registers, thresholds and wiring schedules come later. It records source-backed design intent and user-confirmed requirements; it does not claim installation or acceptance.

Architecture direction: **SC monitors and configures in parallel; DPS/local protection executes all DPS logic.** The contrary software-interlock allocation in the older TTO text is recorded for reconciliation in SOURCES.md.

- [Five-slide review](main.pdf)
- [Control-interface draft: scope and boundaries](CONTROL_INTERFACE_DRAFT.md)
- [Proposed responsibilities](RESPONSIBILITIES.md)
- [Sources and remaining uncertainty](SOURCES.md)
- Reference architecture: [original slide 2 from the 8 September presentation](diagrams/01_reference_architecture.pdf), with [editable original figure](../surf_bms_fd_integration_sep2026/figures/architecture.tex). It is retained intact, including its original date and page label.
- Editable new diagrams: [physical interfaces](diagrams/02_physical_interfaces.dot.in), [power domains](diagrams/03_power_domains.dot.in).
- Standalone vectors: [reference architecture](diagrams/01_reference_architecture.svg), [physical interfaces](diagrams/02_physical_interfaces.svg), [power domains](diagrams/03_power_domains.svg).
- Local rack example: [diagram](diagrams/04_rack_protection.pdf), [SVG](diagrams/04_rack_protection.svg), [editable source](diagrams/04_rack_protection.dot.in). Smoke input → DPS/local decision → Raritan outlets → equipment, with parallel SC monitoring/configuration.

The earlier [working plan](../../../wl-144132/dune-docs-analysis/reports/FD_DPS_WORKING_PLAN_2026-09-22.md) remains the longer planning record. Proposed names here are starting assignments, not accepted commitments or a new organization chart.

Build only this pack from the presentations root:

```sh
python3 decks/fd_dps_boundaries_sep2026/build.py
make audit
```

The build uses the existing tokenized Graphviz renderer and Tectonic. It does not check hashes or rebuild other decks. No messages have been sent.
