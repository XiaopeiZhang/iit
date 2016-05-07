__author__ = 'Xiaopei'

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
from pylab import *
from random import shuffle
from sklearn.lda import LDA
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm, datasets
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

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

# compute alpha, mean array, and std array for each label
def getParameters(arr):
    label_set = set([])
    for row in arr:
        label_set.add(row[-1])
    labels = sorted(list(label_set))
    label_alpha, label_mean, label_std = {}, {}, {}
    for l in labels:
        examples_in_l = []
        for row in arr:
            if row[-1] == l:
                examples_in_l.append(row[:-1])
        examples_in_l = np.array(examples_in_l)
        label_alpha[l] = 1.0 * len(examples_in_l) / len(arr)
        mean = np.mean(examples_in_l, axis=0)
        label_mean[l] = mean
        std = zeros(shape=(len(mean), len(mean)))
        for row in examples_in_l:
            sub = np.subtract(row, mean)
            sub = np.array([sub])
            cur = np.dot(transpose(sub), sub)
            std = np.add(std, cur)
        label_std[l] = 1.0 * std / len(examples_in_l)
    return labels, label_alpha, label_mean, label_std

# predict label, discriminant function which choose the highest probability
# for each pair of membership functions, d(x) = g1(x) - g2(x)
# if d(x) > 0, x belongs to label 1; otherwise, x belongs to label 2
def predictLabel(X, label_alpha, label_mean, label_std):
    P = {}
    for l in label_alpha:
        p = gda(X, label_mean[l], label_std[l], label_alpha[l])
        P[l] = p
    result = label_alpha.keys()[0]
    for x in P:
        if P[result] < P[x]:
            result = x
    return result

# gaussian discriminative analysis
def gda(X, mean, std, alpha):
    sub = np.subtract(X, mean)
    p = - 0.5 * log(det(std)) - dot(dot(transpose(sub), pinv(std)), sub) * 0.5 + log(alpha)
    return p

# compute confusion matrix
def confusionMatrix(y_hat, y, confusion_matrix, label_num):
    confusion_matrix[label_num[y_hat], label_num[y]] += 1

# compute precision and recall from matrix
def getPR(confusion_matrix, label_num):
    cii = confusion_matrix[label_num, label_num]
    row, col = 0, 0
    for i in range(len(confusion_matrix)):
        row += confusion_matrix[label_num, i]
        col += confusion_matrix[i, label_num]
    return 1.0 * cii / row, 1.0 * cii / col

# compute F-measure
def getF(precision, recall):
    return 2 * precision * recall / (precision + recall)

# compute accuracy from matrix
def getAccuracy(confusion_matrix):
    total, dia = 0, 0
    for i in range(len(confusion_matrix)):
        for j in range(len(confusion_matrix)):
            total += confusion_matrix[i, j]
            if i == j:
                dia += confusion_matrix[i, j]
    return 1.0 * dia / total

# plot precision recall curve
def plotCurve(arr):
    X = arr[:, :-1]
    y = arr[:, -1]
    # Binarize the output
    y = label_binarize(y, classes=[0,1])
    n_classes = y.shape[1]

    # Add noisy features
    random_state = np.random.RandomState(0)
    n_samples, n_features = X.shape

    X = np.c_[X, random_state.randn(n_samples, 150 * n_features)]

    # Split into training and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=random_state)

    # Run classifier
    classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True, random_state=random_state))
    y_score = classifier.fit(X_train, y_train).decision_function(X_test)

    # Compute Precision-Recall and plot curve
    precision = dict()
    recall = dict()
    average_precision = dict()
    for i in range(n_classes):
        precision[i], recall[i], _ = precision_recall_curve(y_test[:, i],y_score[:, i])
        average_precision[i] = average_precision_score(y_test[:, i], y_score[:, i])

    # Compute micro-average ROC curve and ROC area
    precision["micro"], recall["micro"], _ = precision_recall_curve(y_test.ravel(), y_score.ravel())
    average_precision["micro"] = average_precision_score(y_test, y_score, average="micro")

    # Plot Precision-Recall curve
    plt.clf()
    plt.plot(recall[0], precision[0], label='Precision-Recall curve')
    print(recall)
    print(precision)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.05])
    plt.title('Precision-Recall example: AUC={0:0.2f}'.format(average_precision[0]))
    plt.legend(loc="lower left")
    plt.show()

    # Plot Precision-Recall curve for each class
    plt.clf()
    plt.plot(recall["micro"], precision["micro"], label='micro-average Precision-recall curve (area = {0:0.2f})'''.format(average_precision["micro"]))
    for i in range(n_classes):
        plt.plot(recall[i], precision[i], label='Precision-recall curve of class {0} (area = {1:0.2f})'''.format(i, average_precision[i]))
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Extension of Precision-Recall curve to multi-class')
    plt.legend(loc="lower right")
    plt.show()

