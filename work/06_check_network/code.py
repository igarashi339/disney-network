import json

def main():
    nodes = []
    with open("nodes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for node in data["nodes"]:
            nodes.append((node["lat"], node["lon"]))
    with open("links.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        count = [0 for i in range(110)]
        for link in data["links"]:
            count[int(link["org_node_id"])] += 1
            count[int(link["dst_node_id"])] += 1
        for i, elem in enumerate(count):
            if elem == 1:
                print(str(i) + "," + nodes[i][0] + "," + nodes[i][1])


if __name__ == "__main__":
    main()