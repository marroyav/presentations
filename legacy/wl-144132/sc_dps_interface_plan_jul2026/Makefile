TEX = main.tex
PDF = main.pdf

.PHONY: all clean review

all: $(PDF)

$(PDF): $(TEX)
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error $(TEX)

review: $(PDF)
	mkdir -p /tmp/sc-dps-interface-plan-review
	pdftoppm -png -r 120 $(PDF) /tmp/sc-dps-interface-plan-review/slide

clean:
	latexmk -C $(TEX)
