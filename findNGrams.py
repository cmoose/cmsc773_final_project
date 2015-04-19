import time
import math
import nltk
import re
import sys
from os import listdir
import os
from os.path import isfile, join
import csv


#load stopwords.
def loadStopwords():
    stopwords = []
    f = open('stopwords.txt', 'r')
    for line in f:
        line = line.strip()
        stopwords.append(line)
    f.close()
    return stopwords

def loadData(filename):
    data = []
    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        line = re.sub(r'[^\x00-\x7F]+',' ', line)
        text = nltk.word_tokenize(line)
        data.append(text)
    f.close()
    return data

def findNGrams(stopwords, data, n):
    print 'Finding ' + str(n) +  '-Grams...'
    nGramList = []
    nGramCnts = []
    for i in range(0, len(data)):
        words = data[i]
        for j in range(0, len(words)):
            ngram = ''
            currWord = words[j]
            if n == 1:
                if currWord not in stopwords:
                    ngram = currWord
                    #nGramList.append(currWord)
            elif n == 2:
                if j > 0:
                    prevWord = words[j-1]
                    if ((prevWord not in stopwords) and (currWord not in stopwords)):
                        ngram = prevWord+ '+' +currWord
                        #nGramList.append(prevWord+ '+' +currWord)
            elif n == 3:
                if j > 0 and j < len(words)-1:
                    prevWord = words[j-1]
                    nextWord = words[j+1]
                    if (prevWord not in stopwords) and (currWord not in stopwords) and (nextWord not in stopwords):
                        ngram = prevWord+ '+' +currWord + '+' + nextWord
                        #nGramList.append(prevWord+ '+' +currWord + '+' + nextWord)
            else:
                print "We do not support NGrams of size", n
                sys.exit()
  
            if ngram != '':
                if ngram not in nGramList:
                    nGramList.append(ngram)
                    nGramCnts.append(1)
                else:
                    ind = nGramList.index(ngram)
                    nGramCnts[ind] += 1

    return nGramList, nGramCnts

def freqNGrams(nGramCnts, nGramList):
    sortedCnts, sortedNGrams = (list(t) for t in zip(*sorted(zip(nGramCnts, nGramList))))
    sortedCnts.reverse()
    sortedNGrams.reverse()

    return sortedNGrams, sortedCnts

def klDiv(p,q):
    res = []
    for i in range(0,len(p)):
        res.append(math.log(p[i]/q[i], 2)*p[i])
    return sum(res)

def removeLowCounts(p, pCnts, thresh):
    newP = []
    newCnts = []
    for a,b in zip(p, pCnts):
        if b > thresh:
            newP.append(a)
            newCnts.append(b)
    return newP, newCnts

def combineTwoDistrs(pBigrams, pCnts, qBigrams, qCnts):
    bigrams = pBigrams + list(set(qBigrams) - set(pBigrams))
    p = []
    q = []
    for item in bigrams:
        if item in pBigrams:
            ind = pBigrams.index(item)
            p.append(pCnts[ind]+1) #add 1 smoothing
        else:
            p.append(1)
        if item in qBigrams:
            ind = qBigrams.index(item)
            q.append(qCnts[ind]+1)
        else:
            q.append(1)
    pTot = sum(p)
    qTot = sum(q)
    for i in range(0, len(bigrams)):
        p[i] /= float(pTot)
        q[i] /= float(qTot)
    return p, q

def saveNGrams(nGramList, nGramCnts, filename):
    fout = open(filename, 'w')
    for a,b in zip(nGramList, nGramCnts):
        fout.write(a + ' ' + str(b) + '\n')
    fout.close()

def saveRedditNGrams(n, dataFile, outputFile):
    stopwords = loadStopwords()
    data = loadData(dataFile)
    nGramList, nGramCnts = findNGrams(stopwords, data, n)
    sortedNGrams, sortedCnts = freqNGrams(nGramCnts, nGramList)
    saveNGrams(sortedNGrams, sortedCnts, outputFile)

def saveMyPersonalityNGrams(n, dataFiles, outputFile):
    stopwords = loadStopwords()
    data = []
    for dataFile in dataFiles:
        data += loadData(dataFile)
    nGramList, nGramCnts = findNGrams(stopwords, data, n)
    sortedNGrams, sortedCnts = freqNGrams(nGramCnts, nGramList)
    saveNGrams(sortedNGrams, sortedCnts, outputFile)

