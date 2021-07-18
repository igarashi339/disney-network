from pykml import parser
from geopy.distance import geodesic
import copy
import sys
import json
import decimal
import simplekml

INPUT_DIR_PATH = ""
OUTPUT_DIR_PATH = ""
SAME_NODE_THRESHOLD = 5 # 同じノードとみなすしきい値[m]


def read_kml():
    """
    kmlファイルを読み込んでリンクの形状点列を返す。

    返却値の形式：
        [[(lat, lon), (lat, lon), ...], [],... ]
    """
    links = []
    with open(INPUT_DIR_PATH + "/disney-sea-network-org.kml", "r", encoding="utf-8") as f:
        root = parser.parse(f).getroot()
        placemarks = root.Document.Placemark
        for placemark in placemarks:
            if "link" in placemark.name.__str__():
                link = []
                link_coords = placemark.LineString.coordinates.__str__().replace("\n","").replace("\t","")
                lines = link_coords.split(" ")
                for line in lines:
                    if line == "":
                        continue
                    lon, lat, alt = line.split(",")
                    link.append((lat, lon))
                links.append(link)
    return links


def same_node(coord1, coord2):
    distance = geodesic(coord1, coord2).m
    return distance < SAME_NODE_THRESHOLD


def make_nodes_and_links(org_links):
    """
    端点の接続されていないリンク集合から、接続されたリンク集合及びノード集合を算出する。
    """
    nodes = []
    links = copy.deepcopy(org_links)
    for i, link in enumerate(links):
        org_node = link[0]
        dst_node = link[-1]
        org_find_flag = False
        for node in nodes:
            # リンク端点が既に登録されている場合は緯度経度を差し替える
            if same_node(node, org_node):
                org_find_flag = True
                links[i][0] = node
                break
        # 登録されていない場合は新規追加
        if not org_find_flag:
            nodes.append(org_node)
        dst_find_flag = False
        for node in nodes:
            if same_node(node, dst_node):
                dst_find_flag = True
                links[i][-1] = node
                break
        if not dst_find_flag:
            nodes.append(dst_node)
    return nodes, links


def find_node(coord, nodes):
    for i, node in enumerate(nodes):
        if coord == node:
            return i
    print("system error! ...")
    sys.exit()


def calc_length(coords):
    prev_lat = -1
    prev_lon = -1
    distance = 0
    for coord in coords:
        lat = coord[0]
        lon = coord[1]
        if prev_lat == -1:
            prev_lat = lat
            prev_lon = lon
            continue
        distance += geodesic((lat, lon), (prev_lat, prev_lon)).m
        prev_lat = lat
        prev_lon = lon
    return distance


def make_objects(org_nodes, org_links):
    # nodes
    nodes = []
    for i, org_node in enumerate(org_nodes):
        nodes.append({
            "node_id": i,
            "lat": org_node[0],
            "lon": org_node[1]
        })

    # links
    links = []
    for i, org_link in enumerate(org_links):
        links.append({
            "link_id": i,
            "org_node_id": find_node(org_link[0], org_nodes),
            "dst_node_id": find_node(org_link[-1], org_nodes),
            "length": calc_length(org_link),
            "coords": org_link
        })
    return nodes, links


def dump_nodes(node_obj_list):
    with open(OUTPUT_DIR_PATH + "nodes.json", "w", encoding="utf-8") as f:
        json.dump({"nodes": node_obj_list}, f, ensure_ascii=False, indent=4)


def dump_links(link_obj_list):
    with open(OUTPUT_DIR_PATH + "links.json", "w", encoding="utf-8") as f:
        json.dump({"links": link_obj_list}, f, ensure_ascii=False, indent=4)


def dump_spots(spot_obj_list):
    with open(OUTPUT_DIR_PATH + "spots.json", "w", encoding="utf-8") as f:
        json.dump({"spots": spot_obj_list}, f, ensure_ascii=False, indent=4)


def calc_nearst_node(coord, node_obj_list):
    nearest_node_id = -1
    nearest_distance = decimal.Decimal('inf')
    for node in node_obj_list:
        node_coord = (node["lat"], node["lon"])
        distance = geodesic(coord, node_coord).m
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_node_id = node["node_id"]
    return nearest_node_id


def make_spot_obj_list(node_obj_list):
    with open(INPUT_DIR_PATH + "/spots.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)
        spot_obj_list = []
        for i, spot in enumerate(json_data["spots"]):
            coord = (spot["lat"], spot["lon"])
            new_obj = {
                "spot_id": i,
                "name": spot["name"],
                "short-name": spot["short-name"],
                "lat": spot["lat"],
                "lon": spot["lon"],
                "type": spot["type"],
                "nearest_node_id": calc_nearst_node(coord, node_obj_list)
            }
            if spot.get("play-time"):
                new_obj["play-time"] = spot["play-time"]
            if spot.get("url"):
                new_obj["url"] = spot["url"]
            spot_obj_list.append(new_obj)
        return spot_obj_list


def make_network_kml(link_obj_list, node_obj_list, spot_obj_list):
    kml = simplekml.Kml()
    for link in link_obj_list:
        ls = kml.newlinestring()
        ls.coords = [(lon, lat) for (lat, lon) in link["coords"]]
        ls.style.linestyle.color = simplekml.Color.springgreen
        ls.style.linestyle.width = 3
    kml.save(OUTPUT_DIR_PATH + "disney-sea-network.kml")


def make_spots_kml(spot_obj_list):
    kml = simplekml.Kml()
    spot_color_map = {
        "attraction": simplekml.Color.yellow,
        "restaurant": simplekml.Color.green,
        "shop": simplekml.Color.orange,
        "place": simplekml.Color.red,
        "show": simplekml.Color.hotpink
    }
    for spot in spot_obj_list:
        pnt = kml.newpoint(name=spot["name"])
        pnt.coords = [(spot["lon"], spot["lat"])]
        pnt.style.iconstyle.color = spot_color_map[spot["type"]]
    kml.save(OUTPUT_DIR_PATH + "disney-sea-spots.kml")


def main():
    org_links = read_kml()
    nodes, links = make_nodes_and_links(org_links)
    node_obj_list, link_obj_list = make_objects(nodes, links)
    spot_obj_list = make_spot_obj_list(node_obj_list)
    dump_nodes(node_obj_list)
    dump_links(link_obj_list)
    dump_spots(spot_obj_list)
    make_network_kml(link_obj_list, node_obj_list, spot_obj_list)
    make_spots_kml(spot_obj_list)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("error! three arguments required")
        sys.exit()
    INPUT_DIR_PATH = sys.argv[1]
    OUTPUT_DIR_PATH = sys.argv[2]
    main()