# naive bayes with bernoulli
def NB_Bernoulli(X, y):
    # num of examples in each label
    label_num = {}
    for l in y:
        if l in label_num:
            label_num[l] += 1
        else:
            label_num[l] = 1
    # num of feature occurrences in each label
    label_occurs = {l:zeros(shape=len(X[0])) for l in label_num}
    for i in range(len(X)):
        label = y[i]
        for j in range(len(X[i])):
            if X[i][j] != 0:
                label_occurs[label][j] += 1
    # alphas for each feature in each label
    label_alphas = {l:zeros(shape=len(X[0])) for l in label_num}
    for l in label_occurs:
        for i in range(len(label_alphas[l])):
            label_alphas[l][i] = 1.0 * label_occurs[l][i] / label_num[l]
    return label_alphas

# predict using NB_Bernoulli
def NB_Bernoulli_predict(label_alphas, x):
    label_p = {l:0.0 for l in label_alphas}
    for l in label_alphas:
        alpha = 1.0
        for i in range(len(x)):
            if x[i] == 0:
                alpha *= 1 - label_alphas[l][i]
            else:
                alpha *= label_alphas[l][i]
        label_p[l] = alpha
    result = label_p.keys()[0]
    for l in label_p:
        if label_p[result] < label_p[l]:
            result = l
    return result

# naive bayes with binomial and Laplace smoothing
def NB_Binomial(X, y):
    # num of examples in each label
    label_num = {}
    for l in y:
        if l in label_num:
            label_num[l] += 1
        else:
            label_num[l] = 1
    # num of feature occurrences in each label
    label_occurs = {l:zeros(shape=len(X[0])) for l in label_num}
    for i in range(len(X)):
        label = y[i]
        for j in range(len(X[i])):
            label_occurs[label][j] += X[i][j]
    # sum num of all feature occurrences in each label
    label_sum = {l:0 for l in label_num}
    for l in label_occurs:
        l_sum = 0
        for i in range(len(label_occurs[l])):
            l_sum += label_occurs[l][i]
        label_sum[l] = l_sum
    # alphas (occurrences of each feature / occurrences of all features) in each label
    label_alphas = {l:zeros(shape=len(X[0])) for l in label_num}
    for l in label_occurs:
        for i in range(len(label_alphas[l])):
            label_alphas[l][i] = 1.0 * (label_occurs[l][i] + 1) / (label_sum[l] + len(label_num))
    # priors in each label
    label_priors = {l:0 for l in label_num}
    for l in label_priors:
        label_priors[l] = 1.0 * label_num[l] / len(X)
    return label_alphas, label_priors

# predict using NB_Binomial
def NB_Binomial_predict(label_alphas, label_priors, x):
    label_g = {l:0.0 for l in label_priors}
    for l in label_priors:
        g = label_priors[l]
        P = int(sum(i for i in x))
        for i in range(len(x)):
            xi = int(x[i])
            combination = sp.misc.comb(P, xi)
            g *= combination * (label_alphas[l][i])**xi * (1.0 - label_alphas[l][i])**(P - xi)
        label_g[l] = g
    result = label_g.keys()[0]
    for l in label_g:
        if label_g[result] < label_g[l]:
            result = l
    return result

