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
import datetime
import os

global_now = datetime.datetime.today()
global_year = global_now.year
global_month = global_now.month
global_day = global_now.day
global_hour = global_now.hour
global_min = global_now.minute
global_sec = global_now.second
log_file_name = "console"

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
			ThrowError(10, "main(): Регулярное выражение не смогло извлечь текст скрипта для рскрытия блока " + text[i])
		# appendToFile('scripts.out', res.group(1))
		scripts.append(res.group(1))
	logWrite(str(len(scripts)) + " extracted.")
	# executing scripts
	logWrite("Executing scripts...(it will take at least 20 seconds)")
	for i in range(len(scripts)):
		browser.execute_script(scripts[i])
	time.sleep(2*len(scripts))
	logWrite(str(len(scripts)) + " scripts executed.")

# извлекает из блока массив рядов
# input:
#	block is not html! it is an object
# output:
#	array of rows (they're objects!)
def extractRowsFromBlock(block):
	c = re.compile('class="rowOdd"[^>]*id="(ip_row_\d+)"');
	f = re.findall(c, block.html)
	rows = []			# результирующий массив всех извлеченных рядов данных
	if (len(f) == 0):		# ни одной строчки не найдено
		ThrowError(2, "extractRowsFromBlock(block): Регулярное выражение не смогло извлечь информацию о рядах данных. Программа не прерывается.")
	else:
		for i in range(len(f)):
			row = block.find_by_id(f[i])
			if row == None:			# ошибка! очень странная, никогда не должна возникать
				ThrowError(10, "extractRowsFromBlock(block): не удалось найти ряд по id = " + str(f[i]))
			else:
				rows.append(row)
	return rows
# извлекает необходимую информацию из ряда данных
# input:
#	row is not html! it's an object
# output:
#	array [datetime, array[cmd1, cmd2], link]
def extractInfoFromRow(row):
	dt = extractDateTimeFromRow(row.html)
	cmds = extractCmdNamesFromRow(row.html)
	if cmds[0] == "" or cmds[1] == "":
		ThrowError(10, "extractInfoFromRow(row): не пройдена проверка корректности имен команд. Программа прервана.")
	link = extractLinkFromRow(row.html)
	return [dt, cmds, link]
	
def extractLinkFromRow(row_html):
	link = ""
	c = re.compile('<a href="([^"]+)" title="More markets"')
	f = re.findall(c, row_html)
	if len(f) == 0:
		ThrowError(0, "extractLinkFromRow(row_html): ссылка не найдена. Программа не прервана.")
	else:
		link = f[0]
	return link

# !!! ТРЕБУЕТСЯ ИСПРАВЛЕНИЕ 2015 !!!
def extractDateTimeFromRow(row_html):
	y = 1000; mon = 1; d = 1; h = 0; mint = 0; sc = 0
	c = re.compile('<span[^>]+>(\d\d) ([a-zA-Z]{3})</span>')
	f = re.findall(c, row_html)
	if len(f) == 0:
		ThrowError(2, "extractDateTimeFromRow(row_html): дата не найдена. Программа не прервана.")
		c = re.compile('<a [^>]+>(Live[^<]+)</a>')
		f = re.findall(c, row_html)
		if len(f) == 0:
			c = re.compile('<td [^>]+>Today</td>')
			f = re.findall(c, row_html)
			if len(f) == 0:
				ThrowError(0, "extractDateTimeFromRow(row_html): дата не найдена. Программа не прервана.")
				y = 1000; mon = 1; d = 1
			else:
				y = global_year; mon = global_month; d = global_day
		else:			# было встречено Live At или Live In
			y = global_year; mon = global_month; d = global_day
		
	else:
		d = int(f[0][0])
		mon = mapMonth(f[0][1])
		y = 2015
	c = re.compile('(\d\d):(\d\d)')
	f = re.findall(c, row_html)
	if len(f) == 0:
		ThrowError(2, "extractDateTimeFromRow(row_html): время не найдено. Программа не прервана.")
		c = re.compile('<a [^>]+>(\d+) mins</a>')
		f = re.findall(c, row_html)
		if len(f) == 0:			# не найдено "3 mins"
			# это лайв матч, его необходимо пропустить
			ThrowError(2, "extractDateTimeFromRow(row_html): лайв матч. Пропущено.")
			h = 23; mint = 59; sc = 59
		else:				# матч начнется в течение нескольких минут
			# такие матчи мы тоже пропускаем
			ThrowError(2, "extractDateTimeFromRow(row_html): матч начнется очень скоро. Пропущено.")
			h = 0; mint = 59; sc = 59
	else:
		h = int(f[0][0])
		mint = int(f[0][1])
	return datetime.datetime(y, mon, d, h, mint, sc)

def trimCmdName(name):
	return re.sub('&nbsp;', '', name).strip()
# input:
#	returns array [cmd1, cmd2]
def extractCmdNamesFromRow(row_html):
	cmd1 = ""; cmd2 = ""
	c = re.compile('<span id="\d+_mkt_namespace">([^<]+) v ([^<]+)</span>')
	f = re.findall(c, row_html)
	if len(f) == 0:
		ThrowError(0, "extractCmdNamesFromRow(row_html): команды не найдены. Программа не прервана.")
	else:
		cmd1 = f[0][0]
		cmd2 = f[0][1]
	return [trimCmdName(cmd1), trimCmdName(cmd2)]

