#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import codecs
from splinter import Browser

def main():
	t = time.time()
	browser = Browser('phantomjs')
	print "init browse ", (time.time() - t)
	browser.visit('http://sports.williamhill.com/bet/en-gb/betting/y/5/tm/1/Football.html')
	#browser.find_by_class('more-view').first.click()
	print "visit williamhill " , (time.time() - t)
	browser.execute_script("document.site.ajax_unexpanded_type('ip', '5664', '1', 'Match Betting')");
	#event = browser.find_by_css(".marketHolderCollapsed").first.click()
	
	#script = "document.site.ajax_unexpanded_type('ip', '5664', '1', 'Match Betting')"
	#browser.execute_script(script)
	time.sleep (5)
	event = browser.find_by_css(".marketHolderCollapsed").first
	#event = browser.find_by_id("ip_mkt_grp_tbl_5664_9d8a08d4b13c912153e27659829a27ad").first
	print "Printing result..."
	print event.html

main()
