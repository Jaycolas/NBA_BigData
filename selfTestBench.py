#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

from dataParser import NBATeamStat
from kNN import *
import numpy as np


QueryType='game'
GameType='season'
Team_id='GSW'
Season0='2015'
Season1='2016'
PlayerName = '斯蒂芬-库里'

GSWTeamStat = NBATeamStat(QueryType,GameType,Team_id,Season0,Season1, PlayerName)
StephCurryDataMatrix = GSWTeamStat.parseAllGamesFromSeasonData()
m,n = np.shape(StephCurryDataMatrix)
print "Size of the Player Data Matrix is %d, %d"%(m,n)

kNNClassifywithNorm(StephCurryDataMatrix[:,0:n-2], StephCurryDataMatrix[:,n-1], 6)


Team_id = 'CHI'
PlayerName = '保罗-加索尔'
CHITeamStat = NBATeamStat(QueryType,GameType,Team_id,Season0,Season1, PlayerName)
PauGasolDataMatrix = CHITeamStat.parseAllGamesFromSeasonData()
m,n = np.shape(PauGasolDataMatrix)
print "Size of the Player Data Matrix is %d, %d"%(m,n)

kNNClassifywithNorm(PauGasolDataMatrix[:,0:n-2], PauGasolDataMatrix[:,n-1], 6)