import cv
import subprocess
import sys

if len(sys.argv) < 2:
    print "Must specify file argument"
    sys.exit(1)
filename = sys.argv[1]
fileprefix = filename[:-4]
floornumber = fileprefix[-1]
print floornumber

floorplan = cv.LoadImageM(filename, cv.CV_LOAD_IMAGE_UNCHANGED)
template = cv.LoadImageM("roomcircletemplate.png", cv.CV_LOAD_IMAGE_UNCHANGED)

resultmat = cv.CreateMat(floorplan.rows - template.rows + 1, floorplan.cols -
        template.cols + 1, cv.CV_32F)

cv.MatchTemplate(floorplan, template, resultmat, cv.CV_TM_SQDIFF)

minmax = cv.MinMaxLoc(resultmat)


minv = minmax[0]
maxv = minmax[1]
threshold = minv + 13000000

roomsfound = set()

fout = open("out_%s.txt" % fileprefix,"w")

def setSurroundingPoints(mat, coords, size):
    x = coords[1] - (size - 1) / 2
    y = coords[0] - (size - 1) / 2
    for i in range(0,size):
        for j in range(0,size):
            mat[x+i, y+j] = maxv

def outputCoords(coords, counter):
    width = template.cols - 40
    height = template.rows - 10
    crop = cv.CreateImage((width, height), 8, 1)
    region = cv.GetSubRect(floorplan, (coords[0] + 20, coords[1] + 5, width,
        height))
    cv.Copy(region, crop)
    cv.SaveImage("out%d.tiff" % counter, crop)
    subprocess.call(["tesseract", "out%d.tiff" % counter, "abc", "tessconfig"])
    subprocess.call(["cat", "abc.txt"])
    roomnumber = open("abc.txt").read().split('\n')
    if len(roomnumber) < 1:
        return True
    roomnumber = roomnumber[0].replace(' ','')
    if len(roomnumber) < 1: #make sure it's not an empty string
        return True
    if roomnumber in roomsfound:
        print roomnumber
        return False
    if roomnumber[0] != floornumber:
        return True
    roomsfound.add(roomnumber)
    fout.write("%s %d %d\n" % (roomnumber, coords[0] + template.cols / 2,
        coords[1] + template.rows / 2))
    return True

for i in range(0,100):
    item = cv.MinMaxLoc(resultmat)
    coords = item[2]
#    resultmat[coords[1], coords[0]] = maxv
    setSurroundingPoints(resultmat, coords, 5)
    print item[0]
    print coords
    if not outputCoords(coords, i):
        break
    #if item[0] > threshold:
    #    print "done"
    #    break
