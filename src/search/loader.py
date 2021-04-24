import json


class Loader:
    def __init__(self, input_data_path):
        self.spots_json_path = input_data_path + "spots.json"
        self.links_json_path = input_data_path + "links.json"
        self.nodes_json_path = input_data_path + "nodes.json"

    def get_nearest_node_id(self, spot_id_org, spot_id_dst):
        org_node_id = -1
        dst_node_id = -1
        with open(self.spots_json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            for spot in json_data["spots"]:
                if spot_id_org == spot["spot_id"]:
                    org_node_id = spot["nearest_node_id"]
                if spot_id_dst == spot["spot_id"]:
                    dst_node_id = spot["nearest_node_id"]
            return org_node_id, dst_node_id

    def get_nodes(self):
        with open(self.nodes_json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return json_data["nodes"]

    def get_links(self):
        with open(self.links_json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return json_data["links"]

    def get_spots(self):
        with open(self.spots_json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            return json_data["spots"]