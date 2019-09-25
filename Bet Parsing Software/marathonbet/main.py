#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import shutil
import os
import codecs
import sys
from splinter import Browser

CONST_MIN_EVENT_ADDITION_ACTIONS_AMOUNT = 20


#-------------------------
#--------helpers----------
#-------------------------
def throwError(level, text):
    #print "-----------"
    print "ERROR"
    print text
    #print "-----------"

def getSubstr(str, toFind, endSymbol):
    res = ''
    ind = str.find(toFind)
    if ind == -1 :
        res = 'no'
    else :
        ind += len(toFind)
        #if (ind >= len(str)):
        #        print "index out of range"
        #        print str
        #        raw_input('waiting')
        while str[ind] != endSymbol :
            res += str[ind]
            ind += 1
            #if (ind >= len(str)):
            #    print "index out of range"
            #    print str
            #    raw_input('waiting')
    
    #delete space symbols
    #res.encode('utf8')
    return res.strip()
def checkDate(strDate, minMinutes, maxMinutes):
    diffTime = -1
    date = time.strptime(strDate, "%Y-%m-%d %H:%M:00\n")
    currTime = time.gmtime()
    diffTime = ((date.tm_mday - currTime.tm_mday) * 24 + date.tm_hour - currTime.tm_hour ) * 60 + date.tm_min - currTime.tm_min
    return (diffTime >= minMinutes and diffTime <= maxMinutes)
def getInfo(str):
    res = ''
    prevChar = '#'
    isHTML = 0
    for char in str :
        if (char == '<'): 
            isHTML += 1
        if (char == '>'): 
            isHTML -= 1
            continue
        if (isHTML == 0): 
            if not ((char == ' ' or char == '\n') and (prevChar == ' ' or prevChar == '\n')):
                res += char
                prevChar = char
    return res     
def getBet(str, toFind):
    res = 0
    ind = str.find(toFind)
    if ind == -1 :
        res = -1
    else :
        num = ''
        den = ''
        flag = False;
        ind += len(toFind)
        while str[ind].isdigit() :
            num += str[ind]
            ind += 1
        ind += 1
        while str[ind].isdigit() :
             den += str[ind]
             ind += 1
        if num == '' or den == '' :
            res = -1
        else :
            res = float(num) / float(den) + 1
    return res
def getFloatBet(str) :
    numbers = str.split('/')
    if len(numbers) != 2 : 
        return -1
    res = float(numbers[0]) / float(numbers[1]) + 1
    return res
def getAsianTotal(str) :
    return float(str.split(",")[0])
def getAsianHandicap(str) :
    return min(map(float, str.split(',')))
def isEqualAsianHandicap(fst, snd) :
    fstNum = fst.split(',')
    sndNum = snd.split(',')
    return fst[0][1:] == snd[0][1:] and fst[1][1:] == snd[1][1:]

def getFileNameForEvent(event):
    res = ''
    date = time.strptime(event[1].strip(), "%Y-%m-%d %H:%M:00")
    res += time.strftime("%Y-%m-%d %H-%M-00_", date)
    res += event[2].strip() + '_' + event[3].strip()
    return res

#-------------------------
#-------formatting--------
#-------------------------

def testFormat():
    parseMatch('2015-02-22 11:00:00\n', 'St Pauli U-19\n', 'Werder Bremen U-19\n')
    return

def formatDataForEvent(event, text):
    event = tuple(item.strip() for item in event)
    res = event[2] + '\n' + event[3] + '\n'
    date = time.strptime(event[1].strip(), "%Y-%m-%d %H:%M:00")
    res += time.strftime("%Y %m %d\n%H %M\n", date)
#    a = res.count('\n')
    res += getMoneyLine(event[2], event[3], text)
