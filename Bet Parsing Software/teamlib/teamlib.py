#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import shutil
import os
import codecs
import sys

#DICT = dict({'2': ('a3', 'b3', 'c3', '', '2'), '1': ('a2', 'b2', 'c2', '', '1'), 'c 4': ('', 'b   2', 'c 4', '', '3'), '3': ('', 'b   2', 'c 4', '', '3'), 'a1': ('a1', 'b1', 'c1', '', '0'), '0': ('a1', 'b1', 'c1', '', '0'), 'a3': ('a3', 'b3', 'c3', '', '2'), 'a2': ('a2', 'b2', 'c2', '', '1'), 'b1': ('a1', 'b1', 'c1', '', '0'), 'b2': ('a2', 'b2', 'c2', '', '1'), 'b3': ('a3', 'b3', 'c3', '', '2'), 'c3': ('a3', 'b3', 'c3', '', '2'), 'c2': ('a2', 'b2', 'c2', '', '1'), 'c1': ('a1', 'b1', 'c1', '', '0'), 'b   2': ('', 'b   2', 'c 4', '', '3')})
DICT = dict()

#------------------------
#-----public methods-----
#------------------------
# sites' codes
# 0 == bet365
# 1 == william hill
# 2 == marathonbet
# 3 == sbobet


def getDICT():
    return DICT

def idForTeam(team):
    if team in DICT :
        return DICT.get(team)[4]
    else :
        return "-1"

def teamsForID(ID):
    ID = str(ID)
    if ID in DICT :
        return DICT.get(ID)
    else :
        return None    

def alternativeTeams(team) :
    if team in DICT :
        return DICT.get(team)
    else :
        None    

def teamFromSiteForID(site, ID):
    t = teamsForID(ID)
    if t and site in range(4) :
        return t[site]
    else :
        return ""

def getTeamByIds(bookFrom, cmd, bookTo):
    t = alternativeTeams(cmd)
    site = getSiteCodeByCode(bookTo)
    if t :
        return t[site]     
    else :
        return ""

def getTeamByNames(bookFrom, cmd, bookTo):
    t = alternativeTeams(cmd)
    site = getSiteCodeByName(bookTo)
    if t :
        return t[site]
    else :
        return ""


#update по имени и по id сайта. старое имя и новое имя.
def updateTeamByName(cmdForSearch, newCmd, bookTo):
    site = getSiteCodeByName(bookTo)
    updateTeamBySite(cmdForSearch, newCmd, site)
def updateTeamByid(cmdForSearch, newCmd, bookTo):
    site = getSiteCodeByCode(bookTo)
    updateTeamBySite(cmdForSearch, newCmd, site)

def updateTeamBySite(cmdForSearch, newCmd, site):
    t = alternativeTeams(cmdForSearch)
    if t :
        oldLine = str(t[0]) + "#" + str(t[1]) + "#" + str(t[2]) + "#" + str(t[3]) + "\n"
        del DICT[cmdForSearch]
        lst = list(t)
        lst[site] = newCmd
        t = tuple(lst)
        for key in lst :
            if len(key) > 0 :
                DICT[key] = t

        newLine = str(t[0]) + "#" + str(t[1]) + "#" + str(t[2]) + "#" + str(t[3]) + "\n"
        #print oldLine
        #print newLine
        #need to update teams.in
        lines = open('teams.in','r').readlines()
        for i in range(len(lines)):
            if lines[i] == oldLine : 
                lines[i] = newLine

        f = open('teams.in', 'w')
        f.writelines(lines)
        f.close()
        return True
    else :
        return False

def updateTeamBySites(cmdForSearch, siteForSearch, newCmd, site):
    if len(str(siteForSearch)) > 1: 
        siteForSearch = getSiteCodeByName(siteForSearch)
    else:
        siteForSearch = getSiteCodeByCode(siteForSearch)
    if len(str(site)) > 1: 
        site = getSiteCodeByName(site)
    else:
        site = getSiteCodeByCode(site)

    if not updateTeamBySite(cmdForSearch, newCmd, site):
        if not updateTeamBySite(newCmd, cmdForSearch, siteForSearch):
            #need to add new team to DICT
            lines = open('teams.in','r').readlines()
            lst = ["","","",""]
            lst[siteForSearch] = cmdForSearch
            lst[site] = newCmd
            lst.append(str(len(lines))) #ID
            t = tuple(lst)
            for key in lst :
                if len(key) > 0 :
                    DICT[key] = t

            newLine = str(t[0]) + "#" + str(t[1]) + "#" + str(t[2]) + "#" + str(t[3]) + "\n"
            #print oldLine
            #print newLine
            #need to update teams.in
            lines.append(newLine)
            f = open('teams.in', 'w')
            f.writelines(lines)
            f.close()
            return True
        else :
            updateTeamBySite(cmdForSearch, newCmd, site)
    else :
        updateTeamBySite(newCmd, cmdForSearch, siteForSearch)
    return False
        
#-------------------------
#-----private methods-----
#-------------------------
def getSiteCodeByCode(dispCode):
    codes = [0, 3, 2, 1]
    return codes[dispCode]
def getSiteCodeByName(name):
    if name == "bet365" :
        return getSiteCodeByCode(0)
    if name == "sbobet" :
        return getSiteCodeByCode(1)
    if name == "marathonbet" :
        return getSiteCodeByCode(2)
    
    # "whill"
    return getSiteCodeByCode(3)


def getData():
    f = open('teams.in','r')
    ID = 0
    for line in f:
        t = line[:-1].split("#")
        t.append(str(ID))
        ID += 1
        #value = '("' + t[0] + '",' + '"' + t[1] + '",' + '"' + t[2] + '",' + '"' + t[3] + '")'
        value = tuple(t)
        for key in t :
            if len(key) > 0 :
                DICT[key] = value
    f.close()
    return DICT
    

def main():
    getData()
    #print DICT
    return

main()
