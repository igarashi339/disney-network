class Attraction:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon


class Node:
    def __init__(self, node_id, lat, lon):
        self.node_id = node_id
        self.lat = lat
        self.lon = lon
        self.out_links = []

    def calc_out_links(self, links):
        for link in links:
            if link.org_node_id == self.node_id or link.dst_node_id == self.node_id:
                self.out_links.append(link.link_id)


class Instance:
    def __init__(self, base_path):
        self.attractions_path = base_path + "attractions.json"
        self.links.csv = base_path + "links.json"
        self.nodes.csv = base_path + "nodes.json"
