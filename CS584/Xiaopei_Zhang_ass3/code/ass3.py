__author__ = 'Xiaopei'

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.io as sio
import pandas as pd
from pylab import *
from random import shuffle
from sklearn.metrics import confusion_matrix
from sklearn import linear_model
from sknn.mlp import Classifier, Layer

# get both X, y
def load_data(filename):
    arr = np.loadtxt(filename, delimiter=',')
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
    return np.array(X), np.array(y)

# get all the labels
def getLabels(arr):
    label_set = set([])
    for row in arr:
        label_set.add(row[-1])
    labels = sorted(list(label_set))
    return labels

# change label1 to 1 and all the others to 0
def preparation(data, label1):
    prep_data = []
    for row in data:
        if row[-1] == label1:
            temp = np.array(row)
            temp[-1] = 1 * 1.0
            prep_data.append(np.array(temp))
        else:
            temp = np.array(row)
            temp[-1] = 0 * 1.0
            prep_data.append(np.array(temp))
    return np.array(prep_data)

# get Z by adding 1s to X
def getZ(X):
    Z = ones(shape=(len(X), len(X[0]) + 1))
    Z[:, 1:] = X
    return Z

# get Z for non-linear case: eg, 1, x1, x2, x3, x4, ..., x4*x1, x4*x2, x4*x3, x4*x4
def getZNonlinear(X):
    n = len(X[0])
    Z2 = ones(shape=(len(X), n ** 2 + n + 1))
    Z2[:, 1:n + 1] = X
    for x in Z2:
        cnt = n + 1
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                x[cnt] = x[i] * x[j]
                cnt += 1
    return Z2

# Sigmoid function
def sigmoid(theta, Z):
    y_hat = dot(Z, theta)
    g = 1.0 / (1.0 + exp(-y_hat))
    return g

# Softmax function
def softmax(theta, Z):
    y_hat = dot(Z, theta)
    return np.exp(y_hat) / np.sum(np.exp(y_hat))

# compute cost of each descent
def computeCost(theta, Z, y):
    m = len(y)
    y_hat = sigmoid(dot(Z, theta))
    J = (1.0 / (2 * m)) * np.square(np.subtract(y_hat, y))
    return J

# compute logistic regression theta using gradient descent
def gradientDescent(theta, Z, y, alpha, iter_num):
    m = len(y)
    #J_history = []
    for i in range(iter_num):
        y_hat = sigmoid(theta, Z)
        for j in range(len(theta)):
            theta[j] -= (alpha * 1.0) * np.sum(dot(np.subtract(y_hat, y), Z[:, j]))
        #J_history.append(computeCost(theta, Z, y))
    return theta#, J_history

# logistic regression class prediction with label1 1 and label2 0
def logisticPredictY(theta, Z):
    y_hat = sigmoid(theta, Z)
    y_class = []
    for e in y_hat:
        if e > 0.5:
            y_class.append(1 * 1.0)
        else:
            y_class.append(0 * 1.0)
    return np.array(y_class)

# logistic regression class one vs all the others: get the highest probability
def logisticPredictYMultiple(label_prob):
    result = label_prob.keys()[0]
    for l in label_prob:
        if label_prob[result] < label_prob[l]:
            result = l
    return result

# get all X and y from .mat if y belongs to specific classes
def getDataByClasses(X, y, labels_desired):
    desired_X, desired_y = [], []
    for i,e in enumerate(y):
        if e[0] in labels_desired:
            desired_X.append(X[i])
            desired_y.append(e)
    return np.array(desired_X), np.array(desired_y)

# get the derivative of sigmoid
def sigmoidDerivative(x):
    return x * (1 - x)

# convert a list to a list of lists
def convert(l):
    res = []
    for e in l:
        res.append(np.array([e]))
    return np.array(res)

# neural network for 3 classes with gradient descent
def neuralNetwork3Classes(trainX, trainY, hidden_dimension, epsilon):
    trainZ = getZ(trainX)
    m, n = len(trainY), len(trainZ[0])
    # randomly initialize weights with mean 0
    np.random.seed(1)
    syn0 = 2 * np.random.random((n, hidden_dimension)) - 1
    syn1 = 2 * np.random.random((hidden_dimension, 1)) - 1
    formerError = None
    count = 100
    former_syn0 = syn0
    while count > 0:
        l0 = trainZ
        l1 = sigmoid(syn0, l0)
        l2 = softmax(syn1, l1)
        error = np.sum(np.square(np.abs(trainY - l2))) * 0.5
        l2_delta = (trainY - l2) * sigmoidDerivative(l2)
        l1_delta = (l2_delta.dot(syn1.T)) * sigmoidDerivative(l1)
        syn1 += l1.T.dot(l2_delta) * epsilon
        # add momentum, set beta to 0.1
        cur_syn0 = syn0
        syn0 += l0.T.dot(l1_delta) * epsilon + 0.1 * (cur_syn0 - former_syn0)
        former_syn0 = cur_syn0
        if error != formerError:
            formerError = error
        else:
            break
        count -= 1
    return syn0, syn1

# neural network 3-class probability calculation
def neuralPredictY3(testX, syn0, syn1):
    y_hat = softmax(syn1, sigmoid(syn0, getZ(testX)))
    return y_hat

# neural network 3-class classifier
def neuralClassifier(p1, p2, p3):
    y_hat = []
    for i in range(len(p1)):
        max_p = max(p1[i][0], p2[i][0], p3[i][0])
        if max_p == p1[i][0]:
            y_hat.append(np.array([1.0]))
        elif max_p == p2[i][0]:
            y_hat.append(np.array([2.0]))
        else:
            y_hat.append(np.array([3.0]))
    return np.array(y_hat)

