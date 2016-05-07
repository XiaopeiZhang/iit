__author__ = 'Xiaopei'

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.io as sio
import pandas as pd
from pylab import *
from random import shuffle
from sklearn.metrics import confusion_matrix
from numpy import linalg
import cvxopt
import cvxopt.solvers
from sklearn import svm

# get both X, y
def load_data(filename):
    arr = np.loadtxt(filename, delimiter=',')
    return arr

# get both X, y from .mat file
def load_mat(filename):
    mat = sio.loadmat(filename)
    arr = ones(shape=(len(mat['X']), len(mat['X'][0]) + 1))
    arr[:, :-1] = mat['X']
    arr[:, -1:] = mat['y']
    return arr

# plot linear model on data
def plot2D(arr):
    plt.scatter(arr[:,0], arr[:,1], c=arr[:,-1], cmap=plt.cm.Paired)
    plt.show()

# 10 fold
def tenFold(data):
    arr = np.copy(data)
    shuffle(arr)
    for k in range(10):
        train = [x for i, x in enumerate(arr) if i % 10 != k]
        test = [x for i, x in enumerate(arr) if i % 10 == k]
        yield train, test

# split X, y
def splitXy(arr):
    X, y = [], []
    for i in arr:
        X.append(i[:-1])
        y.append(i[-1])
    return np.array(X), np.array(y)

# get all the labels
def getLabels(arr):
    label_set = set([])
    for row in arr:
        label_set.add(row[-1])
    labels = sorted(list(label_set))
    return labels

# get all X and y if y belongs to specific classes
def getDataByClasses(arr, labels_desired):
    desired_arr = []
    for i, e in enumerate(arr):
        if e[-1] in labels_desired:
            desired_arr.append(arr[i])
    return np.array(desired_arr)

# change label1 to 1 and all the others to -1
def preparation(data, label1):
    prep_data = []
    for row in data:
        if row[-1] == label1:
            temp = np.array(row)
            temp[-1] = 1 * 1.0
            prep_data.append(np.array(temp))
        else:
            temp = np.array(row)
            temp[-1] = -1 * 1.0
            prep_data.append(np.array(temp))
    return np.array(prep_data)

# convert a list to a list of lists
def convert(l):
    res = []
    for e in l:
        res.append(np.array([e]))
    return np.array(res)

# compute gram matrix
def gram(x1, x2):
    return np.dot(x1, x2)

# compute polynomial
def polynomial(x1, x2, degree=3):
    return (1 + np.dot(x1, x2)) ** degree

# compute gaussian
def gaussian(x1, x2, sigma=5.0):
    return np.exp(-linalg.norm(x1 - x2) ** 2 / (2 * (sigma ** 2)))

# compute kernel
def getKernel(X, kernel):
    m = len(X)
    K = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            K[i, j] = kernel(X[i], X[j])
    return K

# train data with SVM
def my_svm(X, y, kernel=gram, C=None):
    m, n = X.shape
    K = getKernel(X, kernel)

    P = cvxopt.matrix(np.outer(y, y) * K)
    q = cvxopt.matrix(np.ones(m) * -1)
    A = cvxopt.matrix(y, (1, m))
    b = cvxopt.matrix(0.0)

    # hard margin
    if C == None:
        G = cvxopt.matrix(np.diag(np.ones(m) * -1))
        h = cvxopt.matrix(np.zeros(m))
    # soft margin
    else:
        G = cvxopt.matrix(np.vstack((np.diag(np.ones(m) * -1), np.identity(m))))
        h = cvxopt.matrix(np.hstack((np.zeros(m), np.ones(m) * C)))
    sol = cvxopt.solvers.qp(P, q, G, h, A, b)
    # get lagrange multipliers
    alpha = np.ravel(sol['x'])
    # get support vectors
    sv = alpha > 1e-5
    sv0 = np.arange(len(alpha))[sv]
    sv_alpha = alpha[sv]
    sv_x = X[sv]
    sv_y = y[sv]

    # get weights
    if kernel == gram:
        w = np.zeros(n)
        for i in range(len(sv_alpha)):
            w += sv_alpha[i] * sv_y[i] * sv_x[i]
    else:
        w = None
    # get intercept
    w0 = 0
    for i in range(len(sv_alpha)):
        w0 += sv_y[i] / len(sv_alpha)
        w0 -= np.sum(sv_alpha * sv_y * K[sv0[i], sv]) / len(sv_alpha)
    #w0 /= len(sv_alpha)
    return w, w0, sv_alpha, sv_x, sv_y

