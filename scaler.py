from decimal import Decimal
import json
import room_mapping

#MIT lat lon scale factor
scalefactor = Decimal(1/1.35)

#xml reader
import sys
if len(sys.argv) < 2:
    print """Invalid number of arguments
    example (building):
    python scaler.py 34
    """
    sys.exit(1)
building = sys.argv[1]
coordfile = open("coords/%s" % building).read().split("\n")
bottomfloor,topfloor = map(int, coordfile[0].split(" ")[1:3])

A = map(Decimal, coordfile[1].split(" ")[0].split(","))
A[1] *= scalefactor
B = map(Decimal, coordfile[2].split(" ")[0].split(","))
B[1] *= scalefactor
U = (B[0]-A[0], B[1]-A[1])
V = (B[1]-A[1], A[0]-B[0])
floorMapa = {}
floorMapb = {}
for floor in range(bottomfloor, topfloor + 1):
    la = coordfile[(floor - bottomfloor + 1) * 3 + 1]
    lb = coordfile[(floor - bottomfloor + 1) * 3 + 2]
    a = map(Decimal,la.split(","))
    b = map(Decimal,lb.split(","))
    floorMapa[floor] = a
    floorMapb[floor] = b

#sys.exit(1)
#dom = minidom.parse(open("%s.kml"%building))
#y0 = Decimal(dom.getElementsByTagName("north")[0].firstChild.wholeText)
#x1 = Decimal(dom.getElementsByTagName("east")[0].firstChild.wholeText)
#y1 = Decimal(dom.getElementsByTagName("south")[0].firstChild.wholeText)
#x0 = Decimal(dom.getElementsByTagName("west")[0].firstChild.wholeText)
#rot = \
#        float(Decimal(dom.getElementsByTagName("rotation")[0].firstChild.wholeText)) \
#    / 180.0 * pi

w = 10200.0
h = 6600.0
#xc = (x0+x1)/2
#yc = (y0+y1)/2
yibc = 3056 #centerpoint of building in image
xibc = w/2
floorprefix = building + "-"
floorrange = range(bottomfloor, topfloor + 1)
filename = "out_" + building + "_%d.txt"
#buildingcoords = json.load(open("buildingcoords.json"))[building]
mapping = room_mapping.getMapping(building)


#rot = 0
inlines = []
for i in floorrange:
    inlines += open(filename % i).read().split('\n')

def rotatePoint(point, origin, radians):
    pointx, pointy = point
    originx, originy = origin
    displacementx = pointx - originx
    displacementy = pointy - originy
    pointx = displacementx * Decimal(cos(radians)) + Decimal(scalefactor) * displacementy * \
            Decimal(sin(radians))
    pointy = displacementy * Decimal(cos(radians)) - Decimal(1/scalefactor) * displacementx * \
        Decimal(sin(radians))
    return (pointx + originx, pointy + originy)

#x0, y0 = rotatePoint((x0,y0), (xc, yc), -rot)
#x1, y1 = rotatePoint((x1,y1), (xc, yc), -rot)

kmlout = open("kmlout.kml","w")

kmlout.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns = "http://earth.google.com/kml/2.1">
  <Document>
    <Style id="restaurantStyle">
      <IconStyle id="restuarantIcon">
      <Icon>
        <href>http://maps.google.com/mapfiles/kml/pal2/icon63.png</href>
      </Icon>
      </IconStyle>
    </Style>
    <Style id="barStyle">
      <IconStyle id="barIcon">
      <Icon>
        <href>http://maps.google.com/mapfiles/kml/pal2/icon27.png</href>
      </Icon>
      </IconStyle>
      </Style>
""")


def outputKml(kmlout, name, gpsx, gpsy):
    kmlout.write("""
    <Placemark>
        <name>%s</name>
        <Point>
            <coordinates>%s,%s</coordinates>
        </Point>
    </Placemark>
    """ % (name, gpsy, gpsx))

def decToE6(dec):
    return int(dec * Decimal(1e6))

centerpoint = (Decimal(0.5), Decimal(0.5))

#shift latlonbox to center on buildingcoords
#xr, yr = rotatePoint((Decimal(xibc) / Decimal(w), Decimal(yibc) / Decimal(h)),
#    centerpoint, rot)
#gpsx = (x1-x0) * xr + x0
#gpsy = (y1-y0) * yr + y0
#dgpsx = Decimal(buildingcoords['lon']) - gpsx
#dgpsy = Decimal(buildingcoords['lat']) - gpsy

#Project of a onto b
def getProjectionC(a,b):
    #a * b / |b|
    dp = a[0]*b[0] + a[1]*b[1]
    ma = (a[0]*a[0] + a[1]*a[1]).sqrt()
    mb = (b[0]*b[0] + b[1]*b[1]).sqrt()
    return dp / mb / ma

roompoints = {}

for line in inlines:
    ldata = line.split(" ")
    if len(ldata) != 3:
        continue
    room = floorprefix + ldata[0]
    if not room in mapping.keys():
        #print "%s not found" % room
        continue
    roomtype = mapping[room]
    x = Decimal(ldata[1])
    y = Decimal(ldata[2])
    floor = 0
    try:
        floor = int(ldata[0][0])
    except Exception as e:
        pass

    p = [x,y]
    fa = floorMapa[floor]
    fb = floorMapb[floor]
    fu = (fb[0]-fa[0],fb[1]-fa[1])
    fv = (fb[1]-fa[1],fa[0]-fb[0])
    #scale
    p[0] = p[0] - fa[0]
    p[1] = p[1] - fa[1]
#    c1 = getProjectionC(p,fa)
#    c2 = getProjectionC(p,fb)
##    c3 = getProjectionC(fb,fa) #linearly dependent
#    c1a = (c1 * fa[0], c1 * fa[1])
#    c2 -= getProjectionC(c1a,b)
#    print c3
#                  -(by px) + bx py           -(ay px) + ax py
#Out[5]= {{c1 -> -(----------------), c2 -> -(----------------)}}
#                  -(ay bx) + ax by            ay bx - ax by
    c1 = -(-fv[1] * p[0] + fv[0] * p[1]) / (-fu[1] * fv[0] + fu[0] * fv[1])
    c2 = -(-fu[1] * p[0] + fu[0] * p[1]) / (fu[1] * fv[0] - fu[0] * fv[1])

    print c1,c2

    gpslat = c1 * U[0] + c2 * V[0] + A[0]
    gpslon = c1 * U[1] + c2 * V[1] + A[1]
    gpslon /= scalefactor
    #xr, yr = rotatePoint((Decimal(x) / Decimal(w), Decimal(y) / Decimal(h)),
    #    centerpoint, rot)
    #print xr, yr
    #gpsx = (x1-x0) * xr + x0 + dgpsx
    #gpsy = (y1-y0) * yr + y0 + dgpsy

    

    outputKml(kmlout, room, gpslat, gpslon)
    roompoint = {}
    roompoint['lat'] = decToE6(gpslat)
    roompoint['lon'] = decToE6(gpslon)
    roompoint['floor'] = floor
    roompoint['type'] = roomtype
    #room = "4-3" + ldata[0][1::]
    roompoints[room] = roompoint

jsonout = open("out%s.json" % building, "w")
json.dump(roompoints, jsonout)

kmlout.write("""
        </Document>
    </kml>
    """)
