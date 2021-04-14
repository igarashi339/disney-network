import decimal
from model.py import Graph


class Dijkstra:
    INVALID_NODE_ID = -1
    INVALID_LABEL = decimal.Decimal('inf')

    def __init__(self, graph):
        self.graph = graph

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
        for node in range(self.graph.size()):
            pass
