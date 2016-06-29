#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

import urllib
import urllib2
import re
import os
import util

GSWSeasonDataPage = 'http://stat-nba.com/query_team.php?crtcol=date_out&order=0&QueryType=game&GameType=season&Team_id=GSW&PageNum=1000&Season0=2015&Season1=2016'

GSWPECDataPage='http://stat-nba.com/game/37770.html'
WGAME_PAGE = 'http://stat-nba.com/game/37770.html'
INVALID_STRING = 'Invalid String'
CURRENT_PATH = os.getcwd()+'/'


class NBATeamStat:
    #order 0 means ascending time period, while 1 means descending time period
    _order = 0
    #QueryType has game, player, etc..
    _QueryType = INVALID_STRING
    #Game type has season, post se# anson, play off
    _GameType = INVALID_STRING
    #Team_id, specify which team you need to query
    _Team_id = INVALID_STRING
    #Page Number is 1000 by default
    _PageNum = 1000
    #Season 0, the start year of the season
    _Season0 = INVALID_STRING
    #Season 1, the end year of the season
    _Season1 = INVALID_STRING
    #Final constructed website
    _htmlWebSite = INVALID_STRING
    #The file path which is used to store the html
    _dataStoredPath = INVALID_STRING
    #HTML file to store the whole season schedule data
    _seasonDataHtmlFile = INVALID_STRING
    #Player's name
    _playerName = INVALID_STRING


    def __init__(self, QueryType, GameType, Team_id, Season0, Season1, playerName):
        self._order = 0 #Let's use ascending order by default
        self._QueryType =  QueryType
        self._GameType = GameType
        self._Team_id = Team_id
        self._Season0 = Season0
        self._Season1 = Season1
        self._htmlWebSite = 'http://stat-nba.com/query_team.php?crtcol=date_out&order=0&QueryType='+QueryType+'&GameType='+GameType+'&Team_id='+Team_id+'&PageNum=1000&Season0='+Season0+'&Season1='+Season1
        self._playerName = playerName
        print "htmlWebSite constructed is "+self._htmlWebSite

    def getTeamSeasonHtml(self):
        html = INVALID_STRING
        if cmp(self._htmlWebSite, INVALID_STRING) == 0:
            print "htmlWebSite has not been initialized yet"
        else:
            #If we have already synced the data we need to fetch the html from local instead of reloading the website again
            pathNeed2Test = CURRENT_PATH + self._Season0 + self._Season1 + '/' + self._Team_id
            print "Constructing path as ", pathNeed2Test
            self._dataStoredPath = pathNeed2Test
            util.mkdir(pathNeed2Test)

            htmlFile = pathNeed2Test + '/' + self._GameType + '.html'
            self._seasonDataHtmlFile = htmlFile
            print "Check if html file exist or not ", htmlFile

            if os.path.isfile(htmlFile):
                print "html file exists, open the file, read it and return the string"
                html = util.openFile(htmlFile)

                #print html
            else:
                print "html file does not exist, now loading the webpage from network"
                html = util.getHtmlFromUrl(self._seasonDataHtmlFile)

                if cmp(html, INVALID_STRING)!=0:
                    util.saveFile(htmlFile,html)

                return html


        return html

    def parseAllGamesFromSeasonData(self):
        seasonDataHtml = self.getTeamSeasonHtml()
        #print seasonDataHtml
        if cmp(seasonDataHtml, INVALID_STRING)!=0 :
            singleGameLinkPattern = re.compile('game/\d+.html')
            winOrLosePattern = re.compile('<td.*?class="normal wl change_color col3.*?">(.*?)</td>')
            homeOrAwayPattern = re.compile('<td.*?class="normal ha change_color col4.*?">(.*?)</td>')
            #gameResultPattern = re.compile('<a href="./game/\d+.html" target="_blank">(.*?)</a>')
            #gameResultPattern = re.compile(r'<a href="./game/38577.html" target="_blank">鹈鹕107-125勇士</a>')
            #gameResultPattern = re.compile('\"\./game/38577.html')

            gameLinkMatch = re.findall(singleGameLinkPattern, seasonDataHtml)
            winOrLose = re.findall(winOrLosePattern, seasonDataHtml)
            homeOrAway = re.findall(homeOrAwayPattern, seasonDataHtml)
            #gameResult = re.findall(gameResultPattern, seasonDataHtml)

            #Try print all the matched game
            print gameLinkMatch, winOrLose, homeOrAway
            print len(gameLinkMatch), len(winOrLose), len(homeOrAway)

            winOrLoseNumer = []
            for game in winOrLose:
                if cmp(game, '胜') == 0:
                    singleGame = 1
                elif cmp(game, '负') == 0:
                    singleGame = 0
                else:
                    print "Invalid game result"
                    singleGame = -1

                winOrLoseNumer.append(singleGame)

            print winOrLoseNumer

            #for gameLink in gameLinkMatch:
            #    singleGameHtml = self.getSingleGameHtml(gameLink)
            #    singlePlayerDataHtml = self.parseData4SinglePlayer(self._playerName, singleGameHtml)
            #    self.storeDataForSingleMatch(singlePlayerDataHtml)

            singleGameHtml = self.getSingleGameHtml(gameLinkMatch[0])
            singlePlayerDataHtml = self.parseData4SinglePlayer(self._playerName, singleGameHtml)
            print "singlePlayerDataHtml is "+ singlePlayerDataHtml
            self.storeDataForSingleMatch(singlePlayerDataHtml)




    def getSingleGameHtml(self, singleGameLink):
        singleGameUrl = 'http://stat-nba.com/'+singleGameLink
        singleGameHtmlFileName = re.sub('\/', '_', singleGameLink)
        print singleGameHtmlFileName
        singleGameHtmlFilePath = self._dataStoredPath + '/' + singleGameHtmlFileName
        print singleGameHtmlFilePath

        singleGameHtml = INVALID_STRING
        if os.path.isfile(singleGameHtmlFilePath):
            #If html file exist, read it and return the html content
            print singleGameHtmlFilePath+ " exist, open the file and read it"
            singleGameHtml = util.openFile(singleGameHtmlFilePath)
        else:
            print singleGameHtmlFilePath + " doesn't exist, load the webpage"
            singleGameHtml = util.getHtmlFromUrl(singleGameUrl)
            util.saveFile(singleGameHtmlFilePath, singleGameHtml)
        return  singleGameHtml



    def parseData4SinglePlayer(self, playerName, singleGameHtml):
        print playerName
        playerTotalDataPattern = re.compile('<a href="/player/\d+.html" target="_blank">'+playerName+'</a>.*?normal pts change_color col21 row\d" rank="\d+">\d+</td>', re.S)
        playerTotalDataHtml = re.findall(playerTotalDataPattern, singleGameHtml)
        return playerTotalDataHtml[0]

