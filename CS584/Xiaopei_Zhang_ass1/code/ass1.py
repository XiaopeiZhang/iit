__author__ = 'Xiaopei'

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
from pylab import *
from random import shuffle
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import datetime

# get both X, y
def load_data(filename):
    arr = np.loadtxt(filename)
    return arr

# 10 fold
def tenFold(arr):
    shuffle(arr)
    for k in range(10):
        train = [x for i, x in enumerate(arr) if i % 10 != k]
        test = [x for i, x in enumerate(arr) if i % 10 == k]
        yield train, test

# split X, y
def splitXy(arr):
    n = len(arr[0])
    X, y = [], []
    for i in arr:
        X.append(i[:n - 1])
        y.append(i[n - 1])
    return X,y

# get Z for linear regression
def getZLinear(X):
    Z = ones(shape=(len(X), len(X[0]) + 1))
    Z[:, 1:] = X
    return Z

# linear regression
def regression(Z, y):
    theta = dot(pinv(Z), y)
    return theta

# compute error
def computeError(theta, Z, y):
    y_hat = dot(Z, theta)
    m = len(y)
    MSE = np.sum(np.square(np.subtract(y_hat, y))) / m
    #RSE = np.sum(np.divide(np.square(np.subtract(y_hat, y)), np.square(y))) / m
    return MSE#, RSE

# plot linear model on data
def plotLinearModel(X, Y, x, Z, theta):
    y_hat = dot(Z, theta)
    plt.scatter(X, Y, lw=2)
    plt.plot(x, y_hat, marker='o', c='b')
    plt.show()

# form printout
def formPrintout(s1, n1, s2, n2):
    return s1 + str(n1) + '. ' + s2 + str(n2) + '.'

# get Z for polynomial regression
def getZPolynomial(X):
    Z5 = ones(shape=(len(X), len(X[0]) + 5))
    Z5[:, 1] = X
    for x in Z5:
        x[2] = x[1]**2
        x[3] = x[1]**3
        x[4] = x[1]**4
        x[5] = x[1]**5
    return Z5[:, :3], Z5[:, :4], Z5[:, :5], Z5

# reduce training data by half
def reduceTrainingData(dataSet):
    n = len(dataSet)
    return dataSet[:n / 2]

# map to higher dimensional Z 2 and 3 degree, combination of features
def mapZ(X):
    Z2 = []
    n = len(X[0])
    for x in X:
        row = np.array([1])
        row = np.append(row, x)
        for i in range(n):
            for j in range(i, n):
                row = np.append(row, np.array([x[i] * x[j]]))
        Z2.append(row)
    Z3 = []
    for i, x in enumerate(X):
        row = np.array([])
        row = np.append(row, Z2[i])
        for i in range(n):
            for j in range(i, n):
                for k in range(j, n):
                    row = np.append(row, np.array([x[i] * x[j] * x[k]]))
        Z3.append(row)
    return Z2, Z3

# scale features
def featureScaling(X):
    X_scale = X
    means = []
    stds = []
    for i in range(len(X[0])):
        m = mean(X[:, i])
        s = std(X[:, i])
        means.append(m)
        stds.append(s)
        X_scale[:, i] = (X[:, i] - m) / s
    return X_scale, means, stds

# compute cost of each descent
def computeCost(theta, Z, y):
    m = len(y)
    y_hat = dot(Z, theta)
    J = (1.0 / (2 * m)) * np.square(np.subtract(y_hat, y))
    return J

# compute gradient descent and cost history
def gradientDescent(theta, Z, y, alpha, iter_num):
    m = len(y)
    #J_history = []
    for i in range(iter_num):
        y_hat = dot(Z, theta)
        for j in range(len(theta)):
            theta[j] -= (alpha * 1.0 / m) * np.sum(dot(np.subtract(y_hat, y), Z[:, j]))
        #J_history.append(computeCost(theta, Z, y))
    return theta#, J_history

