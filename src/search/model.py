import json
import copy


class Link:
    def __init__(self):
        self.coords = []
        self.length = Graph.INVALID_COST

    def __str__(self):
        return self.length.__str__() + " >> " + self.coords.__str__()


class Graph:
    INVALID_COST = -1

    def __init__(self, node_num, links_path):
        self.node_num = node_num
        # node_id x node_id -> Link
        self.link_matrix = [[Link() for i in range(self.node_num)] for j in range(self.node_num)]
        self.__load_link_matrix(links_path)

    def __load_link_matrix(self, links_path):
        with open(links_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            for link in json_data["links"]:
                org_node_id = int(link["org_node_id"])
                dst_node_id = int(link["dst_node_id"])
                length = float(link["length"])
                self.link_matrix[org_node_id][dst_node_id].length = length
                self.link_matrix[org_node_id][dst_node_id].coords = copy.deepcopy(link["coords"])
                # 無向グラフなので逆も登録する
                self.link_matrix[dst_node_id][org_node_id].length = length
                self.link_matrix[dst_node_id][org_node_id].coords = copy.deepcopy(link["coords"])
                self.link_matrix[dst_node_id][org_node_id].coords.reverse()

    def cost(self, node1, node2):
        return self.link_matrix[node1][node2].length


class Route:
    def __init__(self, node_list, cost):
        self.node_list = node_list
        self.cost = cost
        # 自身を構成する形状点列。描画用。
        self.coords = []

    def expand_myself(self, graph):
        for i in range(len(self.node_list) - 1):
            org_node = self.node_list[i]
            dst_node = self.node_list[i + 1]
            self.coords.extend(graph.link_matrix[org_node][dst_node].coords)


if __name__ == "__main__":
    graph = Graph("../data/sea/links.json")
    print(graph.link_matrix[0][1].__str__())