def nonlinearDecisionBoundary(X, sv_alpha, sv_x, sv_y, kernel):
    y_hat = np.zeros(len(X))
    for i in range(len(X)):
        t = 0
        for a, y, x in zip(sv_alpha, sv_y, sv_x):
            t += a * y * kernel(X[i], x)
        y_hat[i] = t
    return y_hat

# predict for SVM
def predict(X, w, w0, sv_alpha, sv_x, sv_y, kernel=gram):
    if w is None:
        y_hat = nonlinearDecisionBoundary(X, sv_alpha, sv_x, sv_y, kernel) + w0
    else:
        y_hat = np.dot(X, w) + w0
    return np.sign(y_hat)

# plot linear svm
def plotLinearSVM(trainX, trainY, w, w0, sv_x, sv_y, bound=True):
    slope = - w[0] / w[1]
    xx = np.linspace(min(trainX[:,0]), max(trainX[:,0]), num=100)
    yy = slope * xx - w0 / w[1]
    margin = 1 / np.sqrt(np.sum(w ** 2))
    plt.plot(xx, yy, 'k-')
    if bound:
        yy_down = yy + slope * margin
        yy_up = yy - slope * margin
        plt.plot(xx, yy_down, 'k--')
        plt.plot(xx, yy_up, 'k--')
    plt.scatter(trainX[:,0], trainX[:,1], c=trainY, cmap=plt.cm.Paired)
    plt.scatter(sv_x[:,0], sv_x[:,1], c=sv_y, marker='*', cmap=plt.cm.Paired)
    plt.show()

# plot nonlinear contour
def plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, kernel):

    # create a mesh to plot in
    x_min, x_max = trainX[:, 0].min() - 1, trainX[:, 0].max() + 1
    y_min, y_max = trainX[:, 1].min() - 1, trainX[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.2), np.arange(y_min, y_max, 0.2))
    Z = predict(np.c_[xx.ravel(), yy.ravel()], w, w0, sv_alpha, sv_x, sv_y, kernel)
    Z = Z.reshape(xx.shape)
    plt.contour(xx, yy, Z, levels=[0], cmap='Greys_r')

    plt.scatter(trainX[:,0], trainX[:,1], c=trainY, cmap=plt.cm.Paired)
    plt.scatter(sv_x[:,0], sv_x[:,1], c=sv_y, marker='*', cmap=plt.cm.Paired)
    plt.show()

arr = load_data('iris_reorganized.data')
labels = getLabels(arr)
separable = getDataByClasses(arr, labels[:2])
separable = preparation(separable, labels[0])
non_separable = getDataByClasses(arr, labels[1:])
non_separable = preparation(non_separable, labels[1])
#plot2D(separable)
#plot2D(non_separable)

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY)
    plotLinearSVM(trainX, trainY, w, w0, sv_x, sv_y)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y)
    # python linear svm
    clf = svm.SVC(C=10000.0, kernel='linear')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My linear SVM with hard margin:')
print(confusion_matrix(all_y, all_my_y))
print('Python linear SVM with hard margin:')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(non_separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY)
    plotLinearSVM(trainX, trainY, w, w0, sv_x, sv_y, bound=False)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y)
    # python linear svm
    clf = svm.SVC(C=10000.0, kernel='linear')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My linear SVM with hard margin:')
print(confusion_matrix(all_y, all_my_y))
print('Python linear SVM with hard margin:')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, C=1.0)
    plotLinearSVM(trainX, trainY, w, w0, sv_x, sv_y)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y)
    # python linear svm
    clf = svm.SVC(C=1.0, kernel='linear')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My linear SVM with soft margin (separable):')
print(confusion_matrix(all_y, all_my_y))
print('Python linear SVM with soft margin (separable):')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(non_separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, C=1.0)
    plotLinearSVM(trainX, trainY, w, w0, sv_x, sv_y, bound=False)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y)
    # python linear svm
    clf = svm.SVC(C=1.0, kernel='linear')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My linear SVM with soft margin (non-separable):')
print(confusion_matrix(all_y, all_my_y))
print('Python linear SVM with soft margin (non-separable):')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, kernel=polynomial, C=1.0)
    plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, polynomial)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y, kernel=polynomial)
    # python linear svm
    clf = svm.SVC(C=1.0, kernel='poly')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My polynomial SVM (separable):')
print(confusion_matrix(all_y, all_my_y))
print('Python polynomial SVM (separable):')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(non_separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, kernel=polynomial, C=1.0)
    plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, polynomial)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y, kernel=polynomial)
    # python linear svm
    clf = svm.SVC(C=1.0, kernel='poly')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My polynomial SVM (non-separable):')
