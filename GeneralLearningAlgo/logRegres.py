'''
Created on Oct 27, 2010
Logistic Regression Working Module
@author: Peter
'''
from numpy import *
from modelSelection import *
import random

BATCH_GRAD_DESCENT = 0
STOCH_GRAD_DESCENT = 1
NEWTON_METHOD = 2

class logRegModel(Model):



#algoType to indicate which algorithm need to be applied
#x_tested is the imput vector
def logisticRegression(x, y, alpha, maxCycles, errThreshold, algoType, x_tested):
    if algoType ==  BATCH_GRAD_DESCENT:
        theta = batchGradAscent(x, y, alpha, maxCycles, errThreshold)
    elif algoType == STOCH_GRAD_DESCENT:
        theta = stochaGradAscent(x,y,alpha)
    elif algoType == NEWTON_METHOD:
        theta = newtonMethod(x,y, maxCycles, errThreshold)
    else:
        print "algoType is not valid, %d"%(algoType)
        assert 0

    y_estimated = sigmoid(x_tested*theta)

    if y_estimated >= 0.5:
        return 1
    else:
        return 0





def sigmoid(z):
    return 1.0/(1+exp(-z))

def newtonMethod(x,y, maxCycles, errThreshold):
    xMat = mat(x)
    yMat = mat(y).transpose()

    # m: data sample number ;  n: feature number
    mx,nx = shape(xMat)
    print "for xMat, mx=%d, nx=%d"%(mx,nx)
    my,ny = shape(yMat)
    print "for yMat, my=%d, ny=%d"%(my,ny)

    if mx!=my :
        print "xMat's line count should equals yMat's"
        assert(0)

    theta = ones((nx, 1))

    for i in range(maxCycles):
        h = sigmoid(xMat*theta)
        err = yMat - h

         #We should set an error threshold
        if abs(amax(err)) <= errThreshold:
            print "Now estimation error %f is less than errThreshold, iteration will break"%(err)
            break

        grad = xMat.T * err

        #TODO how to caculate Hessian Matrix

    return  theta



def batchGradAscent(x, y, alpha, maxCycles , errThreshold):
    xMat = mat(x)
    yMat = mat(y).transpose()

    # m: data sample number ;  n: feature number
    mx,nx = shape(xMat)
    print "for xMat, mx=%d, nx=%d"%(mx,nx)
    my,ny = shape(yMat)
    print "for yMat, my=%d, ny=%d"%(my,ny)

    if mx!=my :
        print "xMat's line count should equals yMat's"
        assert(0)

    theta = ones((nx, 1))

    for k in range(maxCycles):
        h = sigmoid(xMat*theta)

        err = yMat - h

        #We should set an error threshold
        if abs(amax(err)) <= errThreshold:
            print "Now estimation error %f is less than errThreshold, iteration will break"%(err)
            break
        # theta: n by 1 ; xMat: m by n; err:m by 1
        theta = theta + alpha * xMat.transpose() * err

    print "Final error is %f"%(err)
    return theta


def batchGradDescent(x, y, alpha, maxCycles , errThreshold):
    xMat = mat(x)

    my,ny = shape(yMat)

    if ny > 1 :
        #Only transpose y if y is a line vector
        yMat = mat(y).transpose()


    # m: data sample number ;  n: feature number
    mx,nx = shape(xMat)
    print "for xMat, mx=%d, nx=%d"%(mx,nx)

    print "for yMat, my=%d, ny=%d"%(my,ny)

    if mx!=my :
        print "xMat's line count should equals yMat's"
        assert(0)

    theta = ones((nx, 1))

    for k in range(maxCycles):
        h = sigmoid(xMat*theta)

        err = yMat - h

        #We should set an error threshold
        if abs(amax(err)) <= errThreshold:
            print "Now estimation error %f is less than errThreshold, iteration will break"%(err)
            break
        # theta: n by 1 ; xMat: m by n; err:m by 1
        theta = theta - alpha * xMat.transpose() * err

    print "Final error is %f"%(err)
    return theta


#The original Stochastic Gradient Ascent
def stocGradAscent0(x, y, alpha):
    m,n = shape(x)
    theta = ones(n)   #initialize to all ones

    for i in range(m):
        h = sigmoid(sum(x[i]*theta))
        err = y[i] - h
        theta = theta + alpha * err * x[i]

    return theta

#The original Stochastic Gradient Descent
def stocGradDescent0(x, y, alpha):
    m,n = shape(x)
    theta = ones(n)   #initialize to all ones

    for i in range(m):
        h = sigmoid(sum(x[i]*theta))
        err = y[i] - h
        theta = theta - alpha * err * x[i]

    return theta

#An optimized Stochastic Gradient Ascent
def stochaGradAscent(x, y, alpha, iterNum, errTheshold):
    m,n = shape(x)
    theta = ones(n)   #initialize to all ones

    if errTheshold <= 0:
        print "Warning errThreshold: %f is invalid, it has to be larger than 0"%errTheshold

    for j in range(iterNum):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+alpha    #apha decreases with iteration, does not
            randIndex = int(random.choice(dataIndex))#go to 0 because of the constant
            h = sigmoid(sum(x[randIndex]*theta))
            err = y[randIndex] - h

            if abs(amax(err)) <= errTheshold :
                print "error %f has converged"%(err)
                break

            theta = theta + alpha * err * x[randIndex]

            del(dataIndex[randIndex])

    return theta


#An optimized Stochastic Gradient Ascent
def stochaGradDescent(x, y, alpha, iterNum, errTheshold):
    m,n = shape(x)
    theta = ones(n)   #initialize to all ones

    if errTheshold <= 0:
        print "Warning errThreshold: %f is invalid, it has to be larger than 0"%errTheshold

    for j in range(iterNum):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+alpha    #apha decreases with iteration, does not
            randIndex = int(random.choice(dataIndex))#go to 0 because of the constant
            h = sigmoid(sum(x[randIndex]*theta))
            err = y[randIndex] - h

            if abs(err) <= errTheshold :
                print "error %f has converged"%(err)
                break

            theta = theta - alpha * err * x[randIndex]

            del(dataIndex[randIndex])

    return theta

def classifyVector(x, theta):
    prob = sigmoid(sum(x*theta))
    if prob > 0.5: return 1.0
    else: return 0.0



def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0] 
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()




def colicTest():
    frTrain = open('horseColicTraining.txt'); frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000)
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print "the error rate of this test is: %f" % errorRate
    return errorRate

def multiTest():
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest()
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))
        