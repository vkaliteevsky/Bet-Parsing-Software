#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen
import subprocess
import datetime
import time
from datetime import timedelta
import os
import sys

# реализует вызов парсера с учетом их расположения в папках
# input:
#	parser_name - имя папки/парсера ("whill", "marathonbet", ...)
#	params - параметры командной строки ["./main.py", "init"]
def callParser(parser_name, params):
	subprocess.call(params)
	return 0

def hasElement(name, arr):
	for i in range(len(arr)):
		if name == arr[i]:
			return True
	return False
def readFile(path):
	lines = []
	if not os.path.exists(path):
		print "file doesn't exists:", path
		return []
	f = open(path, "r")
	text = f.readlines()
	for i in range(len(text)):
		text[i] = text[i].strip()
	f.close()
	return text

def main():
	print "Runnig parser William Hill"
	callParser("whill", ["./main.py", "init"])
	print "Parser finished"
	if not os.path.exists("result.out"):
		subprocess.call(["touch", "result.out"])
	cmds = readFile("result.out")
	new_cmds = readFile("running/cmds.out")
	
	for i in range(len(new_cmds)):
		if not hasElement(new_cmds[i], cmds):
			cmds.append(new_cmds[i])
	
	text = ""
	f = open("result.out", "w")
	for i in range(len(cmds)):
		text += cmds[i] + "\n"
	f.write(text[0:-1])
	f.close()
	
main()