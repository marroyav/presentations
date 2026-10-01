# DUNE Dark Template Lab

This folder is a separate Beamer template sandbox for darker, more editorial DUNE talks.

Files:
- `beamerthemeDUNENoir.sty`: dark theme with custom title page, headline, footline, and broader panel styling
- `font-presets.tex`: font preset switches for `Helvetica`, `Open Sans`, `Dosis`, and `KoHo`
- `demo-body.tex`: shared demo deck body
- `fonts/`: local copies of the tested `Open Sans`, `Dosis`, and `KoHo` files used by the presets
- `main.tex`: Helvetica variant
- `opensans.tex`: Open Sans variant
- `dosis.tex`: Dosis variant
- `koho.tex`: KoHo variant
- `logos/`: copied from the current DUNE deck setup

Build:
```sh
cd /Users/marroyav/repo/presentations/dune_dark_template_lab
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error opensans.tex
xelatex -interaction=nonstopmode -halt-on-error dosis.tex
xelatex -interaction=nonstopmode -halt-on-error koho.tex
```

Font presets:
- Default in `main.tex`: `\DuneNoirUseHelvetica`
- Other available presets:
  - `\DuneNoirUseOpenSans`
  - `\DuneNoirUseDosis`
  - `\DuneNoirUseKoHo`

Current machine status:
- Installed: `Helvetica`, `Open Sans`, `Dosis`, `KoHo`
- Also installed: `Helvetica Neue`, `IBM Plex Sans`, `JetBrains Mono`

Behavior:
- `Open Sans`, `Dosis`, and `KoHo` are loaded from the local `fonts/` folder so the lab does not depend on system font discovery
- If a requested sans fallback is still needed, the preset falls back to `IBM Plex Sans`, then `Helvetica Neue`, then `Arial`
- Mono text falls back to JetBrains Mono when available

Intent:
- darker background
- broader cards and more whitespace
- stronger title hierarchy
- sample slide types beyond repeated block grids
- dark-theme branding with `DUNElogo_white.png` and `FNAL-Logo-NAL-Blue.png`
