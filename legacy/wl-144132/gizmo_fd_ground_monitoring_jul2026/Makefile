LATEXMK ?= latexmk

.PHONY: all clean

all: main.pdf

main.pdf: main.tex
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	$(LATEXMK) -C main.tex
