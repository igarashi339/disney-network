import codecs
from geopy.distance import geodesic

class Link:
    def __init__(self):
        self.coords = []
        self.org_node = -1
        self.dst_node = -1

def same_node(coord1, coord2):
    distance = geodesic(coord1, coord2).m
    # 距離が3[m]以内なら同じ点と判断
    if distance < 3:
        return True
    return False

def read_csv():
    ifs = codecs.open("./input/link_coords_unmerged.csv", "r", "utf-8")
    data = ifs.read()
    links = []
    for row in data.splitlines():
        lines = []
        elems = row.split(",")
        for i in range(int(len(elems) / 2)):
            lat = elems[2 * i]
            lon = elems[2 * i + 1]
            lines.append((lat, lon))
        links.append(lines)
    return links

def output_nodes(nodes):
    ofs = codecs.open("nodes.csv", "w", "utf-8")
    for i, node in enumerate(nodes):
        ofs.write(str(i) + "," + node[0] + "," + node[1] + "\n")

def output_links(links):
    ofs = codecs.open("link_shapes.csv", "w", "utf-8")
    for i, link in enumerate(links):
        output_str = str(i) + ","
        for latlon in link:
            output_str += (latlon[0] + "," + latlon[1] + ",")
        output_str = output_str.strip(",")
        ofs.write(output_str + "\n")

def output_link_node_mapping(links, nodes):
    ofs = codecs.open("links.csv", "w", "utf-8")
    for i, link in enumerate(links):
        org_coord = link[0]
        dst_coord = link[-1]
        org_index = -1
        dst_index = -1
        for j, node in enumerate(nodes):
            if same_node(org_coord, node):
                org_index = j
            if same_node(dst_coord, node):
                dst_index = j
        ofs.write(str(i) + "," + str(org_index) + "," + str(dst_index) + "\n")

def main():
    links = read_csv()
    nodes = []
    for i, link in enumerate(links):
        # リンクの端点が既に登録されたノードかチェック
        org_node = link[0]
        dst_node = link[-1]
        org_find_flag = False
        for node in nodes:
            if same_node(node, org_node):
                org_find_flag = True
                links[i][0] = node
                break
        if org_find_flag == False:
            nodes.append(org_node)
        dst_find_flag = False
        for node in nodes:
            if same_node(node, dst_node):
                dst_find_flag = True
                links[i][-1] = node
                break
        if dst_find_flag == False:
            nodes.append(dst_node)
    output_link_node_mapping(links, nodes)
    output_nodes(nodes)
    output_links(links)


if __name__ == "__main__":
    main()