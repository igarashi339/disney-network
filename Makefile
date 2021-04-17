INPUT_PATH="./static_data/sea/"
OUTPUT_PATH="./data/sea/"

.PHONY: convert
convert:
	python src/network/convert.py ${INPUT_PATH} ${OUTPUT_PATH}

.PHONY: search
search:
	python src/search/main.py 8 15