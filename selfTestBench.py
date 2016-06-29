#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

from dataParser import NBATeamStat
import  re

html = r'<a href = "./game/37525.html" target = "_blank">DEADDEAD<a href = "./game/12345.html" target = "_blank">'
test_html = "vgame/37525.html"


QueryType='game'
GameType='season'
Team_id='GSW'
Season0='2015'
Season1='2016'
PlayerName = '斯蒂芬-库里'

GSWTeamStat = NBATeamStat(QueryType,GameType,Team_id,Season0,Season1, PlayerName)


GSWTeamStat.parseAllGamesFromSeasonData()