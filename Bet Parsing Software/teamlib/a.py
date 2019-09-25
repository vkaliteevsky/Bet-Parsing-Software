#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import shutil
import os
import codecs
import sys
import teamlib as tlib

def main():
	print "a1 -> id = ", tlib.idForTeam("Arsenal")
	print "b   2 -> id = ", tlib.idForTeam("Alaab Damanhour")
	print "id -> teams = ", tlib.teamsForID(122)
	print "id -> team  = ", tlib.teamFromSiteForID(1, 2)
	print "team -> teams  = ", tlib.alternativeTeams("Alaab Damanhour")
	print "site codes -> team  = ", tlib.getTeamByIds(0, "Arsenal", 1)
	print "site codes -> team  = ", tlib.getTeamByNames("bet365", "Man Utd", "bet365")
	tlib.updateTeamByName("Alaab Damanhour", "LOL", "marathonbet")
	print "team -> teams  = ", tlib.alternativeTeams("Alaab Damanhour")
	tlib.updateTeamByName("LOL", "ASAS", "bet365")
	print "team -> teams  = ", tlib.alternativeTeams("Alaab Damanhour")
	print "team -> teams  = ", tlib.alternativeTeams("ASAS")
	tlib.updateTeamByName("LOL", "ASAS", 1)
	print "team -> teams  = ", tlib.alternativeTeams("LOL")

	

	return
main()

