from math import sin, cos, pi
from decimal import Decimal
import json

#bldg4
#y0 = Decimal("42.35985824391845")
#x1 = Decimal("-71.09019908580467")
#y1 = Decimal("42.35875655158723")
#x0 = Decimal("-71.09222065156197")
#rot = (-66.087025) / 180.0 * pi
#w = 10200.0
#h = 6600.0
#filename = "out.txt"
#floorprefix = "4-"

#bldg38
y0 = Decimal("42.36154159134831")
x1 = Decimal("-71.09122827659478")
y1 = Decimal("42.36050249583737")
x0 = Decimal("-71.09343248293267")
rot = (24.6202) / 180.0 * pi
w = 10200.0
h = 6600.0
floorrange = range(0,8)
filename = "out_38_%d.txt"
floorprefix = "38-"

scalefactor = 1/1.35
xc = (x0+x1)/2
yc = (y0+y1)/2
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
    """ % (name, gpsx, gpsy))

def decToE6(dec):
    return int(dec * Decimal(1e6))

roompoints = {}

for line in inlines[:]:
    inlines.append('3' + line[1::])

for line in inlines:
    ldata = line.split(" ")
    if len(ldata) != 3:
        continue
    room = floorprefix + ldata[0]
    x = ldata[1]
    y = ldata[2]
#    if x + y != "00":
#        continue
    centerpoint = (Decimal(0.5), Decimal(0.5))
    xr, yr = rotatePoint((Decimal(x) / Decimal(w), Decimal(y) / Decimal(h)),
        centerpoint, rot)
    print xr, yr
    gpsx = (x1-x0) * xr + x0
    gpsy = (y1-y0) * yr + y0
    outputKml(kmlout, room, gpsx, gpsy)
    roompoint = {}
    roompoint['lon'] = decToE6(gpsx)
    roompoint['lat'] = decToE6(gpsy)
    floor = 0
    try:
        floor = int(ldata[0][0])
    except Exception as e:
        pass
    roompoint['floor'] = floor
    #room = "4-3" + ldata[0][1::]
    roompoints[room] = roompoint

jsonout = open("out.json", "w")
json.dump(roompoints, jsonout)

kmlout.write("""
        </Document>
    </kml>
    """)
