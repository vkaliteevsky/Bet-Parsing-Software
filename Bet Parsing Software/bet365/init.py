#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os
import errno
import datetime
import shutil
from datetime import timedelta
GLOBAL_gmt = 0
Counter = 0

def get_matches(league_id):
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D13%23E{0}%23F2%23R1%23&wg=0&cid=158&cg=0').format(league_id))
	league = sock.read()
	sock.close()
	global Counter
	key_pos = league.find('FULL TIME RESULT')
	if (key_pos > -1):
		output = open('all_matches', 'a')
		start_time = open('start_time', 'a')
		teams = open('teams', 'a')
		end_pos = league.find('PY=b', key_pos)
		na_pos = league.find('NA=', key_pos)
		match_pos = league.find('NA=', na_pos + 3)
		while (match_pos < end_pos):
			id_start = league.find('FI=', match_pos)
			output.write(str(league_id) + ' ')
			match_id = league[(id_start + 3) : (id_start + 11)]
			output.write(match_id + '\n')
			sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G0%23H0%23I1%23R1%23P%5E13%23Q%5E{1}%23%21%23AS%23B1%23~%23AC%23B1%23C1%23D13%23E{1}%23F2%23R1%23&wg=0&cid=158&cg=0').format(match_id, league_id))
			match = sock.read()
			sock.close()
			time_pos = match.find('Start Time')
			year = match[time_pos + 11 : time_pos + 15]
			month = match[time_pos + 15 : time_pos + 17]
			day = match[time_pos + 17 : time_pos + 19]
			hour = match[time_pos + 19 : time_pos + 21]
			minute = match[time_pos + 21 : time_pos + 23]
			sec = match[time_pos + 23 : time_pos + 25]
			dt_str = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + sec + '\n'
			dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S\n") + timedelta(hours = GLOBAL_gmt)
			start_time.write(str(dt) + '\n')
			key_pos = match.find('Match Betting')
			key_pos = match.find('EX=', key_pos)
			end1_pos = match.find(';', key_pos + 3)
			name = match[key_pos + 3 : end1_pos]
			v = name.find(' v ')
			team1 = name[: v]
			team2 = name[(v + 3) :]
			teams.write(team1 + '\n' + team2 + '\n')
			Counter += 1
			match_pos = league.find('NA=', id_start + 3)
	return
			
def init():
	sock = urllib.urlopen('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AS%23B1%23&wg=0&cid=158&cg=0')
	soccer = sock.read()
	sock.close()
	key_pos = soccer.find('United Kingdom')
	na_pos = soccer.find('NA=', key_pos)
	na_next = soccer.find('NA=', na_pos + 3)
	end_pos = soccer.find('Goals Over/Under', na_next)
	shutil.rmtree('all_results')
	os.makedirs('all_results')
	os.chdir('all_results')
	output = open('all_matches','w')
	start_time = open('start_time','w')
	teams = open('teams','w')
	while (na_next < end_pos):
		id_pos = soccer.find('#E', na_pos, na_next)
		if (id_pos > -1):
			league_id = soccer[(id_pos + 2) :(id_pos + 10)]
			get_matches(league_id)
		na_pos = na_next
		na_next = soccer.find('NA=', na_next + 3)
	dt_str = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	state = open('state', 'w')
	state.write(dt_str + '\n' + str(Counter) + '\n' + '0')