all_testY, all_y_hat, all_python_y_hat, all_y_hat_non, all_python_y_hat_non = [], [], [], [], []
for trainSet, testSet in tenFold(load_data("iris_reorganized_2class.data")):
    labels = getLabels(trainSet)
    prep_trainSet = preparation(trainSet, labels[0])
    trainX, trainY = splitXy(prep_trainSet)
    prep_testSet = preparation(testSet, labels[0])
    testX, testY = splitXy(prep_testSet)
    all_testY = np.concatenate([all_testY, testY])

    # linear case
    trainZ = getZ(trainX)
    # initialize theta to be 1s, learning rate to be 0.001, and iteration times to be 1000
    theta = gradientDescent(ones(len(trainZ[0])), trainZ, trainY, 0.001, 1000)
    testZ = getZ(testX)
    y_hat = logisticPredictY(theta, testZ)
    all_y_hat = np.concatenate([all_y_hat, y_hat])
    clf = linear_model.LogisticRegression()
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)
    all_python_y_hat = np.concatenate([all_python_y_hat, python_y_hat])

    # non-linear case
    trainZNon = getZNonlinear(trainX)
    # initialize theta to be 1s, learning rate to be 0.001, and iteration times to be 1000
    thetaNon = gradientDescent(ones(len(trainZNon[0])), trainZNon, trainY, 0.001, 1000)
    testZNon = getZNonlinear(testX)
    y_hat_non = logisticPredictY(thetaNon, testZNon)
    all_y_hat_non = np.concatenate([all_y_hat_non, y_hat_non])
    clf_non = linear_model.LogisticRegression()
    clf_non.fit(trainZNon[:,1:], trainY)
    python_y_hat_non = clf_non.predict(testZNon[:,1:])
    all_python_y_hat_non = np.concatenate([all_python_y_hat_non, python_y_hat_non])
print("My logistic regression:")
print(confusion_matrix(all_testY, all_y_hat))
print("Python logistic regression:")
print(confusion_matrix(all_testY, all_python_y_hat))
print("My logistic regression nonlinear:")
print(confusion_matrix(all_testY, all_y_hat_non))
print("Python logistic regression nonlinear:")
print(confusion_matrix(all_testY, all_python_y_hat_non))

print("##########################################################################################")

all_testY1, all_y_hat1, all_python_y_hat1 = [], [], []
for trainSet, testSet in tenFold(load_data("iris_reorganized.data")):
    labels = getLabels(trainSet)
    label_theta = {}
    # train one vs one
    for l in labels:
        prep_trainSet = preparation(trainSet, l)
        trainX, trainY = splitXy(prep_trainSet)
        trainZ = getZNonlinear(trainX)
        # initialize theta to be 1s, learning rate to be 0.001, and iteration times to be 1000
        theta = gradientDescent(ones(len(trainZ[0])), trainZ, trainY, 0.001, 1000)
        label_theta[l] = theta
    testX, testY = splitXy(testSet)
    all_testY1 = np.concatenate([all_testY1, testY])
    testZ = getZNonlinear(testX)
    #print label_theta
    for r, row in enumerate(testZ):
        label_prob = {}
        for l in labels:
            y_prob = sigmoid(label_theta[l], row)
            label_prob[l] = y_prob
        y_hat = logisticPredictYMultiple(label_prob)
        all_y_hat1.append(y_hat)
        #print "true",testY[r]
        #print "pred",label_prob
    clf = linear_model.LogisticRegression()
    X, y = splitXy(trainSet)
    clf.fit(getZNonlinear(X), y)
    python_y_hat = clf.predict(testZ)
    all_python_y_hat1 = np.concatenate([all_python_y_hat1, python_y_hat])
print("My k-class logistic regression nonlinear:")
print(confusion_matrix(all_testY1, all_y_hat1))
print("Python k-class logistic regression nonlinear:")
print(confusion_matrix(all_testY1, all_python_y_hat1))



print("##########################################################################################")

mat = sio.loadmat("ex4data1.mat")
y_set = set([])
for e in mat['y']:
    y_set.add(e[0])
y_classes = sorted(list(y_set))

X2, y2 = getDataByClasses(mat['X'], mat['y'], y_classes[:3])
arr2 = ones(shape=(len(X2), len(X2[0]) + 1))
arr2[:, :-1] = X2
arr2[:, -1:] = y2
for trainSet, testSet in tenFold(arr2):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainY = convert(trainY)
    testY = convert(testY)
    trainY1 = preparation(trainY, y_classes[0])
    trainY2 = preparation(trainY, y_classes[1])
    trainY3 = preparation(trainY, y_classes[2])
    syn0_1, syn1_1 = neuralNetwork3Classes(trainX, trainY1, 20, 0.2)
    syn0_2, syn1_2 = neuralNetwork3Classes(trainX, trainY2, 20, 0.2)
    syn0_3, syn1_3 = neuralNetwork3Classes(trainX, trainY3, 20, 0.2)
    y_hat1 = neuralPredictY3(testX, syn0_1, syn1_1)
    y_hat2 = neuralPredictY3(testX, syn0_2, syn1_2)
    y_hat3 = neuralPredictY3(testX, syn0_3, syn1_3)
    y_hat = neuralClassifier(y_hat1, y_hat2, y_hat3)
    print("My 3-class neural network:")
    print(confusion_matrix(testY, y_hat))
    # Python neural network
    nn = Classifier(
    layers=[
        Layer("Sigmoid", units=20),
        Layer("Softmax")],
    learning_rate=0.2,
    n_iter=10)
    nn.fit(trainX, trainY)
    python_y_hat = nn.predict(testX)
    print("Python 3-class neural network:")
    print(confusion_matrix(testY, python_y_hat))