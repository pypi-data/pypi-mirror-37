# from __future__ import print_function

import fileinput
import html

import sys
if sys.version_info.major < 3:
	raise EnvironmentError("require python version >=3 to run.")

# import re
# html_entities = re.compile(r"&#[^;]{1,7};")

def process(line):
    line = html.unescape(line)
    print(line, end = '')

    
def main():
    for line in fileinput.input():
        process(line)

if __name__ == '__main__':
    main()

