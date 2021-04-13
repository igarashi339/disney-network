import simplekml
import codecs

FILE_PATH = "../../static_data/sea/disney-sea-network.kml"

def read_kml():
    ifs = codecs.open(FILE_PATH, "r", "utf-8")
    data = ifs.read()
    links = []
    for row in data.splitlines():
        row = row.strip()
        if "<" in row:
            continue
        elems = row.split(" ")
        line = []
        for elem in elems:
            lon, lat, alt = elem.split(",")
            line.append((lat, lon))
        links.append(line)
    return links


def main():
    links = read_kml()
    ofs = codecs.open("links.csv", "w", "utf-8")
    for link in links:
        print_str = ""
        for line in link:
            print_str += (str(line[0]) + "," + str(line[1]) + ",")
        print_str = print_str.rstrip(",")
        ofs.write(print_str + "\n")

if __name__ == "__main__":
    main()