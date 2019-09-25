#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import time
import datetime
from datetime import timedelta

GLOBAL_gmt = 0
Scores = 16
Totals = 21
Totals_eq = 11
Asians = 81
Asian_totals = 41
Margins = 11
Total_eq = [-1] * 11
Score_matrix = [-1] * Scores
for i in range(Scores):
	Score_matrix[i] = [-1] * Scores;
Total_over = [-1] * Totals
Total_under = [-1] * Totals
Asian_total_over = [-1] * Asian_totals
Asian_total_under = [-1] * Asian_totals
Asian_home = [-1] * Asians
Asian_away = [-1] * Asians
Margin_home = [-1] * Margins
Margin_away = [-1] * Margins
Total_under_home = [-1] * Totals
Total_under_away = [-1] * Totals
Total_over_home = [-1] * Totals
Total_over_away = [-1] * Totals
Total_eq_home = [-1] * Totals_eq
Total_eq_away = [-1] * Totals_eq
Home_to_score_yes = -1
Home_to_score_no = -1
Away_to_score_yes = -1
Away_to_score_no = -1
Both_to_score = [-1] * 2
Cmd1 = -1
Cmd2 = -1
Draw = -1
Cmd1_or_draw = -1
Draw_or_cmd2 = -1
Cmd1_or_cmd2 = -1
Goals_odd = -1
Goals_even = -1
Goals_home_odd = -1
Goals_home_even = -1
Goals_away_odd = -1
Goals_away_even = -1
Home_to_score = -1
Away_to_score = -1

def ODconvert(OD):
	slash = OD.find('/')
	top = float(OD[:slash])
	bot = float(OD[(slash+1):])
	return str(round((top / bot + 1), 3))

def pars(match_id, league_id):
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G0%23H0%23I1%23R1%23P%5E13%23Q%5E{1}%23%21%23AS%23B1%23~%23AC%23B1%23C1%23D13%23E{1}%23F2%23R1%23&wg=0&cid=158&cg=0').format(match_id, league_id))
	match = sock.read()
	sock.close()
	global Cmd1
	global Cmd2
	global Draw
	global Cmd1_or_draw
	global Draw_or_cmd2
	global Cmd1_or_cmd2
	global Goals_odd
	global Goals_even
	global Goals_home_odd
	global Goals_home_even
	global Goals_away_odd
	global Goals_away_even
	global Home_to_score_yes
	global Home_to_score_no
	global Away_to_score_yes
	global Away_to_score_no
