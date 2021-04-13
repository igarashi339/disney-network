import simplekml
import codecs

SPOT_FILE_PATH = "../../static_data/sea/atractions.csv"
LINK_FILE_PATH = "../../static_data/sea/link.csv"

def read_spot_csv():
    ifs = codecs.open(SPOT_FILE_PATH, "r", "utf-8")
    next(ifs)
    data = ifs.read()
    ret_list = []
    for row in data.splitlines():
        name, lat, lon = row.split(",")
        ret_list.append((name, lat, lon))
    return ret_list

def make_spot_kml():
    kml = simplekml.Kml()
    atractions_data = read_spot_csv()
    for data in atractions_data:
        kml.newpoint(name=data[0], coords=[(data[2], data[1])])
    kml.save("spots.kml")

def main():
    make_spot_kml()


if __name__ == "__main__":
    main()