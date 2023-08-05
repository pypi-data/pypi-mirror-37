#!/usr/bin/env python3

import fileinput
import html

# import re
# html_entities = re.compile(r"&#[^;]{1,7};")

def process(line):
    line = html.unescape(line)
    print(line, end = '')

    
for line in fileinput.input():
    process(line)

