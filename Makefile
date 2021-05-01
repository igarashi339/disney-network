INPUT_PATH="./static_data/sea/"
OUTPUT_PATH="./data/sea/"

.PHONY: convert
convert:
	python src/network/convert.py ${INPUT_PATH} ${OUTPUT_PATH}

.PHONY: search
search:
	python src/search/one_route_search.py 0 5

.PHONY: all_search
all_search:
	python src/search/all_route_search.py