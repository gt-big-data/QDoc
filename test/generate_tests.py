#!/usr/bin/env python
"""Generate tests for articles with known HTML and known good crawled content."""

import glob
import json

htmlFileNames = glob.glob('test/inputs/*.html')

with open('test/test_crawlContent.py.template') as f:
    globalTemplate = f.read()

for htmlFileName in htmlFileNames:
    print("Generating tests for %s" % htmlFileName)
    with open(htmlFileName) as f:
        html = f.read()
    jsonFileName = htmlFileName.replace('.html', '.json')
    with open(jsonFileName) as f:
        parsedData = json.load(f)

    testFile = globalTemplate.replace('%%PATH_TO_JSON%%', jsonFileName).replace('%%PATH_TO_HTML%%', htmlFileName)
    testName = htmlFileName.replace('test/inputs/', '').replace('.html', '')
    with open('test/test_crawlContent_%s.py' % testName, 'w') as f:
        f.write(testFile)
