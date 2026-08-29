TECTONIC ?= tectonic
TECTONIC_FLAGS ?= --chatter minimal --keep-logs --keep-intermediates
PYTHON ?= python3

.SECONDEXPANSION:

DECK_DIRS := $(shell find decks -mindepth 1 -maxdepth 1 -type d | sort)
PDFS := $(addsuffix /main.pdf,$(DECK_DIRS))
DIAGRAM_SOURCES := $(shell find decks examples -type f -name '*.dot.in' 2>/dev/null | sort)
DIAGRAM_PDFS := $(DIAGRAM_SOURCES:.dot.in=.pdf)
STARTER_PDF := examples/framework_starter/main.pdf

.PHONY: all diagrams schematics audit check starter new-deck clean

all: diagrams $(PDFS)

diagrams: $(DIAGRAM_PDFS)

%.pdf: %.dot.in templates/dune-professional/design-tokens.json scripts/render_diagram.py
	$(PYTHON) scripts/render_diagram.py $< $@

decks/%/main.pdf: decks/%/main.tex templates/dune-professional/beamerthemeDUNEProfessional.sty $$(wildcard decks/$$*/diagrams/*) $$(wildcard decks/$$*/figures/*) $$(wildcard decks/$$*/schematics.json) | diagrams
	cd decks/$* && $(TECTONIC) $(TECTONIC_FLAGS) main.tex

schematics:
	$(PYTHON) scripts/audit_schematics.py decks

audit:
	$(PYTHON) scripts/audit_design.py
	$(PYTHON) scripts/audit_decks.py decks

starter: diagrams $(STARTER_PDF)

$(STARTER_PDF): examples/framework_starter/main.tex templates/dune-professional/beamerthemeDUNEProfessional.sty examples/framework_starter/diagrams/system-context.pdf
	cd examples/framework_starter && $(TECTONIC) $(TECTONIC_FLAGS) main.tex

check: audit schematics starter all

new-deck:
	@test -n "$(SLUG)" || (echo "Usage: make new-deck SLUG=my_deck TITLE='My title'" && exit 2)
	@test -n "$(TITLE)" || (echo "TITLE is required" && exit 2)
	@$(PYTHON) scripts/new_deck.py "$(SLUG)" --title "$(TITLE)" --author "$(if $(AUTHOR),$(AUTHOR),Your name)"

clean:
	find decks examples -type f \( -name '*.aux' -o -name '*.log' -o -name '*.nav' -o -name '*.out' -o -name '*.snm' -o -name '*.toc' -o -name '*.vrb' -o -name '*.xdv' \) -delete
