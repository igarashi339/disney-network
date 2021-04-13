import codecs
from geopy.distance import geodesic

def main():
    ifs = codecs.open("input/link_shapes.csv", "r", "utf-8")
    data = ifs.read()
    distance_list = []
    for row in data.splitlines():
        elems = row.split(",")
        elems.pop(0) # リンク番号はいらない
        distance = 0
        before_lat = -1
        after_lat = -1
        for i in range(int(len(elems)/2)):
            lat = elems[i * 2]
            lon = elems[i * 2 + 1]
            if before_lat == -1:
                before_lat = lat
                before_lon = lon
                continue
            distance += geodesic((lat, lon), (before_lat, before_lon)).m
            before_lat = lat
            before_lon = lon
        distance_list.append(distance)
    


if __name__== "__main__":
    main()