# 1D 2-class GDA
print("1D 2-class GDA")
confusion_matrix_1 = zeros(shape=(2, 2))
confusion_matrix_python_1 = zeros(shape=(2, 2))
label_num_1 = None
for trainSet, testSet in tenFold(load_data("perfume_data_reorganized.data")):
    train = np.array(trainSet)
    test = np.array(testSet)
    labels, label_alpha, label_mean, label_std = getParameters(train)
    label_num_1 = {l:i for i, l in enumerate(labels)}
    # sklearn LDA
    clf = LDA()
    X, y = splitXy(train)
    clf.fit(X, y)

    for t in test:
        X, y = t[:-1], t[-1]
        y_hat = predictLabel(X, label_alpha, label_mean, label_std)
        y_python = clf.predict(X)[0]
        #print("y_hat: ", y_hat, " y: ", y, " y_python: ", y_python)
        confusionMatrix(y_hat, y, confusion_matrix_1, label_num_1)
        confusionMatrix(y_python, y, confusion_matrix_python_1, label_num_1)
print("confusion matrix:")
print(confusion_matrix_1)
print("confusion matrix python:")
print(confusion_matrix_python_1)
for l in label_num_1:
    p, r = getPR(confusion_matrix_1, label_num_1[l])
    print("for class " + str(l))
    print("precision:")
    print(p)
    print("recall:")
    print(r)
    print("F-measure:")
    print(getF(p, r))
print("accuracy:")
print(getAccuracy(confusion_matrix_1))

print("##########################################################################################")
# nD 2-class GDA
print("nD 2-class GDA")
confusion_matrix_2 = zeros(shape=(2, 2))
confusion_matrix_python_2 = zeros(shape=(2, 2))
label_num_2 = None
for trainSet, testSet in tenFold(load_data("iris_reorganized_2class.data")):
    train = np.array(trainSet)[:,1:]
    test = np.array(testSet)[:,1:]
    labels, label_alpha, label_mean, label_std = getParameters(train)
    label_num_2 = {l:i for i, l in enumerate(labels)}
    # sklearn LDA
    clf = LDA()
    X, y = splitXy(train)
    clf.fit(X, y)

    for t in test:
        X, y = t[:-1], t[-1]
        y_hat = predictLabel(X, label_alpha, label_mean, label_std)
        y_python = clf.predict(X)[0]
        #print("y_hat: ", y_hat, " y: ", y, " y_python: ", y_python)
        confusionMatrix(y_hat, y, confusion_matrix_2, label_num_2)
        confusionMatrix(y_python, y, confusion_matrix_python_2, label_num_2)
print("confusion matrix:")
print(confusion_matrix_2)
print("confusion matrix python:")
print(confusion_matrix_python_2)
for l in label_num_2:
    p, r = getPR(confusion_matrix_2, label_num_2[l])
    print("for class " + str(l))
    print("precision:")
    print(p)
    print("recall:")
    print(r)
    print("F-measure:")
    print(getF(p, r))
print("accuracy:")
print(getAccuracy(confusion_matrix_2))
#plotCurve(load_data("iris_reorganized_2class.data"))

print("##########################################################################################")
# nD k-class GDA
print("nD k-class GDA")
confusion_matrix_3 = zeros(shape=(3, 3))
confusion_matrix_python_3 = zeros(shape=(3, 3))
label_num_3 = None
for trainSet, testSet in tenFold(load_data("iris_reorganized.data")):
    train = np.array(trainSet)[:,1:]
    test = np.array(testSet)[:,1:]
    labels, label_alpha, label_mean, label_std = getParameters(train)
    label_num_3 = {l:i for i, l in enumerate(labels)}
    # sklearn LDA
    clf = LDA()
    X, y = splitXy(train)
    clf.fit(X, y)

    for t in test:
        X, y = t[:-1], t[-1]
        y_hat = predictLabel(X, label_alpha, label_mean, label_std)
        y_python = clf.predict(X)[0]
        #print("y_hat: ", y_hat, " y: ", y, " y_python: ", y_python)
        confusionMatrix(y_hat, y, confusion_matrix_3, label_num_3)
        confusionMatrix(y_python, y, confusion_matrix_python_3, label_num_3)
