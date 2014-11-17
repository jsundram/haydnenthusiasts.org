#!/usr/bin/python
import json
"""To get valid json, it's helpful to insert via 

    s = "triple-quoted string you want to insert"
    out = json.dumps(s)
    !echo $out | pbcopy

and pasting the result instead of copy/pasting directly.

#justsayin
"""

with open('data.json') as f:
    data = json.load(f)
    if not data:
        print "NO DATA"
    else:
        print "data! %s" % data.keys()
