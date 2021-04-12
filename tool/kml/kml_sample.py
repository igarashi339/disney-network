import simplekml
import codecs

FILE_PATH = "../../static_data/sea/atractions.csv"

def read_csv():
    ifs = codecs.open(FILE_PATH, "r", "utf-8")
    next(ifs)
    data = ifs.read()
    ret_list = []
    for row in data.splitlines():
        name, lat, lon = row.split(",")
        ret_list.append((name, lat, lon))
    return ret_list

def main():
    kml = simplekml.Kml()
    atractions_data = read_csv()
    for data in atractions_data:
        kml.newpoint(name=data[0], coords=[(data[2], data[1])])
    kml.save("sample.kml")


if __name__ == "__main__":
    main()