#    b = res.count('\n')
#    print 'new \\n count = ', b - a
    res += getTotalsUnderOverOddEven(text)
    res += getTotalsHomeAwayOddEven(text)
    res += getTotalsTeamUnderOver(text, event[2]) #home
    res += getTotalsTeamUnderOver(text, event[3]) #away
    res += getAsianTotalsUnderOver(text)
    res += getHandicapHomeAway(text, event[2], event[3])
    res += getAsianHandicapHomeAway(text, event[2], event[3])
    res += getTotalEqual(text)
    res += getTotalEqualHomeAway(text)
    res += getHomeBothAwayToScore(text, event[2], event[3])
    res += getWinningMarginsHomeAway(text, event[2], event[3])
    res += getCorrectScore(text, event[2], event[3])
    return res
def getMoneyLine(home, away, text):
    res = ''
    strToFind = home + " To Win "
    res += str(getBet(text, strToFind)) + "\n"
    strToFind = away + " To Win "
    res += str(getBet(text, strToFind)) + "\n"
    strToFind = "Draw "
    res += str(getBet(text, strToFind)) + "\n"
    strToFind = home + " To Win or Draw "
    res += str(getBet(text, strToFind)) + "\n"
    strToFind = away + " To Win or Draw "
    res += str(getBet(text, strToFind)) + "\n"
    strToFind = home + " To Win or " + away + " To Win "
    res += str(getBet(text, strToFind)) + "\n"
    return res
def getTotalsUnderOverOddEven(text):
    res = ''
    totalsUnder = [-1] * 21
    totalsOver = [-1] * 21
    #start index
    strToFind = "Total Goals Under Over "
    ind = text.find(strToFind)
    #print '==============='
    #print text
    #print 'ind = ', ind
    #print '==============='

    if ind == -1:
        #NO Totals
        for i in range(44) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    while not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    info = map(lambda item: item[1:-1] if item[0] == "(" else item, info)
    #print "info = ", info
    #parsing info
    i = 0
    while i < len(info) :
        if i + 2 < len(info) and info[i] == info [i + 2] :
            totalsUnder[int(2 * float(info[i]))] = getFloatBet(info[i + 1])
            totalsOver[int(2 * float(info[i + 2]))] = getFloatBet(info[i + 3])
            i += 4
        else :
            i += 2
        
    #print "totalsUnder =", totalsUnder
    #print "totalsOver =", totalsOver

    for total in totalsUnder :
        res += str(total) + '\n'
    for total in totalsOver :
        res += str(total) + '\n'

    #odd and even totals
    strToFind = "Odd Even "
    ind = text.find(strToFind, ind) + len(strToFind)
    start = ind
    while not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    #print "odd even info = ", info
    res += str(getFloatBet(info[0])) + '\n'
    res += str(getFloatBet(info[1])) + '\n'
    return res
def getTotalsHomeAwayOddEven(text):
    res = ''
    for i in range(4) :
        res += '-1\n'
    return res
def getTotalsTeamUnderOver(text, team):
    res = ''
    totalsUnder = [-1] * 21
    totalsOver = [-1] * 21
    #start index
    strToFind = "Total Goals (" + team + ") Under Over "
    ind = text.find(strToFind)
    if ind == -1:
        #NO Totals
        for i in range(42) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    while ind < len(text) and not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    info = map(lambda item: item[1:-1] if item[0] == "(" else item, info)
    #print "info = ", info
    #parsing info
    i = 0
    isTotalsUnder = True
    while i < len(info) :
        if isTotalsUnder :
            totalsUnder[int(2 * float(info[i]))] = getFloatBet(info[i + 1])
        else :    
            totalsOver[int(2 * float(info[i]))] = getFloatBet(info[i + 1])
        i += 2
        isTotalsUnder = not isTotalsUnder
    #print "totalsUnder =", totalsUnder
    #print "totalsOver =", totalsOver

    for total in totalsUnder :
        res += str(total) + '\n'
    for total in totalsOver :
        res += str(total) + '\n'
    #print res
    return res
