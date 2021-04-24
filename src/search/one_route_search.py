import simplekml
import sys
from model import Graph
from dijkstra import Dijkstra
from loader import Loader

INPUT_PATH="./data/sea/"
OUTPUT_PATH="./"


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
    loader = Loader(INPUT_PATH)
    node_id_org, node_id_dst = loader.get_nearest_node_id(spot_id_org, spot_id_dst)
    node_num = len(loader.get_nodes())
    graph = Graph(node_num,INPUT_PATH + "/links.json")
    dijkstra = Dijkstra(graph)
    route = dijkstra.calc_shortest_path(node_id_org, node_id_dst)
    route.expand_myself(graph)
    print("distance is " + str(route.cost) + "[m].")
    write_route(route, OUTPUT_PATH + "search_result.kml")