print("confusion matrix:")
print(confusion_matrix_3)
print("confusion matrix python:")
print(confusion_matrix_python_3)
for l in label_num_3:
    p, r = getPR(confusion_matrix_3, label_num_3[l])
    print("for class " + str(l))
    print("precision:")
    print(p)
    print("recall:")
    print(r)
    print("F-measure:")
    print(getF(p, r))
print("accuracy:")
print(getAccuracy(confusion_matrix_3))

print("##########################################################################################")
# NB with Bernoulli nD 2-class
print("NB with Bernoulli nD 2-class")
confusion_matrix_4 = zeros(shape=(2, 2))
confusion_matrix_python_4 = zeros(shape=(2, 2))
label_num_4 = None
for trainSet, testSet in tenFold(load_data("spambase.data")):
    train = np.array(trainSet)
    test = np.array(testSet)
    trainX, trainy = splitXy(train)
    trainX = trainX[:,:54]
    label_alphas = NB_Bernoulli(trainX, trainy)
    labels = sorted(list(label_alphas.keys()))
    label_num_4 = {l:i for i, l in enumerate(labels)}

    # sklearn NB_Bernoulli
    clf = BernoulliNB()
    clf.fit(trainX, trainy)
    for t in test:
        X, y = t[:54], t[-1]
        y_hat = NB_Bernoulli_predict(label_alphas, X)
        y_python = clf.predict(X)[0]
        #print("y_hat: ", y_hat, " y: ", y, " y_python: ", y_python)
        confusionMatrix(y_hat, y, confusion_matrix_4, label_num_4)
        confusionMatrix(y_python, y, confusion_matrix_python_4, label_num_4)
print("confusion matrix:")
print(confusion_matrix_4)
print("confusion matrix python:")
print(confusion_matrix_python_4)
for l in label_num_4:
    p, r = getPR(confusion_matrix_4, label_num_4[l])
    print("for class " + str(l))
    print("precision:")
    print(p)
    print("recall:")
    print(r)
    print("F-measure:")
    print(getF(p, r))
print("accuracy:")
print(getAccuracy(confusion_matrix_4))

print("##########################################################################################")
# NB with Binomial features nD 2-class
print("NB with Binomial features nD 2-class")
confusion_matrix_5 = zeros(shape=(2, 2))
confusion_matrix_python_5 = zeros(shape=(2, 2))
label_num_5 = None
for trainSet, testSet in tenFold(load_data("spambase.data")):
    train = np.array(trainSet)
    test = np.array(testSet)
    trainX, trainy = splitXy(train)
    trainX = trainX[:,:54]
    label_alphas, label_priors = NB_Binomial(trainX, trainy)
    labels = sorted(list(label_alphas.keys()))
    label_num_5 = {l:i for i, l in enumerate(labels)}

    # sklearn NB_Binomial
    clf = MultinomialNB()
    clf.fit(trainX, trainy)
    for t in test:
        X, y = t[:54], t[-1]
        y_hat = NB_Binomial_predict(label_alphas, label_priors, X)
        y_python = clf.predict(X)[0]
        #print("y_hat: ", y_hat, " y: ", y, " y_python: ", y_python)
        confusionMatrix(y_hat, y, confusion_matrix_5, label_num_5)
        confusionMatrix(y_python, y, confusion_matrix_python_5, label_num_5)
print("confusion matrix:")
print(confusion_matrix_5)
print("confusion matrix python:")
print(confusion_matrix_python_5)
for l in label_num_5:
    p, r = getPR(confusion_matrix_5, label_num_5[l])
    print("for class " + str(l))
    print("precision:")
    print(p)
    print("recall:")
    print(r)
    print("F-measure:")
    print(getF(p, r))
print("accuracy:")
print(getAccuracy(confusion_matrix_5))