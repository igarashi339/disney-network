import simplekml
from model import Graph
from dijkstra import Dijkstra


def write_route(route, output_file_path):
    kml = simplekml.Kml()
    linestring = kml.newlinestring(name="search result")
    linestring.coords = [(lon, lat) for (lat, lon) in route.coords]
    linestring.style.linestyle.color = simplekml.Color.lightgreen
    linestring.style.linestyle.width = 5
    kml.save(output_file_path)


if __name__ == "__main__":
    node_num = 104
    graph = Graph(node_num,"../../data/links.json")
    dijkstra = Dijkstra(graph)
    route = dijkstra.calc_shortest_path(0, 103)
    route.expand_myself(graph)
    print(route.cost)
    print(route.node_list)
    print(route.coords)
    write_route(route, "./search_result.kml")