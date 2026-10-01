TECTONIC ?= /home/neutrino/.local/bin/tectonic
FONTS := $(wildcard fonts/*.ttf)

.PHONY: all
all: main.pdf

main.pdf: main.tex $(FONTS)
	$(TECTONIC) -C --keep-logs main.tex
