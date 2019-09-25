#!/usr/bin/env python
# -*- coding: utf-8 -*-

import init
import datetime
import pars_match
from datetime import timedelta
import urllib
import os
import linecache
import re
import sys
import errno
import subprocess

def pars_match_main(dt, cmd1, cmd2):
	os.chdir('all_results')
	start_time = open('start_time','r')
	i = 0
	dt = dt.strip()
	check = 0
	for line in start_time:
		if (line.strip() == dt):
			i1 = 2*i + 1
			i2 = 2*i + 2
			team1 = linecache.getline('teams', i1).strip()
			team2 = linecache.getline('teams', i2).strip()
			if ( ((cmd1 == team1) and (cmd2 == team2)) or ((cmd1 == team2) and (cmd2 == team1)) ):
				ids = linecache.getline('all_matches', i + 1)
				league_id = int(ids.split()[0])
				match_id = int(ids.split()[1])
				pars_match.pars(str(match_id), str(league_id))
				check = 1
		i += 1
	if (check == 1):
		print True
	else:
		print False
	return

def main():
	if not os.path.exists("all_results"):
		os.makedirs("all_results")
	input = sys.argv[1]
	if (input == 'init'):
		init.init()
	elif (input == 'isEnd'):
		os.chdir('all_results')
		state = open('state', 'r')
		state.readline()
		all = state.readline()
		current = state.readline()
		if (all == current ):
			print True
			return True
		else:
			print False
			return False
		
	elif (input == 'parseAll'):
		min_minutes = sys.argv[2]
		max_minutes = sys.argv[3]
		amount = sys.argv[4]
		os.chdir('all_results')
		times = open('start_time', 'r')
		state = open('state','r')
		now_str = state.readline()
		all = state.readline()
		Counter = state.readline()
		Counter = int(Counter)
		parsed = 0
		while((parsed < int(amount)) and (Counter < (int(all)))):
			#print Counter
			dt_str = times.readline()
			dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S\n")
			now = datetime.datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S\n")
			delta_mins = int((dt - now).total_seconds())
			if ((delta_mins <= (int(max_minutes)*60)) and (delta_mins >= (int(min_minutes)*60))):
				ids = linecache.getline('all_matches', Counter + 1)
				league_id = int(ids.split()[0])
				match_id = int(ids.split()[1])
				pars_match.pars(str(match_id), str(league_id))
				parsed += 1
			Counter += 1
		state = open('state','w')
		state.write(now_str)
		state.write(all)
		state.write(str(Counter))
		return
	elif (input == 'getState'):
		os.chdir('all_results')
		try:
			state = open('state', 'r')
		except IOError:
			state = open('state','w')
			state.write('1970-01-01 00:00:00\n0\n0')
			state = open('state', 'r')
		arg = []
		tmp_text = ""
		for i in range(3):
			arg.append(state.readline())
		for i in range(3):
			tmp_text += arg[i].strip() + "\n"
		print tmp_text.strip()
		return arg[0:2];	
	elif (input == 'reset'):
		os.chdir('all_results')
		state = open('state', 'r')
		timer = state.readline()
		counter = state.readline()
		state = open('state', 'w')
		state.write(timer + counter + '0')
		return
	elif (input == 'parseMatch'):
		dt = sys.argv[2]
		cmd1 = sys.argv[3]
		cmd2 = sys.argv[4]
		pars_match_main(dt, cmd1, cmd2)
		return
	elif (input == 'parseMatches'):
		path = sys.argv[2]
		myfile = open(path, 'r')
		myline = myfile.readlines()
		for i in range(0, len(myline), 3):
			dt = myline[i]
			cmd1 = myline[i+1]
			cmd2 = myline[i+2]
			pars_match_main(dt, cmd1, cmd2)
		return
	elif (input == 'deleteState'):
		if os.path.exists("all_results/state"):
			subprocess.call(["rm", "all_results/state"])
main()			