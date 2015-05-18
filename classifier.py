import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
import numpy as np
from random import shuffle
import csv
import pickle
import os

import time
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, GaussianNB
from sklearn import svm
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

def loadSplitInfo(splitfile, dataset, subsets, trainNums, testNum):
    d = pickle.load(open(splitfile))
    trainlist = []
    trainlabel = []
    testlist = []
    testlabel = []
    for sub in subsets:
        if sub == 'depressed':
            label = 1
        else:
            label = 0
        for t in trainNums:
            trainlist += d[dataset][sub][t]
            trainlabel += [label]*len(d[dataset][sub][t])
        testlist += d[dataset][sub][testNum]
        testlabel += [label]*len(d[dataset][sub][testNum])
    return trainlist, trainlabel, testlist, testlabel


MYPRENGRAMS = 'mypersonality/NGrams/Distrs/'
POST = '_distr.txt'
REDPRENGRAMS = 'reddit/NGrams/Distrs/'
MYPRE = 'cache/emmypersonality/'
REDPRE = 'cache/emreddit/'

#dataset = mypersonality_depression
def loadFeatures(subsets, file_prefix, file_postfix, featTypes, IDs):
    feats = []
    for item in IDs:
        if 'grams' in featTypes:
            for dataset in subsets:
                filename = file_prefix + dataset + '_' + item + '_' + featType + file_postfix
                if os.path.exists(filename):
                    feat = loadSingleFeature(filename)
                    break
        else:
            feat = []
            for featType in featTypes:
                for dataset in subsets:
                    if '_' in dataset:
                        dset = dataset.split('_')
                        dset = dset[1]
                    if 'reddit' in dataset:
                        filename = 'cache/emreddit/' + dset + '/' + item + '_' + featType + '.txt'
                    else:
                        filename = 'cache/emmypersonality/depressed' + '/' + item + '_' + featType + '.txt'
                    #print filename
                #print filename
                    if os.path.exists(filename):
                        f = loadSingleFeature(filename)
                        #print f
                        feat += f
                        break
                    #else:
                    #    feat = feats[-1][:]
            if feat == []:
                feat = feats[-1][:]
        #print feat
            #time.sleep(1000)
        feats.append(feat)
    return feats

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

#USAGE
#python trainSVM.py dataset featType trainset testset classifier subsetgroups
args = sys.argv
dataset = args[1]
featTypes = args[2]
featTypes = featTypes.split(',')
featTypes[0] = featTypes[0][1:]
featTypes[-1] = featTypes[-1][:-1]
TRAINSET = args[3]
TRAINSET = TRAINSET[1:-1]
TRAINSET = TRAINSET.split(',')
TRAINSET = [int(x) for x in TRAINSET]
TESTSET = int(args[4])
classifier = args[5]
subsets = []
groups = []

if 'mypersonality' in dataset:
    subsets.append('mypersonality_depressed')
for i in range(6, len(args)):
    if 'reddit' in dataset:
        subsets.append(dataset + '_' + args[i])
    groups.append(args[i])

#TRAINSET=[0,1,3,4]
#TESTSET=2
print 'Loading training and testing files...'
train_IDs, trainLabels, test_IDs, testLabels = loadSplitInfo('cache/cross_valid_lists.pkl', dataset, groups, TRAINSET, TESTSET)
if 'reddit' in dataset:
    FILEPREFIX = REDPRE
else:
    FILEPREFIX = MYPRE
print 'Computing train features...'
trainFeatures = loadFeatures(subsets, FILEPREFIX, POST, featTypes, train_IDs)
print 'Computing test features...'
testFeatures = loadFeatures(subsets, FILEPREFIX, POST, featTypes, test_IDs)

print 'Feature Length:', len(trainFeatures[0])
if len(trainFeatures[0]) > 500:
    MAX = 500
    print 'Finding PCA Projection...'
    mean, eig = cv2.PCACompute(np.array(trainFeatures), maxComponents = MAX)
    projTrainFeat = cv2.PCAProject(np.array(trainFeatures), np.array(mean), np.array(eig))
    trainFeatures = projTrainFeat

    projTestFeat = cv2.PCAProject(np.array(testFeatures), np.array(mean), np.array(eig))
    testFeatures = projTestFeat

print 'Training SVM model...'

if classifier == 'svm':
    clf = svm.SVC(C=100000000.0, gamma=0.1, kernel='rbf', cache_size=1000)
elif classifier == 'bayes':
    clf = GaussianNB()
else:
    print "Unknown classifier", classifier, "..."
    sys.exit()

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

clf.fit(trainFeatures, trainLabels)

result = clf.predict(testFeatures)
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
