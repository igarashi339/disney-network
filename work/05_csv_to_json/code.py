import json
import codecs

def convert_attractions():
    attractions = []
    with codecs.open("input/attractions.csv", "r", "utf-8") as f:
        data = f.read()
        for row in data.splitlines():
            name, lat, lon = row.split(",")
            attraction = {
                "name": name,
                "lat": lat,
                "lon": lon
            }
            attractions.append(attraction)
    with open("attractions.json", "w", encoding="utf-8") as file:
        json.dump({"attractions":attractions}, file, ensure_ascii=False, indent=4)

def convert_links():
    links = []
    with open("input/links.csv") as f:
        data = f.readlines()
        links = []
        for row in data:
            elems = row.split(",")
            org_id = elems[1]
            dst_id = elems[2]
            length = elems[3]
            coords = []
            coords_index = 0
            for i, elem in enumerate(elems):
                if i == 0 or i == 1 or i == 2 or i == 3:
                    continue
                if elem == "":
                    break
                if coords_index%2 == 0:
                    lat = elem
                    coords_index += 1
                else:
                    lon = elem
                    coords.append((lat, lon))
                    coords_index += 1
            link = {
                "org_node_id": org_id,
                "dst_node_id": dst_id,
                "length": length,
                "coords": coords
            }
            links.append(link)
        with open("links.json", "w") as f:
            json.dump({"links": links}, f,ensure_ascii=False, indent=4)

def convert_nodes():
    nodes = []
    with open("input/nodes.csv") as f:
        data = f.readlines()
        for row in data:
            _, lat, lon = row.split(",")
            node = {
                "lat": lat,
                "lon": lon.strip("\n")
            }
            nodes.append(node)
    with open("nodes.json", "w") as f:
        json.dump({"nodes": nodes}, f, ensure_ascii=False, indent=4)


def main():
    convert_attractions()
    convert_links()
    convert_nodes()

if __name__ == "__main__":
    main()