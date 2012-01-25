import json
buildingdb = json.load(open("buildingcoords.json"))
aplist = filter(lambda l: len(l) == 2, map(lambda l: l.split(","),
    open("aps.csv").read().split('\n')[1::]))
fout = open("aplist.csv","w")
fout.write("bssid, building, floor, lat, lon\n")
for aplocation, bssid in aplist:
    try:
        building = aplocation.split("-")[0].upper()
        if building[0] == 'M':
            building = building[1::]
        floor = aplocation.split("-")[1][0]
        lat = buildingdb[building]['lat']
        lon = buildingdb[building]['lon']
        fout.write("%s,%s,%s,%s,%s\n" % (bssid, building, floor, lat, lon))
    except Exception as e:
        print e
