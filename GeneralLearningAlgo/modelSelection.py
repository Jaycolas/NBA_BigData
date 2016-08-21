#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

import numpy as np

class Model:

    #Using this flag to indicate if the model is trained or not, if not, calcTrainingErr will not proceed
    _isTrained = False

    def modelTraining(self, x_train, y_train):
        print "Abstract Layer, for modelTraining"

    def calcTrainingErr(self, x_validation, y_validation):
        print "Abstract Layer, for calculating training error"
        return 0


class modelSelection:

    #For normal cross-validation, define para like below
    _trainingPer = 0.3
    _validationPer = 0.7
    _x = np.zeros(10)
    _y = np.zeros(10)
    _models = {}

    #k Fold CV para
    _kFold = 10

    def __init__(self, x, y, trainingPer, validationPer, kFold, modelArr):
        self._trainingPer = trainingPer
        self._validationPer = validationPer
        self._kFold = kFold
        self._x = x
        self._y = y
        self._models = modelArr

    #Given x, and y, using _trainPer and _validationPer to seperate the training sample
    def randomSeperate(self, x,y):
        #m for sample number and n for feature number
        m,n = np.shape(x)
        if m!=np.shape(y)[0] or np.shape(y)[1]!=1:
            print "label dimension is not matching input x"

        numValidationVec = m * self._validationPer

        validationVecIdxArr = np.random.sample(range(m), numValidationVec)
        validationVecIdxArrSet = set(validationVecIdxArr)
        wholeSet = set(range(m))
        trainVecIdxSet = wholeSet.difference(validationVecIdxArrSet)
        trainVecIdxArr = list(trainVecIdxSet)

        return trainVecIdxArr, validationVecIdxArr

    def kFoldSeperate(self, x, y):
        #m for sample number and n for feature number
        m,n = np.shape(x)
        if m!=np.shape(y)[0] or np.shape(y)[1]!=1:
            print "label dimension is not matching input x"

        subSetNum = m/k
        totalSet = set(range(m))
        S = {}
        for i in range(self._kFold):
            currentSet = totalSet - S[i-1]
            #Considering the case that m can not be divided by k
            if len(currentSet) < subSetNum:
                subSetNum = len(currentSet)
            S[i] = np.random.choice(currentSet,subSetNum)

        return S




    def crossValidation(self, x_train, y_train, x_validate, y_validate, model):


        model.modelTraining(x_train, y_train)
        trainErr = model.calcTrainingErr(x_validate, y_validate)

        return trainErr


    def crossValidationOnWholeSet(self):
        trainVecIdxArr, validationVecIdxArr = self.randomSeperate(self._x, self._y)
        x_train = self._x[trainVecIdxArr,:]
        y_train = self._y[trainVecIdxArr,:]
        x_validate = self._x[validationVecIdxArr,:]
        y_validate = self._y[validationVecIdxArr,:]

        minTrainingError = float("inf")
        bestModel = Model(0,0)

        for model in self._models:
            trainErr = self.crossValidation(x_train, y_train, x_validate, y_validate, model)
            if trainErr < minTrainingError:
                minTrainingError = trainErr
                bestModel = model
        return bestModel


    def kFoldCrossValidation(self):
        S = self.kFoldSeperate(self._x, self._y)

        minTrainingError = float("inf")
        bestModel = Model(0,0)

        for model in self._models:

            err_sum=0
            err = []

            for j in range(self._kFold):
                x_validate = self._x[S[j],:]
                y_validate = self._x[S[j],:]

                S_train = S.copy()
                del S_train[j]

                m,n = np.shape(S_train)
                S_train_1dim = np.reshape(S_train,1, m*n)

                x_train = self._x[S_train_1dim,:]
                y_train = self._y[S_train_1dim,:]

                err[j]=self.crossValidation(x_train,y_train,x_validate,y_validate,model)
                err_sum+=err[j]

            if err_sum < minTrainingError:
                minTrainingError = err_sum
                bestModel = model

        return bestModel