##################################################################################################################################################################
# Parsing main tab for match
	key_pos = match.find('Start Time~;')
	if (key_pos > -1):
		return
	key_pos = match.find('Start Time~')	
	year = match[(key_pos + 11) : (key_pos + 15)]
	month = match[(key_pos + 15) : (key_pos +17)]
	day = match[(key_pos + 17) : (key_pos + 19)]
	hour = match[(key_pos + 19) : (key_pos + 21)]
	minute = match[(key_pos +21) : (key_pos + 23)]
	sec = match[(key_pos +23) : (key_pos + 25)]
	
	# 1,2 or X parsing start
	
	key_pos = match.find('Match Betting')
	if (key_pos > -1):
		ex_pos = match.find('EX=', key_pos + 13)
		end_pos = match.find(';', ex_pos + 3)
		teams = match[(ex_pos + 3) : end_pos]
		v_pos = teams.find(' v ')
		Cmd1_name = teams[:v_pos]
		Cmd2_name = teams[(v_pos + 3):]
	dt_str = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + sec + '\n'
	dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S\n") + timedelta(hours = GLOBAL_gmt)
	print dt
	print Cmd1_name
	print Cmd2_name
	key_pos = match.find('FULL TIME RESULT', v_pos)
	ODstart_pos = match.find('OD=', key_pos)
	ODfin_pos = match.find(';', ODstart_pos)
	Cmd1 = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
	ODstart_pos = match.find('OD=', ODfin_pos)
	ODfin_pos = match.find(';', ODstart_pos)
	Draw = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
	ODstart_pos = match.find('OD=', ODfin_pos)
	ODfin_pos = match.find(';', ODstart_pos)
	Cmd2 = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
	
	# 1, 2 or X parsing finish
	# Double chance parsing start
	
	key_pos = match.find('DOUBLE CHANCE')
	if (key_pos > -1):
		ODstart_pos = match.find('OD=', key_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		Cmd1_or_draw = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
		ODstart_pos = match.find('OD=', ODfin_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		Draw_or_cmd2 = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
		ODstart_pos = match.find('OD=', ODfin_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		Cmd1_or_cmd2 = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
	
	# Double chance parsing finish
	# Correct score parsing start
	
	key_pos = match.find('CORRECT SCORE')
	if (key_pos > -1):
		key_pos = match.find('NA=', key_pos + 13)
		key_pos = match.find('NA=', key_pos + 3)
		score_pos = match.find('NA=', key_pos + 3)
		ODfin_pos = key_pos
		win1_end = match.find('NA=Draw', key_pos)
		while (score_pos < win1_end):
			tire = match.find('-', score_pos)
			score_end = match.find(';', tire)
			score1 = int(match[(score_pos+3) : tire])
			score2 = int(match[(tire + 1) : score_end])
			ODstart_pos = match.find('OD=', ODfin_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			Score_matrix[score1][score2] = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
			score_pos = score_pos = match.find('NA=', score_pos + 3)
		score_pos = match.find('NA=', win1_end +3)
		draw_end = match.find('PY=c', win1_end)
		ODfin_pos = score_pos
		while (score_pos < draw_end):
			score1 = int(match[score_pos+3])
			ODstart_pos = match.find('OD=', ODfin_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			Score_matrix[score1][score1] = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
			score_pos = score_pos = match.find('NA=', score_pos + 3)
		key_pos = match.find('NA=', draw_end)
		score_pos = match.find('NA=', key_pos + 3)
		win2_end = match.find('NA=HALF TIME', key_pos)
		ODfin_pos = score_pos
		while (score_pos < win2_end):
			tire = match.find('-', score_pos)
			score_end = match.find(';', tire)
			score2 = int(match[(score_pos+3) : tire])
			score1 = int(match[(tire + 1) : score_end])
			ODstart_pos = match.find('OD=', ODfin_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			Score_matrix[score1][score2] = ODconvert(match[(ODstart_pos + 3) : ODfin_pos])
			score_pos = score_pos = match.find('NA=', score_pos + 3)
	
	# Correct score parsing finish
	
	# Partly parsing goals and asian handicap start
	
	key_pos = match.find('GOALS OVER')
	if (key_pos > -1):
		key_pos = match.find('OVER', key_pos + 10)
		ODstart_pos = match.find('OD=', key_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		OD = match[(ODstart_pos + 3) : (ODfin_pos)]
		ind_start = match.find('HA=', key_pos)
		ind_fin = match.find(';', ind_start)
		index = float(match[(ind_start + 3) : ind_fin])
		Total_over[int(2 * index)] = ODconvert(OD)
		key_pos = match.find('UNDER', key_pos)
		ODstart_pos = match.find('OD=', key_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		OD = match[(ODstart_pos + 3) : (ODfin_pos)]
		ind_start = match.find('HA=', key_pos)
		ind_fin = match.find(';', ind_start)
		index = float(match[(ind_start + 3) : ind_fin])
		Total_under[int(2 * index)] = ODconvert(OD)
	
	key_pos = match.find('ASIAN HANDICAP', key_pos)
	if(key_pos > -1):
		end_pos = match.find('NA=GOAL LINE', key_pos)
		cmd1_pos = match.find('NA=', key_pos)
		if (cmd1_pos < end_pos):
			ODstart_pos = match.find('OD=', cmd1_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			index = float(match[(ind_start + 3) : ind_fin])
			Asian_home[int((index + 10) * 4)] = ODconvert(OD)
			cmd2_pos = match.find('NA=', ODfin_pos)
			ODstart_pos = match.find('OD=', cmd2_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : (ODfin_pos)]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			index = float(match[(ind_start + 3) : ind_fin])
			Asian_away[int((index + 10) * 4)] = ODconvert(OD)
		
	# Partly parsing goals and asian handicap finish
###############################################################################################################################################
	
###############################################################################################################################################
# Parsing asian totals
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G50139%23H4%23I1%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('NA=OVER')
	if (key_pos > -1):
		end_pos = match.find('UNDER', key_pos + 7)
		ODstart_pos = match.find('OD=', key_pos + 7)
		while (ODstart_pos < end_pos):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			index = float(match[(ind_start + 3) : ind_fin])
			Asian_total_over[int(index * 4)] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
		while (ODstart_pos > -1):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			index = float(match[(ind_start + 3) : ind_fin])
			Asian_total_under[int(index * 4)] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
	for i in range(0, Asian_totals, 4):
		Total_over[i / 4] = Asian_total_over[i]
		Total_under[i / 4] = Asian_total_under[i]
		
###############################################################################################################################################
# Parsing asian alternative handicap
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G50138%23H4%23I1%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('ALTERNATIVE')
	cmd1_pos = match.find('NA=', key_pos)
	cmd2_pos = match.find('NA=', cmd1_pos + 3)
	if (key_pos > -1):
		ODstart_pos = match.find('OD=', cmd1_pos)
		while (ODstart_pos < cmd2_pos):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			index = float(match[(ind_start + 3) : ind_fin])
			Asian_home[int((index + 10) * 4)] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
		while (ODstart_pos > -1) :
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			index = float(match[(ind_start + 3) : ind_fin])
			Asian_away[int((index + 10) * 4)] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			
###############################################################################################################################################
# Parsing alternative goal line


###############################################################################################################################################	
# Parsing winning margins
	
	indeces = [0] * 10
	i = 0
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G56%23H4%23I1%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('MARGIN')
	if (key_pos > -1):
		key_pos = match.find('|PA', key_pos)
		end_pos = match.find('PY=b')
		na_pos = match.find('NA=', key_pos)
		while (na_pos < end_pos):
			indeces[i] = int(match[na_pos + 4])
			na_pos = match.find('NA=', na_pos + 3)
			i = i + 1
		cmd1_pos = match.find('NA=', end_pos)
		cmd2_pos = match.find('NA=', cmd1_pos + 3)
		end_pos = match.find('SCORE', cmd2_pos)
		i = 0
		ODstart_pos = match.find('OD=', cmd1_pos)
		while (ODstart_pos < cmd2_pos):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Margin_home[indeces[i]] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			i = i + 1
		i = 0
		while (ODstart_pos < end_pos):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Margin_away[indeces[i]] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			i = i + 1
			
###############################################################################################################################################
# Parsing total goals
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G10202%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('TOTAL GOALS')
	if (key_pos > -1):
		indeces = [0] * 11
		i = 0
		key_pos = match.find('NA=', key_pos)
		end_pos = match.find('PY=b', key_pos)
		na_pos = match.find('NA=', key_pos + 3)
		while (na_pos < end_pos):
			na_end = match.find(';', na_pos)
			indeces[i] = float(match[(na_pos + 3) : na_end])
			i = i + 1
			na_pos = match.find('NA=', na_end)
		i = 0
		key_pos = match.find('OVER', end_pos)
		under_pos = match.find('UNDER', key_pos)
		ODstart_pos = match.find('OD=', key_pos)
		while (ODstart_pos < under_pos):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_over[int(2 * indeces[i])] = ODconvert(OD)
			i = i + 1
			ODstart_pos = match.find('OD=', ODfin_pos)
		i = 0
		while (ODstart_pos > -1):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_under[int(2 * indeces[i])] = ODconvert(OD)
			i = i + 1
			ODstart_pos = match.find('OD=', ODfin_pos)
			
###############################################################################################################################################
# Parsing exact total goals
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G10203%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('EXACT')
	if (key_pos > -1):
		na_pos = match.find('NA=', key_pos)
		i = 0
		while (na_pos > -1):
			ODstart_pos = match.find('OD=', na_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_eq[i] = ODconvert(OD)
			i = i + 1
			na_pos = match.find('NA=', ODfin_pos)
	
###############################################################################################################################################
# Parsing team total goals
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G10127%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('TEAM TOTAL GOALS')
	if (key_pos > -1):
		na_pos = match.find('NA=', key_pos)
		end_pos = match.find('PY=c', na_pos)
		na_pos = match.find('NA=', na_pos + 3)
		ODstart_pos = match.find('OD=', na_pos)
		while (ODstart_pos < end_pos):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			ind = float(match[(ind_start + 3) : ind_fin])
			index = int(ind * 2)
			Total_over_home[index] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_under_home[index] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
		while (ODstart_pos > -1):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			ind_start = match.find('HA=', ODfin_pos)
			ind_fin = match.find(';', ind_start)
			ind = float(match[(ind_start + 3) : ind_fin])
			index = int(ind * 2)
			Total_over_away[index] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_under_away[index] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			
###############################################################################################################################################
# Parsing team exact goals and both teams to score and teams to score
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G0%23H0%23I6%23R1%23P%5E13%23Q%5E{1}%23&wg=0&cid=158&cg=0').format(match_id, league_id))
	match = sock.read()
	sock.close()
	key_pos = match.find('TOTAL GOALS/BOTH TEAMS TO SCORE')
	if (key_pos > -1):
		key_pos = match.find('BOTH TEAMS TO SCORE', key_pos + 20)
		if (key_pos > -1):
			ODstart_pos = match.find('OD=', key_pos + 10)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Both_to_score[1] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Both_to_score[0] = ODconvert(OD)
	
	key_pos = match.find('CLEAN SHEET')
	if (key_pos > -1):
		ODstart_pos = match.find('OD=', key_pos)
		ODfin_pos = match.find(';', ODstart_pos + 3)
		OD = match[(ODstart_pos + 3) : ODfin_pos]
		Away_to_score_no = ODconvert(OD)
		
		ODstart_pos = match.find('OD=', ODfin_pos)
		ODfin_pos = match.find(';', ODstart_pos + 3)
		OD = match[(ODstart_pos + 3) : ODfin_pos]
		Away_to_score_yes = ODconvert(OD)
		ODstart_pos = match.find('OD=', ODfin_pos)
		ODfin_pos = match.find(';', ODstart_pos + 3)
		OD = match[(ODstart_pos + 3) : ODfin_pos]
		Home_to_score_no = ODconvert(OD)
		ODstart_pos = match.find('OD=', ODfin_pos)
		ODfin_pos = match.find(';', ODstart_pos + 3)
		OD = match[(ODstart_pos + 3) : ODfin_pos]
		Home_to_score_yes = ODconvert(OD)
		
###############################################################################################################################################
# Parsing team exact goals
	
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G50415%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	i = 0
	key_pos = match.find('HOME TEAM EXACT GOALS')
	if (key_pos > -1):
		ODstart_pos = match.find('OD=', key_pos)
		while (ODstart_pos > -1):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_eq_home[i] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			i = i + 1
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G50416%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	i = 0
	key_pos = match.find('AWAY TEAM EXACT GOALS')
	if (key_pos > -1):
		ODstart_pos = match.find('OD=', key_pos)
		while (ODstart_pos > -1):
			ODfin_pos = match.find(';', ODstart_pos)
			OD = match[(ODstart_pos + 3) : ODfin_pos]
			Total_eq_away[i] = ODconvert(OD)
			ODstart_pos = match.find('OD=', ODfin_pos)
			i = i + 1
	

###############################################################################################################################################
# Parsing home/away odd even
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G50406%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	even_pos = match.find('Even')
	if (even_pos > -1):
		od_fin = match.find(';', even_pos + 8)
		OD = match[even_pos + 8 : od_fin]
		Goals_home_even = ODconvert(OD)
		odd_pos = match.find('Odd')
		od_fin = match.find(';', odd_pos + 7)
		OD = match[odd_pos + 7 : od_fin]
		Goals_home_odd = ODconvert(OD)
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G50407%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	even_pos = match.find('Even')
	if (even_pos > -1):
		od_fin = match.find(';', even_pos + 8)
		OD = match[even_pos + 8 : od_fin]
		Goals_away_even = ODconvert(OD)
		odd_pos = match.find('Odd')
		od_fin = match.find(';', odd_pos + 7)
		OD = match[odd_pos + 7 : od_fin]
		Goals_away_odd = ODconvert(OD)
		
###############################################################################################################################################
# Parsing goals odd/even
	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G10111%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
	match = sock.read()
	sock.close()
	odd_pos = match.find('Odd')
	if (odd_pos > -1):
		ODstart_pos = match.find('OD=', odd_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		OD = match[(ODstart_pos + 3) : ODfin_pos]
		Goals_odd = ODconvert(OD)
		even_pos = match.find('Even')
		ODstart_pos = match.find('OD=', even_pos)
		ODfin_pos = match.find(';', ODstart_pos)
		OD = match[(ODstart_pos + 3) : ODfin_pos]
		Goals_even = ODconvert(OD)

###############################################################################################################################################
# Parsing teams to score
#	sock = urllib.urlopen(('http://www.bet365scommetti.com/home/inplayapi/Sportsbook.asp?lid=1&zid=3&pd=%23AC%23B1%23C1%23D8%23E{0}%23F3%23G10211%23H4%23I6%23O2%23&wg=0&cid=158&cg=0').format(match_id))
#	match = sock.read()
#	sock.close()
#	key_pos = match.find('TEAMS TO SCORE')
#	if(key_pos > -1):
#		na_pos = match.find('NA=', key_pos + 14)
#		na_pos = match.find('NA=', na_pos + 3)
#		ODstart_pos = match.find('OD=', odd_pos)
#		ODfin_pos = match.find(';', ODstart_pos)
#		OD = match[(ODstart_pos + 3) : ODfin_pos]
#		Home_to_score = ODconvert(OD)
#		na_pos = match.find('NA=', ODfin_pos)
#		na_pos = match.find('NA=', na_pos + 3)
#		ODstart_pos = match.find('OD=', odd_pos)
#		ODfin_pos = match.find(';', ODstart_pos)
#		OD = match[(ODstart_pos + 3) : ODfin_pos]
#		Away_to_score = ODconvert(OD)
###############################################################################################################################################
	
	for i in range(Totals_eq):
		if (Total_eq[i] < 0):
			j = i - 1
	Total_over[(j - 1) * 2 + 1] = Total_eq[j]
	for i in range(Totals_eq):
		if (Total_eq_home[i] < 0):
			j = i - 1
	Total_over_home[(j - 1) * 2 + 1] = Total_eq_home[j]
	for i in range(Totals_eq):
		if (Total_eq_away[i] < 0):
			j = i - 1
	Total_over_away[(j - 1) * 2 + 1] = Total_eq_away[j]
	for i in range(Margins):
		if (Margin_home[i] < 0):
			j = i - 1
	Asian_home[(j + 10) * 4 - 2] = Margin_home[j]
	for i in range(Margins):
		if (Margin_away[i] < 0):
			j = i - 1
	Asian_away[(j + 10) * 4 - 2] = Margin_away[j]
	res = dt.strftime("%Y-%m-%d %H-%M-%S")
	res += '_' + Cmd1_name + '_' + Cmd2_name
	my_match = open(res,'w')
	my_match.write(Cmd1_name + '\n')
	my_match.write(Cmd2_name + '\n')
	my_match.write(str(dt.year) + ' ')
	my_match.write(str(dt.month) + ' ')
	my_match.write(str(dt.day) + '\n')
	my_match.write(str(dt.hour) + ' ')
	my_match.write(str(dt.minute) + '\n')
	my_match.write(str(Cmd1) + '\n')
	my_match.write(str(Cmd2) + '\n')
	my_match.write(str(Draw) + '\n')
	my_match.write(str(Cmd1_or_draw) + '\n')
	my_match.write(str(Draw_or_cmd2) + '\n')
	my_match.write(str(Cmd1_or_cmd2) + '\n')
	for i in range(Totals):
		my_match.write(str(Total_under[i]) + '\n')
	for i in range(Totals):
		my_match.write(str(Total_over[i]) + '\n')
	my_match.write(str(Goals_odd) + '\n')
	my_match.write(str(Goals_even) + '\n')
	my_match.write(str(Goals_home_odd) + '\n')
	my_match.write(str(Goals_home_even) + '\n')
	my_match.write(str(Goals_away_odd) + '\n')
	my_match.write(str(Goals_away_even) + '\n')
	for i in range(Totals):
		my_match.write(str(Total_under_home[i]) + '\n')
	for i in range(Totals):
		my_match.write(str(Total_over_home[i]) + '\n')
	for i in range(Totals):
		my_match.write(str(Total_under_away[i]) + '\n')
	for i in range(Totals):
		my_match.write(str(Total_over_away[i]) + '\n')
	for i in range(1, Asian_totals, 2):
		my_match.write(str(Asian_total_under[i]) + '\n')
	for i in range(1, Asian_totals, 2):
		my_match.write(str(Asian_total_over[i]) + '\n')
	for i in range(0, Asians, 2):
		my_match.write(str(Asian_home[i]) + '\n')
	for i in range(0, Asians, 2):
		my_match.write(str(Asian_away[i]) + '\n')
	for i in range(1, Asians, 2):
		my_match.write(str(Asian_home[i]) + '\n')
	for i in range(1, Asians, 2):
		my_match.write(str(Asian_away[i]) + '\n')
	for i in range(Totals_eq):
		my_match.write(str(Total_eq[i]) + '\n')
	for i in range(Totals_eq):
		my_match.write(str(Total_eq_home[i]) + '\n')
	for i in range(Totals_eq):
		my_match.write(str(Total_eq_away[i]) + '\n')
	my_match.write(str(Home_to_score_yes) + '\n')
	my_match.write(str(Home_to_score_no) + '\n')
	my_match.write(str(Both_to_score[1]) + '\n')
	my_match.write(str(Both_to_score[0]) + '\n')
	my_match.write(str(Away_to_score_yes) + '\n')
	my_match.write(str(Away_to_score_no) + '\n')
	for i in range(Margins):
		my_match.write(str(Margin_home[i]) + '\n')
	for i in range(Margins):
		my_match.write(str(Margin_away[i]) + '\n')
	for i in range(Scores):
		for j in range(Scores):
			my_match.write(str(Score_matrix[i][j]) + '\n')