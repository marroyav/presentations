# PDS PoF budget

One slide · 14 October 2026 · USD indicative hardware estimates.

Audience: PDS and SC integration teams comparing the PoF team’s Opta
implementation with I/O added to the existing Beckhoff platform.
Outcome: distinguish the two monitoring scopes and their hardware budgets.

The slide compares two boxes per rack, 40 racks, one enable per box:

| Scope per box | Opta per rack | Beckhoff I/O per rack |
|---|---|---|
| Up to 7 V + one RTD | $379.50–395.35 | $1,269.38–1,499.38 |
| 8 V + 8 RTDs | $759.00–790.70 | $1,624.38–2,084.38 |

The smaller scope is the upper voltage count in the PoF team’s three-slide
presentation (4–7 V and one chassis RTD). The larger scope is the user’s working
inventory, sized from manufacturer channel capacities. Both assume two-wire
PT100 RTDs and a compatible single box-enable interface. Neither budget
qualifies the PoF connector or electrical mapping.

`main.tex` and `main.pdf` are the slide. `speaker-notes.txt` records the BOM,
limits and sources. `estimates.json` preserves the prices, URLs and arithmetic;
`validation.json` records the build and review. No figure captions or
verification comments are displayed.

Build with `make decks/pds_pof_budget/main.pdf` from the repository root, or
`tectonic --chatter minimal --keep-logs main.tex` in this directory.
