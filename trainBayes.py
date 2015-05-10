import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import numpy as np
from random import shuffle
import csv

import time
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, GaussianNB
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

 
bin_n = 16

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
    avgImg = np.zeros((256,256,3), np.float32)
    for img in imgs:
        cv2.accumulate(img, avgImg)
    N = len(imgs)
    cv2.multiply(avgImg, 1.0/float(N), avgImg)
    return avgImg

def removeMeanImg(img, avgImg):
    res = np.subtract(img, avgImg)
    res = np.absolute(res)
    return cv2.cv.fromarray(res)

print 'Loading training and testing features...'
trainFeatures, trainLabels, testFeatures, testLabels = loadFeatures(FILEPREFIX, FILEPOSTFIX, 'trigrams')

print 'Feature Length:', len(trainFeatures[0])

mean, eig = cv2.PCACompute(np.array(trainFeatures), maxComponents = 500)
#f = open('meanEigFile.txt', 'w')
#f.write(str(mean.tolist()) + '\n')
#f.write(str(eig.tolist()) + '\n')
#f.close()

projTrainFeat = cv2.PCAProject(np.array(trainFeatures), np.array(mean), np.array(eig))

######     Now training     #########################

print 'Training G Bayes model...'
clf = GaussianNB()

clf.fit(projTrainFeat, trainLabels)
#print sum(trainLblList)

#print 'Loading test images...'
#test_cells, testLblList = loadImgs(test_img_list)
#print sum(testLblList)

#print 'Computing test features...'
#testFeatures = computeFeatures(test_cells)

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
