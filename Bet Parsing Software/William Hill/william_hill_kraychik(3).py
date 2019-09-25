#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import codecs
from splinter import Browser
import re
import string

def writeToFile(fileName, text):
	codecs.open(fileName, 'w', encoding='utf-8').write(text)
def appendToFile(fileName, text):
	codecs.open(fileName, 'a', encoding='utf-8').write(text)

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
	time.sleep(5)
	print output, time.time() - t

def clickAllBlocks(allBlocks, browser):
	print "Clicking on all blocks..."
	# raw_input("Press any button to continue...")
	l = len(allBlocks)
	i = 0
	text = []		# массив блоков текста будет содержать только те блоки, на которые нужно кликать
	for i in range(l):
		# allBlocks[i].click()
		block_html = allBlocks[i].html
		toPress = needToBePressed(block_html)
		if toPress:
			text.append(block_html)
	c = re.compile('<thead onclick="([^"]+)">')
	scripts = []		# list of scripts
	for i in range(len(text)):
		res = re.search(c, text[i])
		# appendToFile('scripts.out', res.group(1))
		scripts.append(res.group(1))
	# executing scripts
	for i in range(len(scripts)):
		browser.execute_script(scripts[i])
	time.sleep(7)
	print "Done."

def needToBePressed(block_html):
	text = block_html
	index = string.find(text, '<tbody>')
	return index <> -1
	
def main():
	print "William Hill parsing started..."
	t = time.time()
	browser = Browser('firefox')
	print "Loading main page..."
	browser.visit('http://sports.williamhill.com/bet/en-gb/betting/y/5/tm/0/Football.html')
	print "Done. Time", time.time() - t
	#writeToFile('html.out', browser.html)
	submitTimeZone(browser)
	
	text = browser.html
	#writeToFile('html.out', text)
	t = time.time()
	c = re.compile('"ip_type_\d+"')
	ip_types = re.findall(c, text)
	print "Regex used in", time.time() - t
	
	print "Extracting IDs..."
	ids = []				# массив id событий
	for i in range(len(ip_types)):
		s = ip_types[i]
		c = re.compile('\d+')
		id = re.findall(c, s)
		print id[0]
		ids.append(id[0])
	#for i in range(len(ids)):
	#	print i, ids[i]
	print "IDs extracted."
	
	
	print "Extracting data blocks..."	
	#writeToFile("html.out", p)
	allBlocks = []		# массив <div ...>...</div> всех событий (не в текстовом виде)
	
	for i in range(len(ids)):
		block = browser.find_by_id("ip_type_"+str(ids[i])).first
		allBlocks.append(block)
	print "Data blocks extracted", time.time() - t		
	
	l = len(allBlocks)
	clickAllBlocks(allBlocks, browser)
	writeToFile('delete.out', allBlocks[23].html)
	print "Gathering info from pressing buttons..."
	allBlocks = []
	
	for i in range(len(ids)):
		block = browser.find_by_id("ip_type_"+str(ids[i])).first
		allBlocks.append(block)
		# appendToFile('blocks.out', block.html)
	print "Done."
	raw_input("Press any key...")
	browser.quit()
	print "William Hill parsed."
main()