def getAsianTotalsUnderOver(text):
    res = ''
    totalsUnder = [-1] * 20
    totalsOver = [-1] * 20
    #start index
    strToFind = "Asian Total Goals Under Over"
    ind = text.find(strToFind)
    if ind == -1:
        #NO Totals
        for i in range(40) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    while not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    info = map(lambda item: item[1:-1] if item[0] == "(" else item, info)
    #print "info = ", info
    #parsing info
    i = 0
    while i < len(info) :
        if i + 2 < len(info) and info[i] == info [i + 2] :
            totalsUnder[int(2 * getAsianTotal(info[i]))] = getFloatBet(info[i + 1])
            totalsOver[int(2 * getAsianTotal(info[i + 2]))] = getFloatBet(info[i + 3])
            i += 4
        else :
            i += 2
        
    #print "totalsUnder =", totalsUnder
    #print "totalsOver =", totalsOver

    for total in totalsUnder :
        res += str(total) + '\n'
    for total in totalsOver :
        res += str(total) + '\n'

    return res
def getHandicapHomeAway(text, home, away):
    res = ''
    handicapHome = [-1] * 41
    handicapAway = [-1] * 41
    #start index
    strToFind = "To Win Match With Handicap " + home + " " + away + " "
    ind = text.find(strToFind)
    if ind == -1:
        #NO Totals
        for i in range(82) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    while not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    info = map(lambda item: item[1:-1] if item[0] == "(" else item, info)
    #print "info = ", info
    
    #parsing info
    i = 0
    while i < len(info) :
        if i + 2 < len(info) and info[i][1:] == info [i + 2][1:] :
            handicapHome[int(2 * float(info[i])) + 20] = getFloatBet(info[i + 1])
            handicapAway[int(2 * float(info[i + 2])) + 20] = getFloatBet(info[i + 3])
            i += 4
        else :
            i += 2
        
    #print "handicapHome =", handicapHome
    #print "handicapAway =", handicapAway
    
    for total in handicapHome :
        res += str(total) + '\n'
    for total in handicapAway :
        res += str(total) + '\n'

    return res
def getAsianHandicapHomeAway(text, home, away):    
    res = ''
    handicapHome = [-1] * 40
    handicapAway = [-1] * 40
    #start index
    strToFind = "To Win Match With Asian Handicap " + home + " " + away + " "
    ind = text.find(strToFind)
    if ind == -1:
        #NO Totals
        for i in range(80) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    while not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    info = map(lambda item: item[1:-1] if item[0] == "(" else item, info)
    #print "info = ", info
    
    #parsing info
    i = 0
    while i < len(info) :
        if i + 2 < len(info) and isEqualAsianHandicap(info[i], info [i + 2]) :
            handicapHome[int(2 * getAsianHandicap(info[i])) + 20] = getFloatBet(info[i + 1])
            handicapAway[int(2 * getAsianHandicap(info[i + 2])) + 20] = getFloatBet(info[i + 3])
            i += 4
        else :
            i += 2
        
    #print "handicapHome =", handicapHome
    #print "handicapAway =", handicapAway
    
    for total in handicapHome :
        res += str(total) + '\n'
    for total in handicapAway :
        res += str(total) + '\n'

    return res
def getTotalEqual(text):
    res = ''
    totalEqual = [-1] * 11
    #start index
    strToFind = "Number of Goals "
    ind = text.find(strToFind)
    if ind == -1:
        #NO Totals
        for i in range(11) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    ind = text.find("more)")
    info = text[start:ind].split()
    #zero case 
    if info[0] == "(No" and info[1] == "goals)" :
        totalEqual[0] = getFloatBet(info[2])
    else :
        #NO Totals
        for i in range(11) :
            res += '-1\n'
        return res

    for i in range(3, len(info), 2) :
        if info[i][-1] == ')' :
            totalEqual[int(info[i][1:-1])] = getFloatBet(info[i + 1])
            
    for item in totalEqual :
        res += str(item) + '\n'

    return res
