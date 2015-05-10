import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import numpy as np
import csv
from random import shuffle

import time
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from scipy import ndimage as nd
from skimage.util import img_as_float
from skimage.filter import gabor_kernel


def separateMyPersonalityData(folder, scoreFile):
    dep_keys = []
    nondep_keys = []
    with open(folder + scoreFile, 'rU') as csvfile:
        f = csv.reader(csvfile)
        cnt = 0
        for row in f:
            if cnt > 0:
                if int(row[-1]) <= 24:
                    nondep_keys.append(row[0])
                elif int(row[-1]) >= 31:
                    dep_keys.append(row[0])
            cnt += 1
    return dep_keys, nondep_keys


FILEPREFIX = 'mypersonality/NGrams/Distrs/mypersonality_depressed_'
FILEPOSTFIX = '_distr.txt'

def loadFeatures(file_prefix, file_postfix, gramType):
    dep_IDs, nondep_IDs = separateMyPersonalityData('project_materials/mypersonality_depression/', '939_userScores.csv')
    numDepTrain = int(len(dep_IDs)*0.8)
    numNonDepTrain = int(len(nondep_IDs)*0.8)
    numDepTest = len(dep_IDs)-numDepTrain
    numNonDepTest = len(nondep_IDs) - numNonDepTrain
    shuffle(dep_IDs)
    shuffle(nondep_IDs)
    trainDep = dep_IDs[0:numDepTrain]
    testDep = dep_IDs[numDepTrain:]
    trainNonDep = nondep_IDs[0:numNonDepTrain]
    testNonDep = nondep_IDs[numNonDepTrain:]
    trainFileSet = trainDep + trainNonDep
    trainLabels = [1]*numDepTrain + [0]*numNonDepTrain
    testFileSet = testDep + testNonDep
    testLabels = [1]*numDepTest + [0]*numNonDepTest
    trainFeats = []
    for item in trainFileSet:
        filename = file_prefix + item + '_' + gramType + file_postfix
        feat = loadSingleFeature(filename)
        trainFeats.append(feat)
    testFeats = []
    for item in testFileSet:
        filename = file_prefix + item + '_' + gramType + file_postfix
        feat = loadSingleFeature(filename)
        testFeats.append(feat)
    return trainFeats, trainLabels, testFeats, testLabels

    
def loadSingleFeature(filename):
    feat = []
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        feat.append(float(line))
    f.close()
    return feat

def computeMeanImg(imgs):
    avgBImg = np.zeros((256,256), np.float32)
    avgGImg = np.zeros((256,256), np.float32)
    avgRImg = np.zeros((256,256), np.float32)
    for img in imgs:
        np.add(img[:,:,0], avgBImg, avgBImg)
        np.add(img[:,:,1], avgGImg, avgGImg)
        np.add(img[:,:,2], avgRImg, avgRImg)
        tempImg = img
    N = len(imgs)
    np.divide(avgBImg, float(N), avgBImg)
    np.divide(avgGImg, float(N), avgGImg)
    np.divide(avgRImg, float(N), avgRImg)
    tempImg[:,:,0] = avgBImg
    tempImg[:,:,1] = avgGImg
    tempImg[:,:,2] = avgRImg
    #print tempImg.shape
    #cv2.imshow('avgimg', tempImg)
    #cv2.waitKey(0)
    return tempImg

def removeMeanImg(img, avgImg):
    res = np.subtract(img, avgImg)
    return res

#print 'Loading train images...'
#train_cells, trainLblList = loadImgs(train_img_list, 'train')
#train_mean = computeMeanImg(train_cells)

#print 'Computing train features...'
#trainFeatures = computeFeatures(train_cells, train_mean)

print 'Loading training and testing features...'
trainFeatures, trainLabels, testFeatures, testLabels = loadFeatures(FILEPREFIX, FILEPOSTFIX, 'trigrams')

print 'Feature Length:', len(trainFeatures[0])

mean, eig = cv2.PCACompute(np.array(trainFeatures), maxComponents = 500)
#f = open('meanEigFile.txt', 'w')
#f.write(str(mean.tolist()) + '\n')
#f.write(str(eig.tolist()) + '\n')
#f.close()

print 'Finding PCA Projection...'
projTrainFeat = cv2.PCAProject(np.array(trainFeatures), np.array(mean), np.array(eig))

######     Now training     #########################

print 'Training SVM model...'
#clf = svm.SVC(kernel='rbf', C=10000.0, gamma=0.01)#C=1000000.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0.001, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)
#clf = SGDClassifier(loss="log", penalty="l2",shuffle=True)
clf = svm.SVC(C=100000000.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
  gamma=0.10000000000000001, kernel='rbf', max_iter=-1, probability=False,
  random_state=None, shrinking=True, tol=0.001, verbose=False)

#C_range = 10.0 ** np.arange(1, 9)
#gamma_range = 10.0 ** np.arange(-8, 0)
#param_grid = dict(gamma=gamma_range, C=C_range)
#cv = StratifiedKFold(y=trainLabels, n_folds=3)
#grid = GridSearchCV(clf, param_grid=param_grid, cv=cv)
#grid.fit(projTrainFeat, trainLabels)

#print("The best classifier is: ", grid.best_estimator_)
#a = raw_input('Quit? ')
#if a == 'q':
#    sys.exit()#time.sleep()

clf.fit(projTrainFeat, trainLabels)
#print sum(trainLblList)

#print 'Loading test images...'
#test_cells, testLblList = loadImgs(test_img_list, 'test')
#print sum(testLblList)

#print 'Computing test features...'
#testFeatures = computeFeatures(test_cells, train_mean)

projTestFeat = cv2.PCAProject(np.array(testFeatures), np.array(mean), np.array(eig))

result = clf.predict(projTestFeat)
responses = testLabels

tot = 0
truePos = sum(responses)
trueNeg = len(responses)-truePos
numPos = 0
numNeg = 0
for gt, pred in zip(responses, result):
    #print gt, pred
    tot += abs(gt-pred)
    if pred == 1 and gt == 1:
        numPos += 1
    if pred == 0 and gt == 0:
        numNeg += 1

print "NumPos:", sum(result)
print "TruePos:", 100*float(numPos)/truePos
print "TrueNeg:", 100*float(numNeg)/trueNeg
print "Accuracy:", 100*(len(responses)-float(tot))/len(responses)
