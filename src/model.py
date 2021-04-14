class Link:
    def __init__(self):
        self.coords = []
        self.length = Graph.INVALID_COST


class Graph:
    INVALID_COST = -1

    def __init__(self, node_num):
        self.node_num = node_num
        # node_id x node_id -> Link
        self.link_matrix = [ [ Link() ] * self.node_num for _ in range(self.node_num) ]

    def load_link_matrix(self, links_path, link_shapes_path):
        # links
        with open(links_path) as f:
            data = f.read()
            for row in data.splitlines():
                _, org_node_id, dst_node_id, length = row.split(",")
                self.link_matrix[org_node_id][dst_node_id].
        # link_shapes
        pass


class Route:
    def __init__(self, node_list, cost):
        self.node_list = node_list
        self.cost = cost
        # 自身を構成する形状点列。描画用。
        self.coords = []

    def expand_myself(self, graph):
        pass

if __name__ == "__main__":
    graph = Graph(3)