#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import codecs
from splinter import Browser

def submitTimeZone(browser):
	res = browser.find_by_id("yesBtn")
	if (res != []):
		res.click()
		print "Time zone submitted"
	else:
		print "Without time zone"
	return

def main():
	t = time.time()
	browser = Browser('phantomjs')
	print "init browser", (time.time() - t)
	
	browser.visit('http://sports.williamhill.com/bet/en-gb/betting/y/5/tm/0/Football.html')
	submitTimeZone(browser)
	#browser.visit('http://petroclima.ru/')

	#browser.find_by_id("yesBtn").click()
	
	#f = codecs.open('html_new.out', 'w', encoding='utf-8')
	#f.write (browser.html)
	#browser.quit()
	#exit(
	#f = codecs.open('html_new.out', 'w', encoding='utf-8')
	#f.write(browser.html)
	bts = browser.find_by_id("ip_mkt_grp_994186").first
	print bts.html
	script = "document.site.ajax_unexpanded_type('ip', '6733', '0', 'Match Betting')"
	browser.execute_script(script)
	bts = browser.find_by_id("ip_row_6746483").first
	print "**********************************"
	print bts.html
	browser.quit()
	exit()
	
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
