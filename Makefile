INPUT_PATH="./static_data/sea/"
OUTPUT_PATH="./data/"

.PHONY: gen_network
gen_network:
	python src/network/convert.py ${INPUT_PATH} ${OUTPUT_PATH}

.PHONY: search
search:
	python src/search/main.py 8 17