def getTotalEqualHomeAway(text) :
    res = ''
    for i in range(22) :
        res += '-1\n'
    return res
def getHomeBothAwayToScore(text, home, away):
    res = ''
    strsToFind = [home + " To Score ", "Both Teams To Score ", away + " To Score "]
    for strToFind in strsToFind :
        ind = text.find(strToFind)
        if ind == -1:
            #NO info
            for i in range(2) :
                res += '-1\n'
            continue
        ind += len(strToFind)
        start = ind
        while not text[ind].isalpha() :
            ind += 1
        info = text[start:ind].split()
        if info[0] == "-" : info = []
        info = map(getFloatBet, info)
        if len(info) == 0 :
            #NO info
            for i in range(2) :
                res += '-1\n'
            continue
        if len(info) == 1 :
            res += str(info[0]) + "\n-1\n"
        if len(info) >= 2 :
            res += str(info[0]) + '\n'
            res += str(info[1]) + '\n'
    #print res
    return res
def getWinningMarginsHomeAway(text,home, away) :
    res = ''
    strToFind = "Winning Margin"
    ind = text.find(strToFind)
    if ind == -1 :
        #no margins
        for i in range(22) :
            res += '-1\n'
        return res
    teams = [home, away]
    for team in teams :
        margins = [-1] * 11
        for i in range(1, 10) :
            if i == 1 :
                strToFind = "To Win By 1 Goal - " + team + " "
            else :
                strToFind = "To Win By " + str(i + 1) + " Goals - " + team + " "
            bet = getBet(text, strToFind)
            if bet == -1 :
                break
            margins[i] = bet
        #print margins
        for item in margins :
            res += str(item) + '\n'
    
    return res
def getCorrectScore(text, home, away) :
    res = ''
    strToFind = "Correct Score " + home + " Draw " + away + " "
    ind = text.find(strToFind)
    if ind == -1 :
        #no margins
        for i in range(22) :
            res += '-1\n'
        return res
    ind += len(strToFind)
    start = ind
    while not text[ind].isalpha() :
        ind += 1
    info = text[start:ind].split()
    info = filter(lambda x : x != "-", info)
    info = map(lambda item: item[1:] if item[0] == "(" else item[:-1] if item[-1] == ")" else item, info)
    #print info

    table = [[-1]*16 for i in range(16)]
    i = 0
    while i < len(info) :
        table[int(info[i])] [int(info[i + 1])] = getFloatBet(info[i + 2])
        i += 3
    #print table
    for i in range(16) :
        for j in range(16) :
            res += str(table[i][j]) + "\n"
        #res += "\n"
    
    #any other score
    #strToFind = "Any Other Score - "
    #res += str(getBet(text, strToFind)) + "\n"
    return res
#-------------------------
#--------parsing----------
#-------------------------
def getEvents(str, hoursLimit):

    
    eventsId = []
    toFind = 'first member-area '
    ind = str.find(toFind)
    while (ind > 0):
        
        strForSearch = str[ind : ind + 900]

        #get id
        strId = getSubstr(strForSearch, 'event-more-view-', '\'')
        #get date
        strDate = getSubstr(strForSearch, '\"date\">', '<')
        #get amount
        strAmount = getSubstr(strForSearch, '<span>+', '<')
        #get home command
        strHome = getSubstr(strForSearch, '1.</b>\n <div class="member-name nowrap" data-ellipsis="{}">', '<')
        #get away command
        strAway = getSubstr(strForSearch, '2.</b>\n <div class="member-name nowrap" data-ellipsis="{}">', '<')
        if strHome == 'no':
            strHome = getSubstr(strForSearch, '1.</b>\n <div class="today-member-name nowrap" data-ellipsis="{}">', '<')
            strAway = getSubstr(strForSearch, '2.</b>\n <div class="today-member-name nowrap" data-ellipsis="{}">', '<')

        #print strForSearch
        #print strId 
        #print strDate
        #print strHome
        #print strAway
    
        if (len(strDate) == 5) :
            date = time.strptime(strDate, "%H:%M")
            currTime = time.gmtime()
            strDate = time.strftime("%Y-%m-%d ", currTime) + strDate + ":00"
        else :
            date = time.strptime(strDate, "%d %b %H:%M")
            #maybe problem with year
            strDate = time.strftime("2015-%m-%d %H:%M:00", date)

    

        if strAmount != 'no' and int (strAmount) > CONST_MIN_EVENT_ADDITION_ACTIONS_AMOUNT :
            eventsId.append((strId, strDate, strHome, strAway))
        
        ind = str.find(toFind, ind + 900)
        


    return eventsId

