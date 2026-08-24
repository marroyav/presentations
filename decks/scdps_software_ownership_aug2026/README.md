# SC/DPS Software Ownership

Deck slug: `scdps_software_ownership_aug2026`

Complete this brief before adding slides. It is the deck's editorial contract.

## Audience

- Primary audience: DUNE slow-controls, DAQ, Computing, subsystem, and DPS/facilities stakeholders discussing repository ownership.
- What they already know: Prototype code exists for DAPHNE, WIB/BDE, bridges, emulators, and support services; official requirements live in EDMS/DUNE sources.
- What they need from this talk: A clear boundary between Slow Controls, DAQ, Computing, subsystem owners, and protection owners before naming final repositories.

## Outcome

- One-sentence takeaway: Agree on who owns each behavior before deciding where the code lives.
- Decision or action requested: Agree on the responsibility lines, then choose DAPHNE or WIB as the first working example.
- Owner and completion condition: We are done when named SC, DAQ, Computing, subsystem, and DPS/facilities reviewers accept one shared interface used by a DAQ client, an SC bridge, and an emulator.

## Scope

- In scope: PDU/rack services, PDS/DAPHNE, TPC/BDE/WIB, HVS/calibration, TDE/timing, DAQ-facing interfaces, Computing support, DPS/facilities boundaries, and Git checks.
- Explicitly out of scope: Final repository names, live deployment details, private site configuration, secrets, and claims that monitoring software provides credited protection.

## Evidence

- Authoritative sources: Online EDMS/DUNE documents, DUNE and DUNE-DAQ GitHub spaces, DUNE Computing guidance, and release/test evidence produced by the repositories.
- Measurements or test results: First proof should be one shared contract used by one DAQ client, one SC bridge, and one emulator scenario.
- Important uncertainty: Exact GitHub namespace and CODEOWNERS assignments require meeting agreement.

## Build

From the repository root:

```sh
make
```

Graphviz sources live in `diagrams/*.dot.in`. Use only tokens from
`templates/dune-professional/design-tokens.json`; `make diagrams` renders them
to vector PDF.

## Reference index

The main deck shows only the sources needed to explain the argument. This is
the complete working index:

- [Common Slow Controls project](https://edms.cern.ch/project/CERN-0000266175)
- [PDS slow controls](https://edms.cern.ch/document/3309688)
- [BDE slow controls](https://edms.cern.ch/document/3362709)
- [HVS slow controls](https://edms.cern.ch/document/3315615)
- [TDE slow controls](https://edms.cern.ch/document/3297045)
- [DAQ slow controls](https://edms.cern.ch/document/3449868)
- [Detector protection system](https://edms.cern.ch/document/2401090)
- [VD rack assignments](https://edms.cern.ch/document/2741879/1)
- [HD rack assignments](https://edms.cern.ch/document/2429058/3)
- [DAQ rack build](https://edms.cern.ch/document/2794420/1)
- [HWDB export project](https://edms.cern.ch/project/CERN-0000279681)
- [DUNE-DAQ GitHub](https://github.com/DUNE-DAQ)
- [DUNE GitHub](https://github.com/DUNE)
- [DUNE Computing basics](https://dune.github.io/computing-basics/)
- [Offline Computing CDR](https://arxiv.org/abs/2210.15665)