# Gaussian kernel
def gaussianKernel(X1, X2, sigma):
    # distances between each X1 to each X2
    pairwise_distances = sp.spatial.distance.cdist(X1, X2, 'euclidean')
    K = sp.exp(- 1.0 * (pairwise_distances ** 2) / (2 * sigma ** 2))
    return K

# dual linear regression
def dualLinearRegression(X, y, sigma):
    #gram = dot(X, transpose(X))
    #alfa = dot(pinv(gram), y)
    K = gaussianKernel(X, X, sigma)
    alfa = dot(y, pinv(K))
    return alfa

# single variable
for filename in ['svar-set1.dat', 'svar-set2.dat', 'svar-set3.dat', 'svar-set4.dat', 'iris.dat']:
    avg_mse = [0] * 5
    dataSet = load_data(filename)
    if filename == 'iris.dat':
        dataSet = dataSet[:, :2]
    # plot svar
    #allX, allY = splitXy(dataSet)
    #plt.scatter(allX, allY, lw=2)
    #plt.show()
    for trainSet, testSet in tenFold(dataSet):
        trainX, trainY = splitXy(trainSet)
        testX, testY = splitXy(testSet)

        # my linear regression
        trainZ = getZLinear(trainX)
        testZ = getZLinear(testX)
        theta = regression(trainZ, trainY)
        train_mse = computeError(theta, trainZ, trainY)
        test_mse = computeError(theta, testZ, testY)
        #plotLinearModel(testX, testY, trainX, trainZ, theta)
        # python linear regression
        clf = linear_model.LinearRegression()
        clf.fit(trainX, trainY)
        py_train_mse = mean_squared_error(trainY, clf.predict(trainX))
        py_test_mse = mean_squared_error(testY, clf.predict(testX))
        # compare
        print(formPrintout('My training MSE: ', train_mse, 'Python training MSE: ', py_train_mse))
        print(formPrintout('My testing MSE: ', test_mse, 'Python testing MSE: ', py_test_mse))
        avg_mse[0] += test_mse / 10

        # my polynomial regression for 2 - 5 degrees
        trainZ2, trainZ3, trainZ4, trainZ5 = getZPolynomial(trainX)
        testZ2, testZ3, testZ4, testZ5 = getZPolynomial(testX)
        theta2 = regression(trainZ2, trainY)
        theta3 = regression(trainZ3, trainY)
        theta4 = regression(trainZ4, trainY)
        theta5 = regression(trainZ5, trainY)
        train_mse2 = computeError(theta2, trainZ2, trainY)
        train_mse3 = computeError(theta3, trainZ3, trainY)
        train_mse4 = computeError(theta4, trainZ4, trainY)
        train_mse5 = computeError(theta5, trainZ5, trainY)
        test_mse2 = computeError(theta2, testZ2, testY)
        test_mse3 = computeError(theta3, testZ3, testY)
        test_mse4 = computeError(theta4, testZ4, testY)
        test_mse5 = computeError(theta5, testZ5, testY)
        # python polynomial regression for 2 - 5 degrees
        clf2 = linear_model.LinearRegression()
        clf2.fit(trainZ2[:, 1:], trainY)
        py_train_mse2 = mean_squared_error(trainY, clf2.predict(trainZ2[:, 1:]))
        py_test_mse2 = mean_squared_error(testY, clf2.predict(testZ2[:, 1:]))
        clf3 = linear_model.LinearRegression()
        clf3.fit(trainZ3[:, 1:], trainY)
        py_train_mse3 = mean_squared_error(trainY, clf3.predict(trainZ3[:, 1:]))
        py_test_mse3 = mean_squared_error(testY, clf3.predict(testZ3[:, 1:]))
        clf4 = linear_model.LinearRegression()
        clf4.fit(trainZ4[:, 1:], trainY)
        py_train_mse4 = mean_squared_error(trainY, clf4.predict(trainZ4[:, 1:]))
        py_test_mse4 = mean_squared_error(testY, clf4.predict(testZ4[:, 1:]))
        clf5 = linear_model.LinearRegression()
        clf5.fit(trainZ5[:, 1:], trainY)
        py_train_mse5 = mean_squared_error(trainY, clf5.predict(trainZ5[:, 1:]))
        py_test_mse5 = mean_squared_error(testY, clf5.predict(testZ5[:, 1:]))
        # compare
        print(formPrintout('My training MSE for Poly2: ', train_mse2, 'Python training MSE for Poly2: ', py_train_mse2))
        print(formPrintout('My testing MSE for Poly2: ', test_mse2, 'Python testing MSE for Poly2: ', py_test_mse2))
        print(formPrintout('My training MSE for Poly3: ', train_mse3, 'Python training MSE for Poly3: ', py_train_mse3))
        print(formPrintout('My testing MSE for Poly3: ', test_mse3, 'Python testing MSE for Poly3: ', py_test_mse3))
        print(formPrintout('My training MSE for Poly4: ', train_mse4, 'Python training MSE for Poly4: ', py_train_mse4))
        print(formPrintout('My testing MSE for Poly4: ', test_mse4, 'Python testing MSE for Poly4: ', py_test_mse4))
        print(formPrintout('My training MSE for Poly5: ', train_mse5, 'Python training MSE for Poly5: ', py_train_mse5))
        print(formPrintout('My testing MSE for Poly5: ', test_mse5, 'Python testing MSE for Poly5: ', py_test_mse5))
        avg_mse[1] += test_mse2 / 10
        avg_mse[2] += test_mse3 / 10
        avg_mse[3] += test_mse4 / 10
        avg_mse[4] += test_mse5 / 10

        # reduce training data amount
        reducedTrainX, reducedTrainY = splitXy(reduceTrainingData(trainSet))
        reducedTrainZ = getZLinear(reducedTrainX)
        reducedTheta = regression(reducedTrainZ, reducedTrainY)
        reducedTrain_mse = computeError(reducedTheta, reducedTrainZ, reducedTrainY)
        reducedTest_mse = computeError(reducedTheta, testZ, testY)
        reducedTrainZ2, reducedTrainZ3, reducedTrainZ4, reducedTrainZ5 = getZPolynomial(reducedTrainX)
        reducedTheta2 = regression(reducedTrainZ2, reducedTrainY)
        reducedTheta3 = regression(reducedTrainZ3, reducedTrainY)
        reducedTheta4 = regression(reducedTrainZ4, reducedTrainY)
        reducedTheta5 = regression(reducedTrainZ5, reducedTrainY)
        reducedTrain_mse2 = computeError(reducedTheta2, reducedTrainZ2, reducedTrainY)
        reducedTrain_mse3 = computeError(reducedTheta3, reducedTrainZ3, reducedTrainY)
        reducedTrain_mse4 = computeError(reducedTheta4, reducedTrainZ4, reducedTrainY)
        reducedTrain_mse5 = computeError(reducedTheta5, reducedTrainZ5, reducedTrainY)
        reducedTest_mse2 = computeError(reducedTheta2, testZ2, testY)
        reducedTest_mse3 = computeError(reducedTheta3, testZ3, testY)
        reducedTest_mse4 = computeError(reducedTheta4, testZ4, testY)
        reducedTest_mse5 = computeError(reducedTheta5, testZ5, testY)
        print(formPrintout('My training MSE: ', train_mse, 'Reduced training MSE: ', reducedTrain_mse))
        print(formPrintout('My testing MSE: ', test_mse, 'Reduced testing MSE: ', reducedTest_mse))
        print(formPrintout('My training MSE for Poly2: ', train_mse2, 'Reduced training MSE for Poly2: ', reducedTrain_mse2))
        print(formPrintout('My testing MSE for Poly2: ', test_mse2, 'Reduced testing MSE for Poly2: ', reducedTest_mse2))
        print(formPrintout('My training MSE for Poly3: ', train_mse3, 'Reduced training MSE for Poly3: ', reducedTrain_mse3))
        print(formPrintout('My testing MSE for Poly3: ', test_mse3, 'Reduced testing MSE for Poly3: ', reducedTest_mse3))
        print(formPrintout('My training MSE for Poly4: ', train_mse4, 'Reduced training MSE for Poly4: ', reducedTrain_mse4))
        print(formPrintout('My testing MSE for Poly4: ', test_mse4, 'Reduced testing MSE for Poly4: ', reducedTest_mse4))
        print(formPrintout('My training MSE for Poly5: ', train_mse5, 'Reduced training MSE for Poly5: ', reducedTrain_mse5))
        print(formPrintout('My testing MSE for Poly5: ', test_mse5, 'Reduced testing MSE for Poly5: ', reducedTest_mse5))

    print(avg_mse)
    minMse = min(avg_mse)
    for i, e in enumerate(avg_mse):
        if e == minMse:
            print('The ' + str(i + 1) + 'th degree is the minimum.\n')