def getEventsFromFile():
    events = []
    f = codecs.open('events.out', 'rw', encoding='utf-8')
    n = int(f.readline())
    i = 0
    while i < n :
        strId = f.readline()
        strDate = f.readline()
        strHome = f.readline()
        strAway = f.readline()
        events.append((strId, strDate, strHome, strAway))
        i += 1
    return events

def getMatchesFromFile(filename):
    events = []
    f = codecs.open(filename, 'rw', encoding='utf-8')
    lines = f.readlines()
    for i in range(0, len(lines), 3) :
        events.append((lines[i], lines[i + 1], lines[i + 2]))
    return events

def getDataForEvents(eventsId, amount, currState, isParseAll):
    resForParseMatches = []
    t = time.time()
    browser = Browser('chrome') #chrome phantomjs
    #print "init browser", (time.time() - t)
    try :
        browser.visit('http://www.betmarathon.com/en/popular/Football/')
    except Exception as error :
        throwError(1, "Browser.visit failed. info = " + str(error))
    #print "visit maraphon" , (time.time() - t)

    n = min(8, amount)
    fromInd = currState - n
    toInd = currState
    finishInd = min(len(eventsId), currState + amount)
    while True :
        
        fromInd = min(finishInd - 1, fromInd + n)
        toInd = min(finishInd, toInd + n)
        #print "---------------"
        #print "attempt fromInd  = ", fromInd, "; toInd = ", toInd
        for index in range(fromInd, toInd) :
            eventId = eventsId[index]
            #print eventId
            #print "time before script" , (time.time() - t)
            strId = eventId[0][:-1]
            #f.write(eventId[0] + '\n' + eventId[1] + '\n')
            try : 
                script = "Markets.applyView(document.getElementById('event-more-view-" + strId + "'));return false;"
                browser.execute_script(script);
            except Exception as error :
                throwError(1, "Browser.execute_script failed. info = " + str(error))
            #print "time after script" , (time.time() - t)
    
        #print "scripts are done" , (time.time() - t)
        #print "sleep"
        time.sleep(5)
        #print "wake up"
        
        for index in range(fromInd, toInd) :
            res = ''
            eventId = eventsId[index]
            strId = eventId[0][:-1]
            #browser.is_element_present_by_id("market-details-" + eventId, wait_time = 4)
            #print "before search" , (time.time() - t)
            try : 
                event = browser.find_by_id("event_" + strId).first
            except Exception as error :
                throwError(1, "Browser.find_by_id failed. info = " + str(error))
            #print "search" , (time.time() - t)
            res += '-------\n' + eventId[0] + '\n' + eventId[1] + '\n'
            res += getInfo(event.html)
            res += 'a-------\n'
            #print "getting text" , (time.time() - t)
            #try :
            res = formatDataForEvent(eventId,res)
            #except Exception as error :
            #    throwError(2, "Format data failed. info = " + str(error))
            try :
                filename = getFileNameForEvent(eventId)
                f = open('./all_results/' + filename, 'w')
                f.write(res)
                f.close()
                if isParseAll :
                    print eventId[1].strip()
                    print eventId[2].strip()
                    print eventId[3].strip()
                else :
                    resForParseMatches.append(eventId)

            except Exception as error :
                throwError(3, "Writing result to file failed. info = " + str(error))    
        if isParseAll : saveState(toInd)    
        if (fromInd == finishInd - 1) or (toInd == finishInd): 
            break
        try :
            browser.reload()
        except Exception as error :
            throwError(1, "Browser.reload failed. info = " + str(error))
    browser.quit()
    
    if isParseAll : 
        saveState(toInd)
        if toInd == len(eventsId) : setEnd("True")
        return
    else :
        return resForParseMatches

