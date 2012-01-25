import sys, json
args = sys.argv[1:]
d = {}
for f in args:
    j = json.load(open(f))
    for key, val in j.iteritems():
        d[key] = val
print json.dumps(d)