# multiple variables
for filename in ['mvar-set1.dat', 'mvar-set2.dat', 'mvar-set3.dat', 'mvar-set4.dat']:
    avg_mse = [0, 0]
    avg_train_mse = [0, 0]
    for trainSet, testSet in tenFold(load_data(filename)):
        trainX, trainY = splitXy(trainSet)
        testX, testY = splitXy(testSet)

        # linear regression in higher dimensional space
        startPrimal = datetime.datetime.now()
        trainZ2, trainZ3 = mapZ(trainX)
        testZ2, testZ3 = mapZ(testX)
        theta2 = regression(trainZ2, trainY)
        theta3 = regression(trainZ3, trainY)
        endPrimal = datetime.datetime.now()
        train_mse2 = computeError(theta2, trainZ2, trainY)
        train_mse3 = computeError(theta3, trainZ3, trainY)
        test_mse2 = computeError(theta2, testZ2, testY)
        test_mse3 = computeError(theta3, testZ3, testY)
        print(formPrintout('2nd degree MSE: ', test_mse2, '3rd degree MSE: ', test_mse3))
        avg_mse[0] += test_mse2 / 10
        avg_mse[1] += test_mse3 / 10
        avg_train_mse[0] += train_mse2 / 10
        avg_train_mse[1] += train_mse3 / 10

        trainZ = getZLinear(trainX)
        testZ = getZLinear(testX)
        # explicit solution
        expTheta = regression(trainZ, trainY)
        exp_test_mse = computeError(expTheta, testZ, testY)
        # iterative solution with gradient descent
        # initialize theta to be 1s, learning rate to be 0.001, and iteration times to be 1000
        iterTheta = gradientDescent(ones(expTheta.size), trainZ, trainY, 0.001, 1000)
        iter_test_mse = computeError(iterTheta, testZ, testY)
        print(formPrintout('Explicit MSE: ', exp_test_mse, 'Iterative MSE: ', iter_test_mse))
        # dual linear regression, using sigma = 0.5
        startDual = datetime.datetime.now()
        sigma = 0.5
        K = gaussianKernel(testX, trainX, sigma)
        alfa = dualLinearRegression(trainX, trainY, sigma)
        endDual = datetime.datetime.now()
        dual_test_mse = computeError(alfa, K, testY)
        print(formPrintout('Dual time: ', endDual - startDual, '2nd and 3rd degree time: ', endPrimal - startPrimal))
        print(formPrintout('Dual MSE: ', dual_test_mse, '2nd degree MSE: ', test_mse2))

    print(avg_mse)
    minMse = min(avg_mse)
    for i, e in enumerate(avg_mse):
        if e == minMse:
            print('The ' + str(i + 1) + 'th degree is the minimum.')
            print(formPrintout('The train MSE is ', avg_train_mse[i], 'The test MSE is ', e))