def separateMyPersonalityData(folder, scoreFile):
    origFNames = []
    scores = []
    with open(folder + scoreFile, 'rU') as csvfile:
        f = csv.reader(csvfile)
        cnt = 0
        for row in f:
            if cnt > 0:
                score = row[2]
                origFilename = folder + 'text/' + row[0] + '.txt'
                origFNames.append(origFilename)
                scores.append(score)
                #fname = folder + 'scoredText/' + row[0] + '_' + score + '.txt'
                #shutil.copyfile(origFilename, fname)
            cnt += 1
    return origFNames, scores

def combineMyPersonalityData(scoreRange):
    fBase = 'NGrams/mypersonality_'

    for gramType in ['unigrams', 'bigrams', 'trigrams']:
        print 'Computing', gramType, 'for score range', scoreRange

        ngrams = []
        cnts = []

        f = open(fBase + gramType + '_' + str(scoreRange[0]) + '.txt', 'r')
        for line in f:
            line = line.strip()
            line = line.split()
            ngrams.append(line[0])
            cnts.append(int(line[1]))
        f.close()

        for score in range(scoreRange[0] + 1, scoreRange[1] + 1):
            if os.path.isfile(fBase + gramType + '_' + str(score) + '.txt'):
                f = open(fBase + gramType + '_' + str(score) + '.txt', 'r')
                for line in f:
                    line = line.strip()
                    line = line.split()
                    if line[0] in ngrams:
                        ind = ngrams.index(line[0])
                        cnts[ind] += int(line[1])
                    else:
                        ngrams.append(line[0])
                        cnts.append(int(line[1]))
                f.close()

        fout = open(fBase + gramType + '_' + str(scoreRange[0]) + '-' + str(scoreRange[1]) + '.txt', 'w')
        sortedCnts, sortedGrams = (list(t) for t in zip(*sorted(zip(cnts, ngrams))))
        sortedCnts.reverse() 
        sortedGrams.reverse()
        for a,b in zip(sortedGrams, sortedCnts):
            fout.write(a + ' ' + str(b) + '\n')
        fout.close()


def loadNGramFile(filename):
    f = open(filename, 'r')
    ngrams = []
    cnts = []
    for line in f:
        line = line.strip()
        line = line.split()
        ngrams.append(line[0])
        cnts.append(int(line[1]))
    f.close()
    return ngrams, cnts


def compareDistrs(gramFile1, gramFile2, removeVal):
    ngrams1, cnts1 = loadNGramFile(gramFile1)
    ngrams2, cnts2 = loadNGramFile(gramFile2)

    pNew, pCnts = removeLowCounts(ngrams1, cnts1, removeVal)
    qNew, qCnts = removeLowCounts(ngrams2, cnts2, removeVal)

    p, q = combineTwoDistrs(pNew, pCnts, qNew, qCnts)

    pqDiv = klDiv(p,q)
    qpDiv = klDiv(q,p)
    res = (pqDiv + qpDiv)/2.0
    return res


if not os.path.exists('NGrams'):
    print 'Creating directory NGrams...'
    os.makedirs('NGrams')

print 'Computing Reddit NGrams...'
saveRedditNGrams(1, 'project_materials/reddit/depressed.txt', 'NGrams/reddit_depressed_unigrams.txt')
saveRedditNGrams(2, 'project_materials/reddit/depressed.txt', 'NGrams/reddit_depressed_bigrams.txt')
saveRedditNGrams(3, 'project_materials/reddit/depressed.txt', 'NGrams/reddit_depressed_trigrams.txt')

onlyfiles, scores = separateMyPersonalityData('project_materials/mypersonality_depression/', '939_userScores.csv')

print 'Computing MyPersonality Depression NGrams...'
for s in range(1, 61):
    dataFiles = []
    print 'SCORE:', s
    indices = [i for i, x in enumerate(scores) if x == str(s)]
    for i in indices:
        dataFiles.append(onlyfiles[i])
    if dataFiles != []:
        saveMyPersonalityNGrams(1, dataFiles, 'NGrams/mypersonality_unigrams_' + str(s) + '.txt')
        saveMyPersonalityNGrams(2, dataFiles, 'NGrams/mypersonality_bigrams_' + str(s) + '.txt')
        saveMyPersonalityNGrams(3, dataFiles, 'NGrams/mypersonality_trigrams_' + str(s) + '.txt')


combineMyPersonalityData([10, 15])
combineMyPersonalityData([44, 48])

div = compareDistrs('NGrams/mypersonality_unigrams_10-15.txt', 'NGrams/mypersonality_unigrams_44-48.txt', 2)
print div

