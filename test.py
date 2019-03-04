#!/usr/bin/python

import re

line = """Once I decided to build some sort of platform, I started spelling out my design criteria. First, it had to turn the trunk and second row of seats into a flat area large enough to sleep on. I still wanted to use the second row of seats, though, so it had to fold back into the trunk, too. It also had to stay as short as possible, to maximize headroom. The space beneath it would house camp gear. I also wanted to use that space for a small camp kitchen, with an area for a [large cooler](https://orcacoolers.com/collections/75-quart/products/green-75-cooler) or [portable refrigerator](https://www.snomasterusa.com/product/classic-series-bdc-65-stainless-steel-acdc-fridgefreezer/) and a stove."""
word = "[portable"

start = line.find(word)
length = len(word)
end = start+length

print "Searched: '%s'" % line[start:end]
print "With ends: '%s'" % line[start-1:end+1]
print "Preceeding character: '%s'" % line[start-1]
print "After character: '%s'" % line[end]