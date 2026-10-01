# Current draft

22 September 2026. Canonical pack: this directory in the existing presentations repository. Existing unrelated changes were preserved; no commit made.

User direction: concise definitions and known physical boundaries first. No protocol/register detail yet. Manuel owns HD/VD DPS. TPC/PDS warm electronics have no UPS. DAQ/SC/DPS require UPS; the July CUC review already provides DAQ/SC planning evidence. The exact DPS feed and dependency map remain open.

Critical architecture correction: Slow Controls monitors and configures in parallel. It contains no DPS logic. DPS/local protection executes protective decisions with source inputs and action feedback available independently of SC. The older FDC TTO allocation of software interlocks to SC is an explicit document-reconciliation item, not this draft's architecture.

Reference correction: Manuel identifies his earlier two-line diagram as accurate and confirms that it defines the facility-to-DPS connection. The pack retains slide 2, “How facility signals reach DUNE,” from the 8 September presentation intact. Monitoring is above, DPS control/protection below, with DPS status upward. The architecture is settled for this draft; hardware allocation and named responsibilities remain to be detailed. The generated alternative was moved to previous/. Avoid reopening the architecture or replacing it with new abstractions.

Additional user direction: Raritan PDU is the proposed common power-control endpoint and smoke sensors are available. Add a local rack example using the same two-line layout. Existing 32655-v8 hardware supports this; its Ignition-primary protection logic conflicts with the requested architecture and is recorded for reallocation. The PDU covers loads safe to protect by AC removal; specific inhibits/sequences and essential loads are exceptions to map.

Artifacts: five-slide PDF, the original editable TikZ reference plus three new Graphviz diagrams, SVG/PDF exports, short proposed responsibilities, and a scope/boundary draft for the interface document. Source provenance and uncertainty are in SOURCES.md. No messages sent, hardware changed or hashes checked.

Validation: Graphviz/Tectonic build; shared design/deck audit; PDF text and page-boundary checks; rendered page review. The full repository check includes hash verification and was not run, following the user's instruction. Global audit advisories concern other pre-existing decks.

Next review: user correction of functional boundaries and proposed responsibility allocation. Detailed physical endpoint assignment and acceptance requirements follow that review.
