#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'



from numpy import *
from modelSelection import *
import random

import operator


class kNNModel(Model):

    #The only
    _k = 0
    _x_train = np.zeros(10)
    _y_train = np.zeros(10)
    def __init__(self,k):
        self._k = k
        #No training is required for kNN
        #self._isTrained = True

    def modelTraining(self, x_train, y_train):
        print "This is kNN and nothing need to be trained"
        self._isTrained = True
        self._x_train = x_train
        self._y_train = y_train

    def calcTrainingErr(self, x_validation, y_validation):




    '''
    Below code using the first "numTestVec" samples as test vector, need to change it into random selection
    for i in range(numTestVec):
        classifierResult = classify0(normMat[i, :], normMat[numTestVec:m, :], dataLabels[numTestVec:m],k)
        print "The classifier comes back with %d, the real answer is %d" %(classifierResult, dataLabels[i])
        if (classifierResult != dataLabels[i]): errorCount+=1.0
    '''
    print "The failure rate is %f" %(errorCount/float(numTestVec))



def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0,0], [0,0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group,labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    # calcualte the distance
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2

    # sum has argment (axis=1), which means it sum all the elements in every line
    sqDistance = sqDiffMat.sum(axis=1)
    distances = sqDistance*0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}

    #Found out the closest k
    for i in range(k):
        voteLabel = labels[sortedDistIndicies[i]]
        classCount[voteLabel]=classCount.get(voteLabel,0)+1

    #Sorting
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    try:
        fr=open(filename)
    except IOError,e:
        print e.message

    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0

    #Parsing file data to list
    for line in arrayOfLines:
        line=line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector


def autoNorm(dataSet):
    #For debug purpose#####
    print dataSet
    print dataSet.min
    print dataSet.max
    #######################
    minVal = dataSet.min(0)
    maxVal = dataSet.max(0)
    ranges = maxVal - minVal
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVal, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVal

def datingClassTest():
    hoRatio = 0.05
    datingDataMat,datingLabels = file2matrix('./machinelearninginaction/Ch02/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVec = int(m*hoRatio)
    errorCount = 0
    for i in range(numTestVec):
        classifierResult = classify0(normMat[i, :], normMat[numTestVec:m, :], datingLabels[numTestVec:m],3)
        print "The classifier comes back with %d, the real answer is %d" %(classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0

    print "The failure rate is %f" %(errorCount/float(numTestVec))

def kNNClassifywithNorm(dataMat, dataLabels, k, hoRatio):
    normMat, ranges, minVals = autoNorm(dataMat)
    m = normMat.shape[0]
    numTestVec = int(m*hoRatio)
    print "Tobal samples are ", m, "Test Vec using are ", numTestVec

    errorCount = 0
    testVecIdxArr = random.sample(range(m), numTestVec)
    testVecIdxArrSet = set(testVecIdxArr)
    wholeSet = set(range(m))
    trainVecIdxSet = wholeSet.difference(testVecIdxArrSet)
    trainVecIdxArr = list(trainVecIdxSet)

    print "Test Vector Index Array are", testVecIdxArr
    print "Train Vector Index Array are", trainVecIdxArr

    for i in testVecIdxArr:
        classifierResult = classify0(normMat[i, :], normMat[trainVecIdxArr, :], dataLabels[trainVecIdxArr],k)
        print "The classifier comes back with %d, the real answer is %d" %(classifierResult, dataLabels[i])
        if (classifierResult != dataLabels[i]): errorCount+=1.0



    '''
    Below code using the first "numTestVec" samples as test vector, need to change it into random selection
    for i in range(numTestVec):
        classifierResult = classify0(normMat[i, :], normMat[numTestVec:m, :], dataLabels[numTestVec:m],k)
        print "The classifier comes back with %d, the real answer is %d" %(classifierResult, dataLabels[i])
        if (classifierResult != dataLabels[i]): errorCount+=1.0
    '''
    print "The failure rate is %f" %(errorCount/float(numTestVec))
