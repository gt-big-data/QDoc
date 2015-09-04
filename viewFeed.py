#!/usr/bin/env python
"""Testing script for visually inspecting RSS feeds (or any HTML page)."""
from urllib import urlopen
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Given a URL, display it prettified
if len(sys.argv) > 1:
	html = urlopen(sys.argv[1]).read()
	html = html.replace(u'\xa9', '')
	html = html.replace(u'\u2019', '')
	html = html.replace(u'\u201c', '')
	html = html.replace(u'\u201d', '')
	html = html.replace(u'\u2013', '')
	html = html.replace(u'\u2018', '')
	html = html.replace(u'\u2014', '')
	html = html.replace(u'\u2011', '')
	html = html.replace(u'\u200b', '')
	html = html.replace(u'\u20ac', '')
	soup = BeautifulSoup(html.encode('utf-8'), 'html.parser')
	print soup.prettify()
else:
	print 'Please provide URL'
