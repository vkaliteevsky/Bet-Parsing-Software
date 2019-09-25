#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import codecs
from splinter import Browser
import re

def writeToFile(fileName, text):
	codecs.open(fileName, 'w', encoding='utf-8').write(text)

def submitTimeZone(browser):
	t = time.time()
	output = ""
	print "Submitting time zone..."
	res = browser.find_by_id("yesBtn")
	if (res != []):
		res.click()
		output = "Time zone submitted. Done."
	else:
		output = "Without time zone. Done."
	#output += string(time.time() - t)
	print output
	
def main():
	print "William Hill parsing started..."
	t = time.time()
	browser = Browser('phantomjs')
	print "Loading main page..."
	browser.visit('http://sports.williamhill.com/bet/en-gb/betting/y/5/tm/0/Football.html')
	print "Done. Time", time.time() - t
	submitTimeZone(browser)
	
	text = browser.html
	t = time.time()
	c = re.compile('"ip_type_\d+"')
	ip_types = re.findall(c, text)
	print "Regex used in", time.time() - t
	s = ip_types[0]
	n = len(s) - 1
	while ((s[n] >= '0') and (s[n] <= '9')):
		n -= 1
	s = s[n:]
	print s
	#writeToFile("html.out", p)
	#t = time.time()
	#allBlocks = browser.find_by_id("ip_sport_0_types").first	# содердит все блоки с инфой
	#print time.time() - t
	
	browser.quit()
	print "William Hill parsed."
main()
