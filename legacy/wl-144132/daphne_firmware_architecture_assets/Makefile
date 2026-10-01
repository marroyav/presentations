PYTHON ?= python3

.PHONY: all render clean

all: render

render:
	$(PYTHON) scripts/render_architecture.py

clean:
	rm -f output/*.dot output/*.svg output/*.pdf output/*.png output/dependency_matrix.csv output/dependency_matrix.md
