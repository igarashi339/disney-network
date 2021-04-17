import simplekml
import json
import sys
from model import Graph
from dijkstra import Dijkstra

INPUT_PATH="./data/sea/"
OUTPUT_PATH="./"


def get_nodes():
    with open(INPUT_PATH + "nodes.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        return json_data["nodes"]


def get_nearest_node_id(spot_id_org, spot_id_dst):
    org_node_id = -1
    dst_node_id = -1
    with open(INPUT_PATH + "spots.json", "r",  encoding="utf-8") as f:
        json_data = json.load(f)
        for spot in json_data["spots"]:
            if spot_id_org == spot["spot_id"]:
                org_node_id = spot["nearest_node_id"]
            if spot_id_dst == spot["spot_id"]:
                dst_node_id = spot["nearest_node_id"]
        return org_node_id, dst_node_id


def write_route(route, output_file_path):
    kml = simplekml.Kml()
    linestring = kml.newlinestring(name="search result")
    linestring.coords = [(lon, lat) for (lat, lon) in route.coords]
    linestring.style.linestyle.color = simplekml.Color.orange
    linestring.style.linestyle.width = 8
    kml.save(output_file_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("error! three arguments are required.")
        sys.exit()
    spot_id_org = int(sys.argv[1])
    spot_id_dst = int(sys.argv[2])
    node_id_org, node_id_dst = get_nearest_node_id(spot_id_org, spot_id_dst)
    node_num = len(get_nodes())
    graph = Graph(node_num,INPUT_PATH + "/links.json")
    dijkstra = Dijkstra(graph)
    route = dijkstra.calc_shortest_path(node_id_org, node_id_dst)
    route.expand_myself(graph)
    print(route.cost)
    write_route(route, OUTPUT_PATH + "search_result.kml")