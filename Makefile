all:
	python generate-table.py

data:
	mkdir -p build
	python get-data.py
