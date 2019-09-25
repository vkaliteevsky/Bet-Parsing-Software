#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import codecs
from splinter import Browser
import re
import string
import thread
import subprocess
import sys

def writeToFile(fileName, text):
	codecs.open(fileName, 'w', encoding='utf-8').write(text)
def appendToFile(fileName, text):
	codecs.open(fileName, 'a', encoding='utf-8').write(text)

def submitTimeZone(browser):
	t = time.time()
	output = ""
	logWrite("Submitting time zone...")
	res = browser.find_by_id("yesBtn")
	if (res != []):
		res.click()
		output = "Time zone submitted. Done."
	else:
		output = "Without time zone. Done."
	time.sleep(5)
	logWrite(output)

def clickAllBlocks(allBlocks, browser):
	logWrite("Clicking on all blocks...")
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
		if res == None:			# ошибка! не найден скрипт для нажатия на блок
			ThrowError(1, "main(): Регулярное выражение не смогло извлечь текст скрипта для рскрытия блока " + text[i])
		# appendToFile('scripts.out', res.group(1))
		scripts.append(res.group(1))
	logWrite(str(len(scripts)) + " extracted.")
	# executing scripts
	logWrite("Executing scripts...(it will take at least 20 seconds)")
	for i in range(len(scripts)):
		browser.execute_script(scripts[i])
	if len(scripts) != 0:
		time.sleep(20)
	logWrite(str(len(scripts)) + " scripts executed.")

def getLinks(allBlocks):
	logWrite("Extracting links from blocks...")
	links = []
	c = re.compile('<a href="([^"]+)" title="More markets"')
	for i in range(len(allBlocks)):
		res = re.findall(c, allBlocks[i].html)
		if len(res) == 0:			# ошибка! не найдена ссылка на страницу с коэффициентами
			ThrowError(0, "main(): Не найдена ссылка на страницу с коэффициентами №" + str(i))
			continue;
		else:
			for j in range(len(res)):
				links.append(res[j])
				print res[j]
	logWrite(str(len(links)) + " links extracted.")
	return links
		
def needToBePressed(block_html):
	text = block_html
	index = string.find(text, '<tbody>')
	return index <> -1

def parsePage(link, i):
	browser = Browser('firefox')
	print "Process #", i, "..."
	browser.visit(link)
	print "Process #", i, "finished."
# severity == 0 - lowest level
# severity == 1 - highest level
def ThrowError(severity, text):
	print text
	if severity > 0:
		quit()

# печатает информацию в log-файл
def logWrite(text):
	print time.asctime()
	print text

# input:
#	sys.argv[1] - URL страницы, с которой начинается parse
# output:
#	
def main():
	return_result = 0			# возвращаемое значение процедуры main()
	if (len(sys.argv) < 2):
		ThrowError(1, "No parameters found in sys.argv. Interrupted")
	link_to_site = sys.argv[1]
	logWrite("William Hill parsing started...")
	browser = Browser('phantomjs')
	logWrite("Loading main page...")
	browser.visit(link_to_site)
	logWrite("Main page loaded.")
	submitTimeZone(browser)
	
	logWrite("Extracting IDs...")
	text = browser.html
	c = re.compile('"ip_type_\d+"')
	ip_types = re.findall(c, text)
	if (len(ip_types) == 0):		# ошибка! регулярное выражение ничего не нашло
		ThrowError(1, "main(): Ни один экземпляр 'ip_type' не был найден регулярным выражением. Программа прервана.")
	#logWrite("Regex used in")
	
	ids = []				# массив id событий
	for i in range(len(ip_types)):
		s = ip_types[i]
		c = re.compile('\d+')
		id = re.findall(c, s)
		if (len(id) != 1):		# ошибка! в каждом ip_type должно содержаться единственное число
			ThrowError(1, "main(): В ip_type == " + str(s) + " (№" + str(i) + " найдено не одно число!")
		# print id[0]
		ids.append(id[0])
	#for i in range(len(ids)):
	#	print i, ids[i]
	logWrite(str(len(ids)) + " ids extracted")
	logWrite("IDs extracted.")
	
	
	logWrite("Extracting data blocks...")
	allBlocks = []		# массив <div ...>...</div> всех событий (не в текстовом виде)
	
	for i in range(len(ids)):
		block = browser.find_by_id("ip_type_"+str(ids[i])).first
		if block == []:			# очень странная ошибка; по логике возникать не должна никогда
			ThrowError(0, "main(): Не найден блок по номеру ids[i] == " + str(ids[i]) + ". Программа продолжает исполнение.")
		allBlocks.append(block)
	l = len(allBlocks)
	logWrite(str(l) + " blocks extracted")
	logWrite("Data blocks extracted")
	
	clickAllBlocks(allBlocks, browser)
	
	# в этот момент вся необходимая информация загружена на страницу
	# далее следует только ее извлечение
	
	logWrite("Gathering info from pressing buttons...")
	links = getLinks(allBlocks)			# allBlocks уже обновленные
	for i in range(len(links)):
		appendToFile("links.out", links[i] + "\n")
	raw_input("Press any key...")
	browser.quit()
	logWrite("William Hill parser is initialized.")
	return return_result
main()
