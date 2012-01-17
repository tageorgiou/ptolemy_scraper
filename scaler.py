from math import sin, cos, pi
from decimal import Decimal

inlines = open("out.txt").read().split('\n')
y0 = Decimal("42.35985824391845")
x1 = Decimal("-71.09019908580467")
y1 = Decimal("42.35875655158723")
x0 = Decimal("-71.09222065156197")
w = 10200.0
h = 6600.0
xc = (x0+x1)/2
yc = (y0+y1)/2
rot = (66.087025) / 180.0 * pi
#rot = 0

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

def rotatePoint(point, origin, radians):
    pointx, pointy = point
    originx, originy = origin
    displacementx = pointx - originx
    displacementy = pointy - originy
    pointx = displacementx * Decimal(cos(radians)) + displacementy * \
            Decimal(sin(radians))
    pointy = displacementy * Decimal(cos(radians)) - displacementx * \
        Decimal(sin(radians))
    return (pointx + originx, pointy + originy)

#for line in inlines:
#    ldata = line.split(" ")
#    if len(ldata) != 3:
#        continue
#    room = ldata[0]
#    x = ldata[1]
#    y = ldata[2]
#    gpsx = (x1-x0) * Decimal(float(x) / w) + x0
#    gpsy = (y1-y0) * Decimal(float(y) / h) + y0
#    gpsx, gpsy = rotatePoint((gpsx, gpsy), (xc, yc), rot)
#    kmlout.write("""
#    <Placemark>
#        <name>%s</name>
#        <Point>
#            <coordinates>%s,%s</coordinates>
#        </Point>
#    </Placemark>
#    """ % (room + "a%s,%s" % (x,y) , str(gpsx), str(gpsy)))

room = "217A"
x = "1281"
y = "1941"
print (float(x) / w)
print (float(y) / h)
gpsx = (x1-x0) * Decimal(float(x) / w) + x0
gpsy = (y1-y0) * Decimal(float(y) / h) + y0
#gpsx, gpsy = rotatePoint((gpsx, gpsy), (xc, yc), rot)
print gpsx
print gpsy

kmlout.write("""
<Placemark>
    <name>ne</name>
    <Point>
        <coordinates>%s, %s</coordinates>
    </Point>
</Placemark>
""" % (x0, y0))

kmlout.write("""
<Placemark>
    <name>ner</name>
    <Point>
        <coordinates>%s, %s</coordinates>
    </Point>
</Placemark>
""" % rotatePoint((x0,y0), (xc, yc), rot))

kmlout.write("""
<Placemark>
    <name>sw</name>
    <Point>
        <coordinates>%s, %s</coordinates>
    </Point>
</Placemark>
""" % (x1, y1))

kmlout.write("""
<Placemark>
    <name>swr</name>
    <Point>
        <coordinates>%s, %s</coordinates>
    </Point>
</Placemark>
""" % rotatePoint((x1,y1), (xc, yc), rot))

kmlout.write("""
        </Document>
    </kml>
    """)
