#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen
import subprocess
import datetime
import time
from datetime import timedelta
import os
import sys

# инициализирует парсер
# input:
#	state_file - имя файла-состояния (путь к нему)
#	amount_of_pages - количество страниц, необходимых для инициализации
def initParser(state_file, amount_of_pages):
	now_old = datetime.datetime.today()
	for i in range(amount_of_pages):
		subprocess.call(["./init.py", "http://sports.williamhill.com/bet/en-gb/betting/y/5/tm/" + str(i) + "/Football.html", "running", "firefox", "log_file.txt"])
	now_new = datetime.datetime.today()
	writeState(state_file, [now_old, now_new, 0])
	return 0

# фильтрует матчи только по дате и извлекает информацию
# input:
#	min_minutes - обрабатывать те матчи, которые начинаются не ранее, чем через min_minutes минут
#	max_minutes - обрабатывать те матчи, которые начинаются не позднее, чем через max_minutes минут
#	amount - общее количество матчей, которых необходимо обработать
#	folder_name - имя папки, в которой будут храниться файлы с результатами работы программы
#	state_file - имя файла, в котором сохраняется последнее состояние работы парсера
#	input_folder - имя папки, в которой хранятся файлы с результатами работы метода initParser
def parseAll(min_minutes, max_minutes, amount, folder_name, state_file, input_folder):
	if input_folder[len(input_folder)-1] != "/":
		input_folder = input_folder + "/"
	if folder_name[len(folder_name)-1] != "/":
		folder_name = folder_name + "/"
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	links_file = open(input_folder + "links.out")
	dates_file = open(input_folder + "dates.out")
	cmds_file = open(input_folder + "cmds.out")
	counter = 0
	now = datetime.datetime.today()
	state = readState(state_file)			# состояние парсера (массив)
	last_index = state[len(state)-1]
	cur_line = 0				# впоследствии запишется в state.stf
	
	while last_index != 0:
		link = links_file.readline()
		if not link:
			links_file.close()
			dates_file.close()
			cmds_file.close()
			return
		dt_str = dates_file.readline()
		cmd1 = cmds_file.readline()
		cmd2 = cmds_file.readline()
		last_index = last_index - 1
		cur_line = cur_line + 1

	dt_str = dates_file.readline()
	link = links_file.readline()
	cmd1 = cmds_file.readline()
	cmd2 = cmds_file.readline()
	while link:
		if counter >= amount:
			break;
		dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S\n")
		delta_mins = (dt - now).total_seconds() / 60
		if min_minutes <= delta_mins and delta_mins <= max_minutes:		# фильтрация по времени
			subprocess.Popen(["node", "parse_page.js", link, folder_name + str(counter)])
			counter += 1
		dt_str = dates_file.readline()
		link = links_file.readline()
		cmd1 = cmds_file.readline()
		cmd2 = cmds_file.readline()
		cur_line += 1
	
	links_file.close()
	dates_file.close()
	cmds_file.close()
	modifyState(state_file, cur_line)			# обновляем состояние парсера

# сохраняет состояние парсера
# input:
#	init_start_datetime - время начала инициализации парсера
#	init_end_datetime - время конца инициализации парсера
#	link_number - номер строчки в файле ссылок (links.out),
#		      начиная с которой необходимо продолжать чтение файла (нумерация с 0)
# def writeState(init_start_datetime, init_end_datetime, link_number):

# input:
# lines - массив строк, которые необходимо записать в файл-состояние парсера
def writeState(state_file, lines):
	f = open(state_file, "w")
	text = ""
	for i in range(len(lines)):
		text = text + str(lines[i]) + "\n"
	text = text.strip()
	if len(lines) != 0 and text == "":
		return -1
	f.write(text)
	f.close()
	return 0
# читает состояние парсера
# input:
#	state_file - имя файла-состояния
# output:
#	выдает массив строк, хранящийся в файле-состоянии
def readState(state_file):
	f = open(state_file, "r")
	lines = []
	line = f.readline()
	while (line):
		lines.append(line)
		line = f.readline()
	f.close()
	return lines

# изменяет состояние парсера
# меняется ТОЛЬКО link_number, который ВСЕГДА записан последним в файле
def modifyState(state_file, new_link_number):
	lines = readState(state_file)
	if len(lines) == 0:
		return -1
	lines[len(lines)-1] = new_link_number
	resp = writeState(state_file, lines)
	if resp != 0:
		return -1
	return 0

def main():
	l = len(sys.argv)
	if l == 1:
		print "Not enough arguments. Enter command name."
		return 0
	cmd = sys.argv[1]
	if cmd == "init":
		#subprocess.call(["rm", "-r", "running/"])
		initParser("state.stf", 1)
	elif cmd == "parseAll":
		min_minutes = int(sys.argv[2])
		max_minutes = int(sys.argv[3])
		amount = int(sys.argv[4])
		parseAll(min_minutes, max_minutes, amount, "all_result", "state_file.stf", "running")
	else:
		print "Wrong command name. Nothing to execute."
	return 0
main()
# initParser()
# parseAll(80, 106, 10, "all_result", "state_file.stf", "running")




