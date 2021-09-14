from loader import Loader
import itertools
import json
from model import Graph
from dijkstra import Dijkstra

INPUT_PATH="./data/sea/"
OUTPUT_PATH="./data/sea/"

if __name__ == "__main__":
    loader = Loader(INPUT_PATH)
    spots = loader.get_spots()
    node_num = len(loader.get_nodes())
    graph = Graph(node_num, INPUT_PATH + "/links.json")
    dijkstra = Dijkstra(graph)
    all_spot_routes = []
    for pair in itertools.combinations_with_replacement(spots, 2):
        org_spot_id = pair[0]["spot-id"]
        dst_spot_id = pair[1]["spot-id"]
        node_id_org, node_id_dst = \
            loader.get_nearest_node_id(org_spot_id, dst_spot_id)
        route = dijkstra.calc_shortest_path(node_id_org, node_id_dst)
        route.expand_myself(graph)
        print(str(pair[0]["spot-id"]) + "_" + str(pair[1]["spot-id"]) + ": OK")
        all_spot_routes.append({
            "org-spot-id": org_spot_id,
            "dst-spot-id": dst_spot_id,
            "distance": route.cost,
            "nodes": route.node_list
        })
        if org_spot_id == dst_spot_id:
            continue
        all_spot_routes.append({
            "org-spot-id": dst_spot_id,
            "dst-spot-id": org_spot_id,
            "distance": route.cost,
            "nodes": list(reversed(route.node_list))
        })
    with open(OUTPUT_PATH + "all_spot_pair_routes.json", "w", encoding="utf-8") as f:
        json.dump({"all_spot_pair_routes": all_spot_routes}, f, ensure_ascii=False, indent=4)