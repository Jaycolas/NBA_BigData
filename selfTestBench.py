#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

from dataParser import *
from kNN import *
import numpy as np
import util
import os
import sys
import matplotlib.pyplot as plt



#util.createLogFileAndRedrect()

QueryType='game'
GameType='season'
Team_id='GSW'
Season0='2015'
Season1='2016'
PlayerName = '斯蒂芬-库里'

k = 10
hoRatio = 0.2

'''
GSWTeamStat = NBATeamStat(QueryType,GameType,Team_id,Season0,Season1, PlayerName)
StephCurryDataMatrix = GSWTeamStat.parseAllGamesFromSeasonData()
game_count, stat_number = np.shape(StephCurryDataMatrix)
print "Size of the Player Data Matrix is %d, %d"%(game_count,stat_number)

kNNClassifywithNorm(StephCurryDataMatrix[:,(THREEP, ASSIT)], StephCurryDataMatrix[:,stat_number-1], k, hoRatio)'''


Team_id = 'CHI'
PlayerName = '保罗-加索尔'
CHITeamStat = NBATeamStat(QueryType,GameType,Team_id,Season0,Season1, PlayerName)
PauGasolDataMatrix = CHITeamStat.parseAllGamesFromSeasonData()
game_count, stat_number = np.shape(PauGasolDataMatrix)
print "Size of the Player Data Matrix is %d, %d"%(game_count, stat_number)

kNNClassifywithNorm(PauGasolDataMatrix[:,(REB, POINTS)], PauGasolDataMatrix[:,stat_number-1], k, hoRatio)


#Below are for figure drawing

x_stat_index = REB
y_stat_index = POINTS
TestMatrix = PauGasolDataMatrix

x_vector = TestMatrix[:, x_stat_index]
y_vector = TestMatrix[:, y_stat_index]

x_win = []
y_win = []
x_lose = []
y_lose = []

for i in range(game_count):
    if TestMatrix[i, WIN_LOSE] == 1:
        x_win.append(TestMatrix[i,x_stat_index])
        y_win.append(TestMatrix[i,y_stat_index])
    elif TestMatrix[i, WIN_LOSE] == 0:
        x_lose.append(TestMatrix[i, x_stat_index])
        y_lose.append(TestMatrix[i, y_stat_index])
    else:
        print "WIN: 1; LOSE: 0, it has to be one number, can not be %d"%TestMatrix[i, WIN_LOSE]
        assert(0)




fig = plt.figure()
ax = fig.add_subplot(111)
#datingDataMat,datingLabels = kNN.file2matrix('datingTestSet.txt')
#ax.scatter(datingDataMat[:,1], datingDataMat[:,2])
#ax.scatter(x_vector, y_vector)
#ax.axis([-2,25,-0.2,2.0])

win_dots = ax.scatter(x_win, y_win,c='blue')
lose_dots = ax.scatter(x_lose, y_lose, c='red')
ax.legend([win_dots, lose_dots], ["WIN", "LOST"], loc=2)


plt.xlabel('Rebounds')
plt.ylabel('Points')
plt.title("Paul Gasol's Stat Analysis")
plt.show()


