INPUT_PATH="./static_data/sea/disney-sea-network.kml"
OUTPUT_PATH="./data/"

.PHONY: gen_network
gen_network:
	python src/network/convert.py ${INPUT_PATH} ${OUTPUT_PATH}
