class Attraction:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon


class CostElement:
    def __init__(self, cost, link):
        pass


class Link:
    def __init__(self, link_id, org_node_id, dst_node_id, length):
        self.link_id = link_id
        self.org_node_id = org_node_id
        self.dst_node_id = dst_node_id
        self.length = length


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
        self.attractions_path = base_path + "attractions.csv"
        self.link_shapes_path = base_path + "link_shapes.csv"
        self.links.csv = base_path + "links.csv"
        self.nodes.csv = base_path + "nodes.csv"
        self.attractions = []
        self.links = []
        self.nodes = []

    def load_attractions(self):
        pass

    def load_links(self):
        pass

    def load_nodes(self):
        pass

    def load_files(self):
        pass