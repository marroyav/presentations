TECTONIC ?= tectonic
LATEXMK ?= latexmk
SOURCES := main.tex deck-style.tex $(wildcard figures/*.tex fonts/*.ttf)

.PHONY: all rebuild latexmk
all: main.pdf

main.pdf: $(SOURCES)
	$(TECTONIC) -C --keep-logs --synctex main.tex

rebuild:
	$(TECTONIC) -C --keep-logs --synctex main.tex

latexmk:
	$(LATEXMK) -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