def mapMonth(s):
	if s == "Jan":
		return 1
	elif s == "Feb":
		return 2
	elif s == "Mar":
		return 3
	elif s == "Apr":
		return 4
	elif s == "May":
		return 5
	elif s == "Jun":
		return 6
	elif s == "Jul":
		return 7
	elif s == "Aug":
		return 8
	elif s == "Sep":
		return 9
	elif s == "Oct":
		return 10
	elif s == "Nov":
		return 11
	elif s == "Dec":
		return 12
	else:
		ThrowError(10, "mapMonth(s): строка s == " + s + " не соответствует ни одному образцу. Программа прервана.")
		return -1

def getInfo(allBlocks):
	logWrite("Extracting info from blocks...")
	info = []
	for i in range(len(allBlocks)):
		rows = extractRowsFromBlock(allBlocks[i])
		if len(rows) == 0:		# подозрительно на ошибку. в принципе такой ситуации быть не должно
			ThrowError(2, "getInfo(allBlocks): warning: массив rows пуст")
		else:
			for j in range(len(rows)):
				inform = extractInfoFromRow(rows[j])
				sec = inform[0].second		# seconds in datetime
				cmd1 = inform[1][0]
				cmd2 = inform[1][1]
				if cmd1 == "" or cmd2 == "":
					continue;
				if sec == 59:			# это означает, что матч необходимо пропустить, его анализ проводиться не будет
					continue;
				info.append(inform)
	logWrite(str(len(info)) + " rows (infos) extracted.")
	return info		
	#links = []; dates = []; cmds1 = []; cmds2 = []
	#info = []
	#c = re.compile('<a href="([^"]+)" title="More markets"')
	#for i in range(len(allBlocks)):
	#	block = allBlocks[i]
	#	rows = block.find_by_name('rowOdd')
	#	print len(rows)
	#	print rows
	#	quit()
	#	res = re.findall(c, allBlocks[i].html)
	#	if len(res) == 0:			# ошибка! не найдена ссылка на страницу с коэффициентами
	#		ThrowError(0, "main(): Не найдена ссылка на страницу с коэффициентами №" + str(i))
	#		continue;
	#	else:
	#		for j in range(len(res)):
	#			links.append(res[j])
	#			print res[j]
	#return links
		
def needToBePressed(block_html):
	text = block_html
	index = string.find(text, '<tbody>')
	return index <> -1

# severity == 0 - lowest level
# severity == 10 - highest level
def ThrowError(severity, text):
	if severity == 2:
		return
	print text
	if severity == 10:
		quit()

# печатает информацию в log-файл
def logWrite(text):
	if log_file_name == "console":
		print time.asctime()
		print text
	else:
		appendToFile(log_file_name, text)

# input:
#	sys.argv[1] - URL страницы, с которой начинается parse
#	sys.argv[2] - имя директории, в которую необходимо сохранять результаты работы скрипта
#	sys.argv[3] - имя используемого браузера
#	sys.argv[4] - имя log-файла; если указано "console" или ничего не указано, печатается в консоль
# output:
#	
def main():
	return_result = 0			# возвращаемое значение процедуры main()
	if (len(sys.argv) < 2):
		ThrowError(10, "No parameters found in sys.argv. Interrupted")
	link_to_site = sys.argv[1]
	if len(sys.argv) > 2:
		folder_name = sys.argv[2]
	else:
		folder_name = "0"
	if len(sys.argv) > 3:
		browser_name = sys.argv[3]
	else:
		browser_name = "phantomjs"
	if len(sys.argv) > 4:
		log_file_name = sys.argv[4]
	else:
		log_file_name = "console"
	try:
		os.makedirs(folder_name)
	except OSError:
		pass
	logWrite("William Hill parsing started...")
	browser = Browser(browser_name)
	logWrite("Loading main page...")
	browser.visit(link_to_site)
	logWrite("Main page loaded.")
	submitTimeZone(browser)
	
	logWrite("Extracting IDs...")
	text = browser.html
	c = re.compile('"ip_type_\d+"')
	ip_types = re.findall(c, text)
	if (len(ip_types) == 0):		# ошибка! регулярное выражение ничего не нашло
		ThrowError(10, "main(): Ни один экземпляр 'ip_type' не был найден регулярным выражением. Программа прервана.")
	#logWrite("Regex used in")
	
	ids = []				# массив id событий
	for i in range(len(ip_types)):
		s = ip_types[i]
		c = re.compile('\d+')
		id = re.findall(c, s)
		if (len(id) != 1):		# ошибка! в каждом ip_type должно содержаться единственное число
			ThrowError(10, "main(): В ip_type == " + str(s) + " (№" + str(i) + " найдено не одно число!")
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
	info = getInfo(allBlocks)			# allBlocks уже обновленные
	for i in range(len(info)):
		appendToFile(folder_name + "/dates.out", str(info[i][0]) + "\n")
		appendToFile(folder_name + "/cmds.out", info[i][1][0] + "\n" + info[i][1][1] + "\n")
		appendToFile(folder_name + "/links.out", info[i][2] + "\n")
	browser.quit()
	logWrite("William Hill parser is initialized.")
	return return_result
main()
