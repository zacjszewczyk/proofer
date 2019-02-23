#!/usr/bin/env python

import re 
string = """\
Here's how he got into her Windows 10 laptop--admittedly using only "off-the-shelf hacking tools":
"""

sentences = (len(re.findall("\.[^\w]?",line))+len(re.findall("[?!]",line))) or 1

i = 1
for word in re.split("(\s|--)", string):
    stripped = re.sub(r"^[\W]+", "", word.strip())
    stripped = re.sub(r"[\W]+$", "", stripped)

    if (len(stripped) == 0):
        continue
    
    print i,stripped.strip()
    i += 1