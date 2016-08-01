#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Jaycolas'

from numpy import *
import math

#This function is to return the k random center of the whole dataset.
#By finding the range of each feature, we can make sure all of the centers found are among the whole dataset.
def randCent(dataSet, k):
    m, n = shape(dataSet)

    if m<=0 or n<=0 :
        print "dataSet input is invalid, nothing will be generated"
        assert(0)

    if k<= 0:
        print "value k must be greater than 0"
        assert 0

    centroids = mat(zeros((k,n)))#create centroid mat
    for j in range(n):#create random cluster centers, within bounds of each dimension
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        # numpy.random.rand: Create an array of the given shape and populate it with random samples from a uniform distribution over [0, 1)
        centroids[:,j] = mat(minJ + rangeJ * (random.rand(k, 1)))
    return centroids

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m, n = shape(dataSet)

    if m<=0 or n<=0 :
        print "dataSet input is invalid, nothing will be generated"
        assert(0)

    #For the two columns of cluster Assement , the first one is the centroid index, 2nd one is the distance
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False

        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1

            #for data sample i, calculate its distance with all k centoids,
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j

            #if minIndex is changed, mark clusterChanged equal to True, keep on the loop
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids


        #To re-calculate the centroids
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean

    return centroids, clusterAssment