print(confusion_matrix(all_y, all_my_y))
print('Python polynomial SVM (non-separable):')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, kernel=gaussian, C=1.0)
    plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, gaussian)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y, kernel=gaussian)
    # python svm
    clf = svm.SVC(C=1.0)
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My Gaussian SVM (separable):')
print(confusion_matrix(all_y, all_my_y))
print('Python Radial SVM (separable):')
print(confusion_matrix(all_y, all_python_y))

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(non_separable):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, kernel=gaussian, C=1.0)
    plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, gaussian)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y, kernel=gaussian)
    # python svm
    clf = svm.SVC(C=1.0)
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My Gaussian SVM (non-separable):')
print(confusion_matrix(all_y, all_my_y))
print('Python radial SVM (non-separable):')
print(confusion_matrix(all_y, all_python_y))


arr1 = load_mat('ex6data1.mat')
labels1 = getLabels(arr1)
ext1 = preparation(arr1, labels1[1])
#plot2D(ext1)

arr3 = load_mat('ex6data3.mat')
labels3 = getLabels(arr3)
ext3 = preparation(arr3, labels3[1])
#plot2D(ext3)


for ext in [ext1, ext3]:
    print("##########################################################################################")

    all_y, all_my_y, all_python_y = [], [], []
    for trainSet, testSet in tenFold(ext):
        trainX, trainY = splitXy(trainSet)
        testX, testY = splitXy(testSet)
        trainX = trainX[:, :2]
        testX = testX[:, :2]
        w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, kernel=polynomial, C=1.0)
        plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, polynomial)
        y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y, kernel=polynomial)
        # python linear svm
        clf = svm.SVC(C=1.0, kernel='poly')
        clf.fit(trainX, trainY)
        python_y_hat = clf.predict(testX)

        all_y = np.concatenate([all_y, testY])
        all_my_y = np.concatenate([all_my_y, y_hat])
        all_python_y = np.concatenate([all_python_y, python_y_hat])
    print('My polynomial SVM (ext):')
    print(confusion_matrix(all_y, all_my_y))
    print('Python polynomial SVM (ext):')
    print(confusion_matrix(all_y, all_python_y))

    print("##########################################################################################")

    all_y, all_my_y, all_python_y = [], [], []
    for trainSet, testSet in tenFold(ext):
        trainX, trainY = splitXy(trainSet)
        testX, testY = splitXy(testSet)
        trainX = trainX[:, :2]
        testX = testX[:, :2]
        w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, kernel=gaussian, C=1.0)
        plotNonlinearSVM(trainX, trainY, w, w0, sv_alpha, sv_x, sv_y, gaussian)
        y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y, kernel=gaussian)
        # python svm
        clf = svm.SVC(C=1.0)
        clf.fit(trainX, trainY)
        python_y_hat = clf.predict(testX)

        all_y = np.concatenate([all_y, testY])
        all_my_y = np.concatenate([all_my_y, y_hat])
        all_python_y = np.concatenate([all_python_y, python_y_hat])
    print('My Gaussian SVM (ext):')
    print(confusion_matrix(all_y, all_my_y))
    print('Python Radial SVM (ext):')
    print(confusion_matrix(all_y, all_python_y))


# unbalance classes: 50 examples for class 1 and 15 examples for class -1
separable_unbalanced = separable[:65, :]

print("##########################################################################################")

all_y, all_my_y, all_python_y = [], [], []
for trainSet, testSet in tenFold(separable_unbalanced):
    trainX, trainY = splitXy(trainSet)
    testX, testY = splitXy(testSet)
    trainX = trainX[:, :2]
    testX = testX[:, :2]
    w, w0, sv_alpha, sv_x, sv_y = my_svm(trainX, trainY, C=1.0)
    plotLinearSVM(trainX, trainY, w, w0, sv_x, sv_y)
    y_hat = predict(testX, w, w0, sv_alpha, sv_x, sv_y)
    # python linear svm
    clf = svm.SVC(C=1.0, kernel='linear')
    clf.fit(trainX, trainY)
    python_y_hat = clf.predict(testX)

    all_y = np.concatenate([all_y, testY])
    all_my_y = np.concatenate([all_my_y, y_hat])
    all_python_y = np.concatenate([all_python_y, python_y_hat])
print('My linear SVM with soft margin (separable_unbalanced):')
print(confusion_matrix(all_y, all_my_y))
print('Python linear SVM with soft margin (separable_unbalanced):')
print(confusion_matrix(all_y, all_python_y))