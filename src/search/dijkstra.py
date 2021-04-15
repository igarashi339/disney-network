import decimal
import copy
from model import Graph, Route


class Dijkstra:
    INVALID_NODE_ID = -1
    INVALID_LABEL = decimal.Decimal('inf')

    def __init__(self, graph):
        self.graph = copy.deepcopy(graph)

    def calc_shortest_path(self, org_node_id, dst_node_id):
        """
        Dijkstra法で最短経路を求める。ノード数をNとすると、計算量はO(N^2)。
        ただし、org_nodeからdst_nodeに到達不能である場合はNoneを返す。
        """
        # ラベル確定済のノード
        label_fixed_nodes = []
        # 各ノードの暫定ラベル
        node_label_list = [Dijkstra.INVALID_LABEL for _ in range(self.graph.node_num)]
        node_label_list[org_node_id] = 0
        # トレース用情報
        prev_node_dict = [Dijkstra.INVALID_NODE_ID for _ in range(self.graph.node_num)]
        while dst_node_id not in label_fixed_nodes:
            min_cost_node = self.find_min_label_node(label_fixed_nodes, node_label_list)
            if min_cost_node == Dijkstra.INVALID_NODE_ID:
                return None
            label_fixed_nodes.append(min_cost_node)
            adjacent_nodes = self.get_adjacent_nodes(min_cost_node)
            for node in adjacent_nodes:
                if node in label_fixed_nodes:
                    continue
                new_cost = node_label_list[min_cost_node] + self.graph.cost(min_cost_node, node)
                if new_cost < node_label_list[node]:
                    prev_node_dict[node] = min_cost_node
                    node_label_list[node] = new_cost
        shortest_path_node_list = Dijkstra.trace(prev_node_dict, org_node_id, dst_node_id)
        shortest_path_cost = node_label_list[dst_node_id]
        return Route(shortest_path_node_list, shortest_path_cost)

    def find_min_label_node(self, label_fixed_nodes, node_label_list):
        """
        ラベルが未確定のノードのうちラベルが最も小さいものを返す。
        ただしラベルがInvalidのものしか残っていない場合はノード番号の無効値を返す。
        """
        min_node_index = Dijkstra.INVALID_NODE_ID
        min_cost = Dijkstra.INVALID_LABEL
        for node_index in range(self.graph.node_num):
            if node_index in label_fixed_nodes:
                continue
            target_cost = node_label_list[node_index]
            if target_cost == Dijkstra.INVALID_LABEL:
                continue
            if target_cost < min_cost:
                min_cost = target_cost
                min_node_index = node_index
        return min_node_index

    def get_adjacent_nodes(self, target_node_id):
        """
        target_nodeに隣接するすべてのノードIDを返す。
        """
        adjacent_nodes = []
        for node in range(self.graph.node_num):
            if self.graph.cost(target_node_id, node) != Graph.INVALID_COST:
                adjacent_nodes.append(node)
        return adjacent_nodes

    @staticmethod
    def trace(prev_node_dict, org_node_id, dst_node_id):
        """
        探索結果を元にスタートノードからゴールノードまでのノード列を求める。
        """
        shortest_path = [dst_node_id]
        target_node = dst_node_id
        assert prev_node_dict[org_node_id] == -1
        while prev_node_dict[target_node] != -1:
            target_node = prev_node_dict[target_node]
            shortest_path.append(target_node)
        shortest_path.reverse()
        return shortest_path

