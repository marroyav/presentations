TECTONIC ?= /home/neutrino/.local/bin/tectonic
LATEXMK ?= latexmk
TEX := main.tex
PDF := main.pdf
FIGURES := \
	figures/01_bms_dcs_dps_boundary.pdf \
	figures/02_alarm_authority_hierarchy.pdf \
	figures/03_failure_response_map.pdf \
	logos/DUNElogo_color.png
FONTS := \
	fonts/LiberationSans-Regular.ttf \
	fonts/LiberationSans-Bold.ttf \
	fonts/LiberationSans-Italic.ttf \
	fonts/LiberationSans-BoldItalic.ttf

.PHONY: all tectonic latexmk clean

all: $(PDF)

$(PDF): $(TEX) $(FIGURES) $(FONTS)
	$(TECTONIC) -C --keep-logs $(TEX)

tectonic: $(PDF)

latexmk:
	$(LATEXMK) -xelatex -interaction=nonstopmode -halt-on-error -file-line-error $(TEX)

clean:
	@if command -v $(LATEXMK) >/dev/null 2>&1; then \
		$(LATEXMK) -C $(TEX); \
	else \
		rm -f main.aux main.log main.nav main.out main.snm main.toc main.xdv main.pdf; \
	fi
