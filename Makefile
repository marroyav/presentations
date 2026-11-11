TECTONIC ?= tectonic
TECTONIC_FLAGS ?= --chatter minimal --keep-logs --keep-intermediates
PYTHON ?= python3

.SECONDEXPANSION:

DECK_DIRS := $(shell find decks -mindepth 1 -maxdepth 1 -type d | sort)
PDFS := $(addsuffix /main.pdf,$(DECK_DIRS))
DIAGRAM_SOURCES := $(shell find decks examples -type f -name '*.dot.in' 2>/dev/null | sort)
DIAGRAM_PDFS := $(DIAGRAM_SOURCES:.dot.in=.pdf)
STARTER_PDF := examples/framework_starter/main.pdf
SCHEMATIC_TESTS := \
	schematics.test_contract \
	schematics.test_geometry \
	schematics.test_svg_postprocess

.PHONY: all diagrams schematics schematic-concepts audit-schematic-concepts audit check starter new-deck clean interlock-guide check-interlock-guide

all: diagrams $(PDFS)

diagrams: $(DIAGRAM_PDFS)

%.pdf: %.dot.in templates/dune-professional/design-tokens.json scripts/render_diagram.py
	$(PYTHON) scripts/render_diagram.py $< $@

decks/grouped32_simulation_sep2026/design-tokens.json: decks/grouped32_simulation_sep2026/palette.py templates/dune-professional/design-tokens.json
	$(PYTHON) decks/grouped32_simulation_sep2026/palette.py

decks/grouped32_simulation_sep2026/diagrams/%.pdf: decks/grouped32_simulation_sep2026/diagrams/%.dot.in decks/grouped32_simulation_sep2026/design-tokens.json scripts/render_diagram.py
	$(PYTHON) scripts/render_diagram.py $< $@ --tokens decks/grouped32_simulation_sep2026/design-tokens.json

decks/%/main.pdf: decks/%/main.tex templates/dune-professional/beamerthemeDUNEProfessional.sty $$(wildcard decks/$$*/*.tex) $$(wildcard decks/$$*/fonts/*.ttf) $$(wildcard decks/$$*/fonts/*.tex) $$(wildcard decks/$$*/diagrams/*) $$(wildcard decks/$$*/figures/*) $$(wildcard decks/$$*/commands/*) $$(wildcard decks/$$*/schematics.json) | diagrams
	cd decks/$* && $(TECTONIC) $(TECTONIC_FLAGS) main.tex

schematics:
	$(PYTHON) scripts/audit_schematics.py decks

schematic-concepts:
	$(PYTHON) -m schematics.render_all
	$(PYTHON) -m unittest $(SCHEMATIC_TESTS)
	$(PYTHON) -m schematics.audit

audit-schematic-concepts:
	$(PYTHON) -m unittest $(SCHEMATIC_TESTS)
	$(PYTHON) -m schematics.audit

audit:
	$(PYTHON) scripts/audit_design.py
	$(PYTHON) scripts/audit_decks.py decks

starter: diagrams $(STARTER_PDF)

$(STARTER_PDF): examples/framework_starter/main.tex templates/dune-professional/beamerthemeDUNEProfessional.sty examples/framework_starter/diagrams/system-context.pdf
	cd examples/framework_starter && $(TECTONIC) $(TECTONIC_FLAGS) main.tex

interlock-guide:
	$(PYTHON) scripts/build_interlock_guide.py

check-interlock-guide:
	$(PYTHON) scripts/build_interlock_guide.py --check

check: audit schematics audit-schematic-concepts check-interlock-guide starter all

new-deck:
	@test -n "$(SLUG)" || (echo "Usage: make new-deck SLUG=my_deck TITLE='My title'" && exit 2)
	@test -n "$(TITLE)" || (echo "TITLE is required" && exit 2)
	@$(PYTHON) scripts/new_deck.py "$(SLUG)" --title "$(TITLE)" --author "$(if $(AUTHOR),$(AUTHOR),Your name)"

clean:
	find decks examples -type f \( -name '*.aux' -o -name '*.log' -o -name '*.nav' -o -name '*.out' -o -name '*.snm' -o -name '*.toc' -o -name '*.vrb' -o -name '*.xdv' \) -delete

# Standalone report; build only this report with `make pds-readout-report`.
PDS_READOUT_REPORT := reports/pds_readout_tests_oct2026
.PHONY: pds-readout-report
pds-readout-report: $(PDS_READOUT_REPORT)/main.pdf

$(PDS_READOUT_REPORT)/main.pdf: $(PDS_READOUT_REPORT)/main.tex $(PDS_READOUT_REPORT)/build_report.py $(wildcard $(PDS_READOUT_REPORT)/evidence/*.json)
	$(PYTHON) $(PDS_READOUT_REPORT)/build_report.py
	cd $(PDS_READOUT_REPORT) && $(TECTONIC) $(TECTONIC_FLAGS) main.tex

# Plain-language ground-shake summary; input checks precede the PDF build.
.PHONY: ground-shakes-report
ground-shakes-report:
	$(PYTHON) reports/ground_shakes_nov2026/build_report.py
	cd reports/ground_shakes_nov2026 && $(TECTONIC) $(TECTONIC_FLAGS) main.tex
