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
        line = line.replace("'",'')
        line = line.lower()
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
    if len(nGramCnts) > 0:
        sortedCnts, sortedNGrams = (list(t) for t in zip(*sorted(zip(nGramCnts, nGramList))))
        sortedCnts.reverse()
        sortedNGrams.reverse()
    else:
        sortedNGrams = []
        sortedCnts = []

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
    if sortedNGrams != []:
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
                score = row[-1]
                origFilename = folder + 'text/' + row[0] + '.txt'
                origFNames.append(origFilename)
                scores.append(score)
                #fname = folder + 'scoredText/' + row[0] + '_' + score + '.txt'
                #shutil.copyfile(origFilename, fname)
            cnt += 1
    return origFNames, scores

def combineMyPersonalityData(scoreRange, dataset):
    fBase = 'mypersonality/NGrams/' + dataset + '_'

    for gramType in ['unigrams', 'bigrams', 'trigrams']:
        print 'Computing', gramType, 'for score range', scoreRange

        ngrams = []
        cnts = []

        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = fsplit[-1][:-4]
                if '-' not in score:
                    if dataset == 'mypersonality_depressed':
                        score = int(score)
                        scoreRange[0] = int(scoreRange[0])
                        scoreRange[1] = int(scoreRange[1])
                    elif dataset == 'mypersonality_neurotic':
                        score = float(score)
                        scoreRange[0] = float(scoreRange[0])
                        scoreRange[1] = float(scoreRange[1])

                    if score >= scoreRange[0] and score <= scoreRange[1]:
                        print 'Saving NGrams for', fname, '...'
                        f = open('mypersonality/NGrams/' + fname, 'r')
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

                        outname = fBase + gramType + '_' + str(scoreRange[0]) + '-' + str(scoreRange[1]) + '.txt'
                        fout = open(outname, 'w')
                        sortedCnts, sortedGrams = (list(t) for t in zip(*sorted(zip(cnts, ngrams))))
                        sortedCnts.reverse() 
                        sortedGrams.reverse()
                        for a,b in zip(sortedGrams, sortedCnts):
                            fout.write(a + ' ' + str(b) + '\n')
                        fout.close()


def combineRedditData(dataset):
    gramTypes = ['unigrams', 'bigrams', 'trigrams']

    for gramType in gramTypes:
        print dataset, gramType
        ngrams = []
        cnts = []
        fout = open('reddit/NGrams/' + dataset + '_' + gramType + '_all.txt', 'w')
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
                #print 'Saving NGrams for', fname, '...'
                f = open('reddit/NGrams/' + fname, 'r')
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
        sortedCnts, sortedNGrams = (list(t) for t in zip(*sorted(zip(cnts, ngrams))))
        sortedCnts.reverse()
        sortedNGrams.reverse()
        for c, n in zip(sortedCnts, sortedNGrams):
            fout.write(n + ' ' + str(c) + '\n')
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

