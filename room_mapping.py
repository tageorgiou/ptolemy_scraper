import json
def getMapping(building):
    mapping = json.load(open("mapping"))
    lines = open("reports/" + building).read().split("\n")
    roomdict = {}
    for line in lines:
        sline = line.split(" ")
        if len(sline) < 2:
            continue
        if not sline[0].startswith(building):
            continue
        room = sline[0]
        for key, val in mapping.iteritems():
            if key in line:
                #print "%s - %s" % (room, val)
                roomdict[room] = val
                break
    return roomdict
