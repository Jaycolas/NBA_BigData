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


def biKmeans(dataSet, k, distMeas=distEclud):
    
    m = shape(dataSet)[0] #m is the sample number
    clusterAssment = mat(zeros((m,2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0] # the first element of the tolist result
    centList =[centroid0] #create a list with one centroid
    for j in range(m):#calc initial Error
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i

            #centroidMat is the 2 centroids of cluster i, splitClustAss only has two categories
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)

            #Get all the sse for splited result
            sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum

            #get all the samples which does not below to cluster i
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])

            print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                #update the best centroid to split
                bestCentToSplit = i
                #bestNewCent's keep the new 2 centroid divided
                bestNewCents = centroidMat
                #bestCustAss save the splitted cluster's feature
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit

        #This is the tricky part
        #Currently the number of centers we have is len(centList), so the maximum cluster number should be len(centList)-1
        #So in this case since we have a new cluster, we are having a [len(centList)-1]+1 cluster
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit

        print 'the bestCentToSplit is: ',bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
    return mat(centList), clusterAssment