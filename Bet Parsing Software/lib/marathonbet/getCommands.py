#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import codecs
import sys
from splinter import Browser


def getSubstr(str, toFind, endSymbol):
	res = ''
	ind = str.find(toFind)
	if ind == -1 :
		res = 'no'
	else :
		ind += len(toFind)
		#if (ind >= len(str)):
		#		print "index out of range"
		#		print str
		#		raw_input('waiting')
		while str[ind] != endSymbol :
			res += str[ind]
			ind += 1
			#if (ind >= len(str)):
			#	print "index out of range"
			#	print str
			#	raw_input('waiting')
	
	#delete space symbols
	#res.encode('utf8')
	return res.strip()
def getEvents(str):

	commands = []
	toFind = 'first member-area '
	ind = str.find(toFind)
	while (ind > 0):
		strForSearch = str[ind : ind + 900]
		#get home command
		strHome = getSubstr(strForSearch, '1.</b>\n <div class="member-name nowrap" data-ellipsis="{}">', '<')
		#get away command
		strAway = getSubstr(strForSearch, '2.</b>\n <div class="member-name nowrap" data-ellipsis="{}">', '<')
		if strHome == 'no':
			strHome = getSubstr(strForSearch, '1.</b>\n <div class="today-member-name nowrap" data-ellipsis="{}">', '<')
			strAway = getSubstr(strForSearch, '2.</b>\n <div class="today-member-name nowrap" data-ellipsis="{}">', '<')

		commands.append(strHome)
		commands.append(strAway)		
		ind = str.find(toFind, ind + 900)
		
	storeCommands(commands)

	return 


def storeCommands(commands):
	oldCommands = open('marathonbet_commands.txt', 'r').readlines()
	for c in oldCommands :
		c = c[:-1]
		commands.append(c)
	
	commands = list(set(commands))
	f = open('marathonbet_commands.txt', 'w')
	for c in commands : f.write(c + "\n")
	f.close()
	return

def main():

	browser = Browser('phantomjs') #chrome phantomjs
	browser.visit('http://www.betmarathon.com/en/popular/Football/')
	eventsContainerHTML = browser.find_by_id("container_EVENTS").first.html
	browser.quit()

	getEvents(eventsContainerHTML)
	return

main()