def runNGrams(flag, gramType):
    if gramType == 'unigrams':
        val = 1
    elif gramType == 'bigrams':
        val = 2
    elif gramType == 'trigrams':
        val = 3
    else:
        print 'Bad gram type...'
        sys.exit()

    if flag == 'mypersonality_depressed':
        if not os.path.exists('mypersonality/NGrams'):
            print 'Creating directory mypersonality/NGrams...'
            os.makedirs('mypersonality/NGrams')

        onlyfiles, scores = separateMyPersonalityData('project_materials/mypersonality_depression/', '939_userScores.csv')

        print 'Computing MyPersonality Depression NGrams...'
        cnt = 0
        for s in list(set(scores)):
            cnt += 1
            dataFiles = []
            print 'SCORE:', s,  'Progress:', cnt, '/', len(list(set(scores)))
            indices = [i for i, x in enumerate(scores) if x == str(s)]
            for i in indices:
                dataFiles.append(onlyfiles[i])
            if dataFiles != []:
                saveMyPersonalityNGrams(val, dataFiles, 'mypersonality/NGrams/mypersonality_depressed_' + gramType + '_' + str(s) + '.txt')

    elif flag == 'mypersonality_neurotic':
        if not os.path.exists('mypersonality/NGrams'):
            print 'Creating directory mypersonality/NGrams...'
            os.makedirs('mypersonality/NGrams')

        onlyfiles, scores = separateMyPersonalityData('project_materials/mypersonality_neuroticism/', 'userDictionary.csv')

        print 'Computing MyPersonality Neuroticism NGrams...'
        cnt = 0
        for s in list(set(scores)):
            cnt += 1
            dataFiles = []
            print 'SCORE:', s,  'Progress:', cnt, '/', len(list(set(scores)))
            indices = [i for i, x in enumerate(scores) if x == str(s)]
            for i in indices:
                dataFiles.append(onlyfiles[i])
            if dataFiles != []:
                saveMyPersonalityNGrams(val, dataFiles, 'mypersonality/NGrams/mypersonality_neurotic_' + gramType + '_' + str(s) + '.txt')


    elif flag == 'reddit_depressed':
        dirname = 'reddit/NGrams/'
        if not os.path.exists(dirname):
            print 'Creating directory ' + dirname + '...'
            os.makedirs(dirname)
        print 'Computing Reddit NGrams...'
        for f in os.listdir("reddit/depressed/"):
            if f.endswith(".txt"):
                print 'Saving NGrams for', f, '...'
                saveRedditNGrams(val, 'reddit/depressed/' + f, dirname + 'reddit_depressed_' + f[:-4] + '_' + gramType + '.txt')

    elif flag == 'reddit_nondepressed':
        dirname = 'reddit/NGrams/'
        if not os.path.exists(dirname):
            print 'Creating directory ' + dirname + '...'
            os.makedirs(dirname)

        print 'Computing Reddit NGrams ChangeMyView...'
        for f in os.listdir("reddit/nondepressed/changemyview/"):
            if f.endswith(".txt"):
                print 'Saving NGrams for', f, '...'
                saveRedditNGrams(val, 'reddit/nondepressed/changemyview/' + f, dirname + 'reddit_nondepressed_changemyview_' + f[:-4] + '_' + gramType + '.txt')


        print 'Computing Reddit NGrams CasualConversation...'
        for f in os.listdir("reddit/nondepressed/casualconversation/"):
            if f.endswith(".txt"):
                print 'Saving NGrams for', f, '...'
                saveRedditNGrams(val, 'reddit/nondepressed/casualconversation/' + f, dirname + 'reddit_nondepressed_casualconversation_' + f[:-4] + '_' + gramType + '.txt')


        print 'Computing Reddit NGrams Confession...'
        for f in os.listdir("reddit/nondepressed/confession/"):
            if f.endswith(".txt"):
                print 'Saving NGrams for', f, '...'
                saveRedditNGrams(val, 'reddit/nondepressed/confession/' + f, dirname + 'reddit_nondepressed_confession_' + f[:-4] + '_' + gramType + '.txt')

        print 'Computing Reddit NGrams Self...'
        for f in os.listdir("reddit/nondepressed/self/"):
            if f.endswith(".txt"):
                print 'Saving NGrams for', f, '...'
                saveRedditNGrams(val, 'reddit/nondepressed/self/' + f, dirname + 'reddit_nondepressed_self_' + f[:-4] + '_' + gramType + '.txt')

    else:
        print 'Unrecognized dataset option...'
        sys.exit()

def printUsage():
    print '*****USAGE*****'
    print 'python findNGrams.py <option> <args>'
    print 'option ngrams: args= <dataset> <gramType>'
    print 'option combine: args= <dataset> <min> <max>'
    print 'option compare: args= <dist1file> <dist2file> <threshval>'

args = sys.argv
if len(args) > 2:
    if args[1] == 'ngrams':
        if len(args) == 4:
            runNGrams(args[2], args[3])
        else:
            printUsage()
    elif args[1] == 'combine':
        if len(args) == 5:
            if 'mypersonality' in args[2]:
                combineMyPersonalityData([args[3], args[4]], args[2])
            print 'Done.'
        elif len(args) == 3:
            if 'reddit' in args[2]:
                combineRedditData(args[2])
            print 'Done.'
        else:
            printUsage()
    elif args[1] == 'compare':
        if len(args) == 5:
            div = compareDistrs(args[2], args[3], float(args[4]))
            print div
        else:
            printUsage()
    else:
        printUsage()
else:
    printUsage()