#HTML cut for a single player's data
#<tr class="sort">
#										<td style="border:0px;"></td>
#										<td class="normal player_name_out change_color col0 row0"><a href="/player/526.html" target="_blank">斯蒂芬-库里</a></td>
#										<td class="current gs change_color col1 row0" rank="1">1</td>
#										<td class="normal mp change_color col2 row0" rank="30">30</td>
#										<td class="normal fgper change_color col3 row0" rank="0.625">62.5%</td>
#										<td class="normal fg change_color col4 row0" rank="15">15</td>
#										<td class="normal fga change_color col5 row0" rank="24">24</td>
#										<td class="normal threepper change_color col6 row0" rank="0.5263157894736842">52.6%</td>
#										<td class="normal threep change_color col7 row0" rank="10">10</td>
#										<td class="normal threepa change_color col8 row0" rank="19">19</td>
#										<td class="normal ftper change_color col9 row0" rank="1">100.0%</td>
#										<td class="normal ft change_color col10 row0" rank="6">6</td>
#										<td class="normal fta change_color col11 row0" rank="6">6</td>
#										<td class="normal ts change_color col12 row0" rank="0.86336336336336">86.3%</td>
#										<td class="normal trb change_color col13 row0" rank="4">4</td>
#										<td class="normal orb change_color col14 row0" rank="1">1</td>
#										<td class="normal drb change_color col15 row0" rank="3">3</td>
#										<td class="normal ast change_color col16 row0" rank="6">6</td>
#										<td class="normal stl change_color col17 row0" rank="2">2</td>
# 										<td class="normal blk change_color col18 row0" rank="0">0</td>
#										<td class="normal tov change_color col19 row0" rank="2">2</td>
#										<td class="normal pf change_color col20 row0" rank="2">2</td>
#										<td class="normal pts change_color col21 row0" rank="46">46</td>
#									</tr>


    def storeDataForSingleMatch(self, singlePlayerDataHtml):
        startLineUpPattern = re.compile('<td class ="current gs change_color col1 row\d+" rank="\d+">(\d+)</td>', re.S)
        minutesPlayedPattern = re.compile('<td class ="normal mp change_color col2 row\d+" rank="\d+">(\d+)</td>',re.S)
        fieldGoalPercentagePattern = re.compile('<td class ="normal fgper change_color col3 row\d+" rank="(.*?)"', re.S)
        fieldGoalPattern = re.compile('<td class ="normal fg change_color col4 row\d+" rank="\d+">(\d+)</td>', re.S)
        filedGoalAttemptedPattern = re.compile('<td class ="normal fga change_color col5 row\d+" rank="\d+">(\d+)</td>', re.S)
        threePPerPattern = re.compile('<td class ="normal threepper change_color col6 row\d+" rank="(.*?)">', re.S)
        threePPattern = re.compile('<td class ="normal threep change_color col7 row\d+" rank="\d+">(\d+)</td>', re.S)
        threePAPattern = re.compile('<td class ="normal threepa change_color col8 row\d+" rank="\d+">(\d+)</td>', re.S)
        ftPerPattern = re.compile('<td class ="normal ftper change_color col9 row\d+" rank="(.*?)">', re.S)
        ftPattern = re.compile('<td class ="normal ft change_color col10 row\d+" rank="\d+">(\d+)</td>', re.S)
        ftAPattern = re.compile('<td class ="normal fta change_color col11 row\d+" rank="\d+">(\d+)</td>', re.S)
        totalRebPattern = re.compile('<td class ="normal trb change_color col13 row\d+" rank="\d+">(\d+)</td>', re.S)
        offRebPattern = re.compile('<td class ="normal orb change_color col14 row\d+" rank="\d+">(\d+)</td>', re.S)
        defRebPattern = re.compile('<td class ="normal drb change_color col15 row\d+" rank="\d+">(\d+)</td>', re.S)
        assistPattern = re.compile('<td class ="normal ast change_color col16 row\d+" rank="\d+">(\d+)</td>', re.S)
        stealPattern = re.compile('<td class ="normal stl change_color col17 row\d+" rank="\d+">(\d+)</td>', re.S)
        blkPattern = re.compile('<td class ="normal blk change_color col18 row\d+" rank="\d+">(\d+)</td>', re.S)
        tovPattern = re.compile('<td class ="normal tov change_color col19 row\d+" rank="\d+">(\d+)</td>',re.S)
        pFoulPattern = re.compile('<td class ="normal pf change_color col20 row\d+" rank="\d+">(\d+)</td>', re.S)
        ptsPattern = re.compile('<td class ="normal pts change_color col21 row\d+" rank="\d+">(\d+)</td>', re.S)

        startLineUp = re.findall(startLineUpPattern, singlePlayerDataHtml)
        print "startline up is ", startLineUp
        minutesPlayed = re.findall(minutesPlayedPattern, singlePlayerDataHtml)
        print "minutes played is ", minutesPlayed
        fieldGoalPercentage = re.findall(fieldGoalPercentagePattern, singlePlayerDataHtml)
        print "field goal percentage is ", fieldGoalPercentage
        fieldGoal = re.findall(fieldGoalPattern, singlePlayerDataHtml)
        print "field goal is ", fieldGoal
        fieldGoalAttempted = re.findall(filedGoalAttemptedPattern, singlePlayerDataHtml)
        print "field goal attempted is ", fieldGoalAttempted
        threePPer = re.findall(threePPerPattern, singlePlayerDataHtml)
        print "3 pointer percentage is ", threePPer
        threeP = re.findall(threePPattern, singlePlayerDataHtml)
        print "3 pointer made is", threeP
        threePA = re.findall(threePAPattern, singlePlayerDataHtml)
        print "3 pointer atempted is ", threePA
        ftPer = re.findall(ftPerPattern, singlePlayerDataHtml)
        print "freethrow percentage is ", ftPer
        ft = re.findall(ftPattern, singlePlayerDataHtml)
        print "freethrow is ", ft
        ftA = re.findall(ftAPattern, singlePlayerDataHtml)
        print "freethrow attempted is ", ftA
        totalReb = re.findall(totalRebPattern, singlePlayerDataHtml)
        print "total rebound number is ", totalReb
        offReb = re.findall(offRebPattern, singlePlayerDataHtml)
        print "offensive rebound number is ", offReb
        defReb = re.findall(defRebPattern, singlePlayerDataHtml)
        print "defensive reboudn number is ", defReb
        assist = re.findall(assistPattern, singlePlayerDataHtml)
        print "assitant is ", assist
        steal = re.findall(stealPattern, singlePlayerDataHtml)
        print "steal is ", steal
        block = re.findall(blkPattern, singlePlayerDataHtml)
        print "block is ", block
        turnOver = re.findall(tovPattern, singlePlayerDataHtml)
        print "turnover is ", turnOver
        pFoul = re.findall(pFoulPattern, singlePlayerDataHtml)
        print "personal Foul is", pFoul
        points = re.findall(ptsPattern, singlePlayerDataHtml)
        print "points is", points

























