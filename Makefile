TECTONIC ?= tectonic

DECK_DIRS := $(shell find decks -mindepth 1 -maxdepth 1 -type d | sort)
PDFS := $(addsuffix /main.pdf,$(DECK_DIRS))

.PHONY: all audit clean

all: $(PDFS)

decks/%/main.pdf: decks/%/main.tex templates/dune-professional/beamerthemeDUNEProfessional.sty
	cd decks/$* && $(TECTONIC) --keep-logs --keep-intermediates main.tex

audit:
	python3 scripts/audit_decks.py decks

clean:
	find decks -type f \( -name '*.aux' -o -name '*.log' -o -name '*.nav' -o -name '*.out' -o -name '*.snm' -o -name '*.toc' -o -name '*.vrb' -o -name '*.xdv' \) -delete