def getDataForEvent(event):
    t = time.time()
    browser = Browser('chrome') #chrome phantomjs
    #print "init browser", (time.time() - t)
    try :
        browser.visit('http://www.betmarathon.com/en/popular/Football/')
    except Exception as error :
        throwError(1, "Browser.visit failed. info = " + str(error))
    
    #print "visit maraphon" , (time.time() - t)

    res = ''
    res += '-------\n' + event[0] + '\n' + event[1] + '\n'

    strId = event[0][:-1]
    #f.write(eventId[0] + '\n' + eventId[1] + '\n')
    try : 
        script = "Markets.applyView(document.getElementById('event-more-view-" + strId + "'));return false;"
        browser.execute_script(script);
    except Exception as error :
        throwError(1, "Browser.execute_script failed. info = " + str(error))
    #print "time after script" , (time.time() - t)
    #print "sleep"
    time.sleep(5)
    #print "wake up"
        
    #browser.is_element_present_by_id("market-details-" + eventId, wait_time = 4)
    #print "before search" , (time.time() - t)
    event2 = browser.find_by_id("event_" + strId).first
    #print "search" , (time.time() - t)
    res += getInfo(event2.html)
    res += 'a-------\n'
    #print "getting text" , (time.time() - t)
    try :
        res = formatDataForEvent(event,res)
    except Exception as error :
        throwError(2, "Format data failed. info = " + str(error))
        
    try :
        filename = getFileNameForEvent(event)
        f = open('./all_results/' + filename, 'w')
        f.write(res)
        f.close()
    except Exception as error :
        throwError(3, "Writing result to file failed. info = " + str(error))    
    browser.quit()
    
    return

#-------------------------
#-----state methods-------
#-------------------------
def getState():
    f = open('state.out', 'rw')
    f.readline()
    f.readline()
    state = int(f.readline())
    f.close()    
    return state
def initState():
    f = open('state.out', 'w')
    currTime = time.gmtime(time.time() + 3 * 60 * 60) # GMT + 03:00
    strDate = time.strftime("%Y-%m-%d %H:%M:00\n", currTime)
    f.write(strDate)
    f.write("GOSHA ZHUK\n")
    f.write('0')
    f.close()
    return
def saveState(state):
    f = open('state.out', 'r')#, encoding='utf-8'
    #print "New state = ", state
    lines = f.readlines()
    lines[2] = str(state)
    f = open('state.out', 'w')#, encoding='utf-8'c
    f.writelines(lines)
    f.close()    

    if state == 0 : setEnd("False")

    return
def printState():
    print open('state.out', 'r').read()
    return

def deleteState():
    if os.path.exists("state.out") :
        os.remove("state.out")

#-------------------------
#-------interface---------
#-------------------------
def init():
    if os.path.exists('init_final'):
        os.remove('init_final')        
    
    t = time.time()
    browser = Browser('chrome') #chrome phantomjs
    #print "init browser", (time.time() - t)
    browser.visit('http://www.betmarathon.com/en/popular/Football/')
    #browser.find_by_class('more-view').first.click()

    #print "visit maraphon" , (time.time() - t)
    #browser.execute_script("Markets.applyView(document.getElementById('event-more-view-2239781'));return false;");
    #print "execute_script0" , (time.time() - t)
    eventsContainerHTML = browser.find_by_id("container_EVENTS").first.html
    #print "search" , (time.time() - t)
    browser.quit()

    eventsId = getEvents(eventsContainerHTML, 500000)

    #print "created eventsId" , (time.time() - t)
    #sort by date
    eventsId.sort(key=lambda tup: tup[1]) 

    f = codecs.open('events.out', 'w', encoding='utf-8')

    f.write('' + str(len(eventsId)))
    for event in eventsId:
        f.write("\n" + event[0] + "\n" + event[1] + "\n" + event[2] + "\n" + event[3])    
            

    #print "eventsId stored" , (time.time() - t)
    
    initState()
    setEnd("False")
    if os.path.exists('all_results'):
        shutil.rmtree('all_results')
    os.makedirs('all_results')

    f = open('init_final', 'w')
    f.write('True')
    f.close()

    return

