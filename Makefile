all:
	mkdir -p build
	python generate-table.py
	python generate-figure.py
