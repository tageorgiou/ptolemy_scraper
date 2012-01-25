from urllib2 import Request, urlopen
import json

buildingcoords = {}

buildings = open("buildinglist").read().split('\n')
for building in buildings:
    try:
        r = Request(url="http://whereis.mit.edu/search?type=query&q=%s&output=json"
                % building)
        response = urlopen(r)
        j = json.load(response)
        d = {}
        d['lon'] = j[0]['long_wgs84']
        d['lat'] = j[0]['lat_wgs84']
        buildingcoords[building] = d
    except Exception as e:
        pass

print json.dumps(buildingcoords)