def parseAll(minMinutes, maxMinutes, amount):
    t = time.time()
    events = getEventsFromFile()
    #print "read events from file", (time.time() - t)
    events = filter(lambda tup: checkDate(tup[1], minMinutes, maxMinutes), events)
    
    #print "events filtered", (time.time() - t)

    currState = getState();
    
    if not(currState >= len(events)) :
        #there is unparsed events
        getDataForEvents(events, amount, currState, True)
        #print "data for events parsed", (time.time() - t)
    else :
        throwError(1,"no unparsed events")

    return

def parseMatch (strDate, strHome, strAway):
    t = time.time()
    events = getEventsFromFile()
    #print "read events from file", (time.time() - t)
    if checkDate(strDate, 0, 1000000) :
        for event in events :
            if event[1] == strDate and event[2] == strHome and event[3] == strAway :
                getDataForEvent(event)
                print True
                return
    print False
    #throwError(1, "no such event")
    return

def parseMatches (filename) :    
    t = time.time()
    events = getEventsFromFile()
    #print "read all events from file", (time.time() - t)

    matches = getMatchesFromFile(filename)

    events = filter(lambda event: (event[1], event[2], event[3]) in matches, events)
    #print events
    events = filter(lambda tup: checkDate(tup[1], 0, 1000000), events)
    #print events
    if len(events) > 0 :
        res = getDataForEvents(events, 1000, 0, False)
        res = map(lambda x: (x[1], x[2], x[3]), res)
        ans = map(lambda x: x in res, matches)
        for a in ans :
            print a

    return


def setEnd(value):
    f = open('isEnd.txt', 'w')
    f.write(value)
    f.close()
    return

def isEnd () :
    print open('isEnd.txt', 'r').readline()
    return

#-------------------------
#----------main-----------
#-------------------------
def main():
    if not os.path.exists('all_results'):
        os.makedirs('all_results')

    if len(sys.argv) == 1 : 
        throwError(1, "no args")
        return
    if len(sys.argv) > 1 :
        if sys.argv[1] == "init" :
            #print "init"
            init()
            return
        if sys.argv[1] == "parseAll" :
            #print "parse all"
            minMinutes = int(sys.argv[2])
            maxMinutes = int(sys.argv[3])
            amount = int(sys.argv[4])
            parseAll(minMinutes, maxMinutes, amount)
        if sys.argv[1] == "parseMatch" :
            #print "parse match"
            strDate = sys.argv[2] + "\n"
            strHome = sys.argv[3] + "\n"
            strAway = sys.argv[4] + "\n"
            parseMatch(strDate, strHome, strAway)
        if sys.argv[1] == "parseMatches" :
            #print "parse matches"
            filename = sys.argv[2]
            parseMatches(filename)
        if sys.argv[1] == "reset" :
            #print "reset"
            saveState(0)
            #print "reset done"
        if sys.argv[1] == "isEnd" :
            #print "isEnd"
            isEnd()
        if sys.argv[1] == "getState" :
            #print "getState"
            printState()
        if sys.argv[1] == "deleteState" :
            #print "delete state"
            deleteState()
        
        if sys.argv[1] == "testFormat" :
            #print "test format"
            testFormat()

    return

main()
#try :
#    main()    
#except Exception as error:
#    throwError(0, "Unknown error; info = " + str(error))
    
