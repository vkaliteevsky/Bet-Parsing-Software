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
	now_old = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S\n")
	for i in range(amount_of_pages):
		subprocess.call(["./init.py", "http://sports.williamhill.com/bet/en-gb/betting/y/5/tm/" + str(i) + "/Football.html", "running", "phantomjs", "log_file.txt"])
	now_new = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S\n")
	writeState(state_file, [str(now_old), str(now_new), 0])
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
	processes = []				# массив процессов (node js)
	pipe_text = ""				# список всех матчей, которые передаются по pipe
	
	while last_index > 0:
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
		if min_minutes <= delta_mins and delta_mins <= max_minutes and dt_str != "\n":		# фильтрация по времени
			processes.append(subprocess.Popen(["node", "parse_page.js", link, folder_name + str(counter), cmd1, cmd2]))
			pipe_text += dt_str + cmd1 + cmd2
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
	for i in range(len(processes)):
		processes[i].wait()
	print pipe_text
# фильтрует матчи по дате, названиям команд и извлекает информацию
# input:
#	to_find_dt_str - 
#	folder_name - имя папки, в которой будут храниться файлы с результатами работы программы
#	state_file - имя файла, в котором сохраняется последнее состояние работы парсера
#	input_folder - имя папки, в которой хранятся файлы с результатами работы метода initParser
def parseMatch(to_find_dt_str, to_find_cmd1, to_find_cmd2, folder_name, state_file, input_folder):
	if input_folder[len(input_folder)-1] != "/":
		input_folder = input_folder + "/"
	if folder_name[len(folder_name)-1] != "/":
		folder_name = folder_name + "/"
	if to_find_dt_str[len(to_find_dt_str)-1] != "\n":
		to_find_dt_str += "\n"
	if to_find_cmd1[len(to_find_cmd1)-1] != "\n":
		to_find_cmd1 += "\n"
	if to_find_cmd2[len(to_find_cmd2)-1] != "\n":
		to_find_cmd2 += "\n"
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	links_file = open(input_folder + "links.out")
	dates_file = open(input_folder + "dates.out")
	cmds_file = open(input_folder + "cmds.out")
	
	match_was_found = False
	dt_str = dates_file.readline()
	link = links_file.readline()
	cmd1 = cmds_file.readline()
	cmd2 = cmds_file.readline()
	while link:
		if to_find_dt_str == dt_str and to_find_cmd1 == cmd1 and to_find_cmd2 == cmd2:
			match_was_found = True
			break;
		dt_str = dates_file.readline()
		link = links_file.readline()
		cmd1 = cmds_file.readline()
		cmd2 = cmds_file.readline()
	if match_was_found:
		id = "found_match"
		subprocess.Popen(["node", "parse_page.js", link, folder_name + id, cmd1, cmd2])
	links_file.close()
	dates_file.close()
	cmds_file.close()
	return match_was_found
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
		text = text + str(lines[i])
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
	lines[len(lines)-1] = int(lines[len(lines)-1])
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

# определяет находится ли парсер в конечном состоянии (т.е. просмотрены ли все доступные матчи)
# input:
#	state_file - имя файла-состояния
#	input_folder - имя папки, в которой хранятся файлы с результатами работы метода initParser
def isEnd(state_file, input_folder):
	if input_folder[len(input_folder)-1] != "/":
		input_folder = input_folder + "/"
	lines = readState(state_file)
	f = open(input_folder + "links.out")
	line = f.readline()
	counter = 1
	while line:
		line = f.readline()
		if line != "\n":
			counter += 1
	f.close()
	#print "Lines:", counter
	return counter -1 == lines[len(lines)-1]
	
def main():
	l = len(sys.argv)
	if l == 1:
		print "Not enough arguments. Enter command name."
		return 1
	cmd = sys.argv[1]
	if cmd == "init":
		if os.path.exists("running"):
			subprocess.call(["rm", "-r", "running/"])
		initParser("state.stf", 2)
	elif cmd == "parseAll":
		if os.path.exists("all_result"):
			subprocess.call(["rm", "-r", "all_result"])
		min_minutes = int(sys.argv[2])
		max_minutes = int(sys.argv[3])
		amount = int(sys.argv[4])
		parseAll(min_minutes, max_minutes, amount, "all_result", "state.stf", "running")
	elif cmd == "reset":
		modifyState("state.stf", 0)
	elif cmd == "isEnd":
		print isEnd("state.stf", "running/")
		return isEnd("state.stf", "running/")
	elif cmd == "getState":
		x = readState("state.stf")
		text = ""
		for i in range(len(x)):
			text += str(x[i])
		print text
		return 0
	elif cmd == "parseMatch":
		#if os.path.exists("all_result"):
			#subprocess.call(["rm", "-r", "all_result"])
		
		dt_str = sys.argv[2]
		cmd1 = sys.argv[3]
		cmd2 = sys.argv[4]
		parseMatch(dt_str, cmd1, cmd2, "all_result1", "state.stf", "running")
	elif cmd == "test":
		print test
	else:
		print "Wrong command name. Nothing to execute."
		return 1
	return 0

main()




