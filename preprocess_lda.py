#process data for topic modeling
import sys
import os
import string
import time

def loadNGramFile(filename):
    ngrams = []
    cnts = []

    f = open(filename, 'r')
    for line in f:
        line = line.strip()
        line = line.split()
        ngrams.append(line[0])
        cnts.append(int(line[1]))
    f.close()
    return ngrams, cnts

def writeVocab(vocab, fname):
    fout = open(fname, 'w')
    for v in vocab:
        fout.write(v + '\n')
    fout.close()

def computeVocab(fnames, thresh):
    vocab = []
    for fname in fnames:
        grams, cnts = loadNGramFile(fname)
        newgrams = [i for (i,j) in zip(grams,cnts) if j > thresh]
        vocab = list(set(vocab + newgrams))
    myset = set(vocab)
    vocab = list(myset)
    return vocab

def computeFeature(fname, vocab):
    grams, cnts = loadNGramFile(fname)
    res = [0]*len(vocab)
    cnt = 0
    for g in grams:
        if g in vocab:
            ind = vocab.index(g)
            res[ind] = cnts[cnt]
        cnt += 1
    return res

def writeFeature(feat, fname):
    fout = open(fname, 'w')
    for item in feat:
        fout.write(str(item) + '\n')
    fout.close()


def runPreprocess(gramType):
    
    dataset = 'mypersonality_depressed'
    print 'Preprocessing lda for', dataset, 'CESD<=15...'
    SCORERANGE = [0,15]
    vocabfnames = ['mypersonality/NGrams/' + dataset + '_' + gramType + '_0-15.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_0-15.txt')
    
    for fname in os.listdir("mypersonality/NGrams/"):
        if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
            fsplit = fname.split('_')
            score = fsplit[-1][:-4]
            if '-' not in score and 'feats' not in score:
                score = int(score)
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    feats = computeFeature(fullfname, vocab)
                    outname = fullfname[:-4] + '_feats_0-15.txt'
                    print fullfname, outname
                    writeFeature(feats, outname)

    #time.sleep(1000)
    print 'Preprocessing lda for', dataset, 'CESD>=44...'
    SCORERANGE = [44,60]
    vocabfnames = ['mypersonality/NGrams/' + dataset + '_' + gramType + '_44-60.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_44-60.txt')
    
    for fname in os.listdir("mypersonality/NGrams/"):
        if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
            fsplit = fname.split('_')
            score = fsplit[-1][:-4]
            if '-' not in score and 'feats' not in score:
                score = int(score)
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    feats = computeFeature(fullfname, vocab)
                    outname = fullfname[:-4] + '_feats_-44-60.txt'
                    print fullfname, outname
                    writeFeature(feats, outname)


    print 'Preprocessing lda for', dataset, 'CESD<=24...'
    SCORERANGE = [0,24]
    vocabfnames = ['mypersonality/NGrams/' + dataset + '_' + gramType + '_0-24.txt']
    vocab = computeVocab(vocabfnames, 10)
    writeVocab(vocab, 'mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_0-24.txt')
    
    for fname in os.listdir("mypersonality/NGrams/"):
        if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
            fsplit = fname.split('_')
            score = fsplit[-1][:-4]
            if '-' not in score and 'feats' not in score:
                score = int(score)
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    feats = computeFeature(fullfname, vocab)
                    outname = fullfname[:-4] + '_feats_0-24.txt'
                    print fullfname, outname
                    writeFeature(feats, outname)

    print 'Preprocessing lda for', dataset, 'CESD>=31...'
    SCORERANGE = [31,60]
    vocabfnames = ['mypersonality/NGrams/' + dataset + '_' + gramType + '_31-60.txt']
    vocab = computeVocab(vocabfnames, 10)
    writeVocab(vocab, 'mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_31-60.txt')
    
    for fname in os.listdir("mypersonality/NGrams/"):
        if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
            fsplit = fname.split('_')
            score = fsplit[-1][:-4]
            if '-' not in score and 'feats' not in score:
                score = int(score)
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    feats = computeFeature(fullfname, vocab)
                    outname = fullfname[:-4] + '_feats_31-60.txt'
                    print fullfname, outname
                    writeFeature(feats, outname)

    dataset = 'mypersonality_neurotic'
    print 'Preprocessing lda for', dataset, 'score<=2.25...'
    SCORERANGE = [0.0, 2.25]
    vocabfnames = ['mypersonality/NGrams/' + dataset + '_' + gramType + '_0.0-2.25.txt']
    vocab = computeVocab(vocabfnames, 10)
    writeVocab(vocab, 'mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_0.0-2.25.txt')
    
    for fname in os.listdir("mypersonality/NGrams/"):
        if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
            fsplit = fname.split('_')
            score = fsplit[-1][:-4]
            if '-' not in score and 'feats' not in score:
                score = float(score)
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    feats = computeFeature(fullfname, vocab)
                    outname = fullfname[:-4] + '_feats_0.0-2.25.txt'
                    print fullfname, outname
                    writeFeature(feats, outname)

    print 'Preprocessing lda for', dataset, 'score>=3.05...'
    SCORERANGE = [3.05,5.0]
    vocabfnames = ['mypersonality/NGrams/' + dataset + '_' + gramType + '_3.05-5.0.txt']
    vocab = computeVocab(vocabfnames, 10)
    writeVocab(vocab, 'mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_3.05-5.0.txt')
    
    for fname in os.listdir("mypersonality/NGrams/"):
        if fname.endswith(".txt") and fname.startswith(dataset + '_' + gramType):
            fsplit = fname.split('_')
            score = fsplit[-1][:-4]
            if '-' not in score and 'feats' not in score:
                score = float(score)
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    feats = computeFeature(fullfname, vocab)
                    outname = fullfname[:-4] + '_feats_0.0-3.05.txt'
                    print fullfname, outname
                    writeFeature(feats, outname)

    dataset = 'reddit_depressed'
    print 'Preprocessing lda for', dataset, '...'
    vocabfnames = ['reddit/NGrams/' + dataset + '_' + gramType + '_all.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
    
    for fname in os.listdir("reddit/NGrams/"):
        if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
            fullfname = "reddit/NGrams/" + fname
            feats = computeFeature(fullfname, vocab)
            outname = fullfname[:-4] + '_feats.txt'
            print fullfname, outname
            writeFeature(feats, outname)
            fsplit = fname.split('_')
    
    dataset = 'reddit_nondepressed'
    print 'Preprocessing lda for', dataset, '...'
    vocabfnames = ['reddit/NGrams/' + dataset + '_' + gramType + '_all.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
    
    for fname in os.listdir("reddit/NGrams/"):
        if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
            fullfname = "reddit/NGrams/" + fname
            print fullfname
            feats = computeFeature(fullfname, vocab)
            outname = fullfname[:-4] + '_feats_full.txt'
            print fullfname, outname
            writeFeature(feats, outname)
            fsplit = fname.split('_')

    dataset = 'reddit_nondepressed_changemyview'
    print 'Preprocessing lda for', dataset, '...'
    #SCORERANGE = [3.05,5.0]
    vocabfnames = ['reddit/NGrams/' + dataset + '_' + gramType + '_all.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
    
    for fname in os.listdir("reddit/NGrams/"):
        if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
            fullfname = "reddit/NGrams/" + fname
            feats = computeFeature(fullfname, vocab)
            outname = fullfname[:-4] + '_feats.txt'
            print fullfname, outname
            writeFeature(feats, outname)
            fsplit = fname.split('_')

    dataset = 'reddit_nondepressed_casualconversation'
    print 'Preprocessing lda for', dataset, '...'
    #SCORERANGE = [3.05,5.0]
    vocabfnames = ['reddit/NGrams/' + dataset + '_' + gramType + '_all.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
    
    for fname in os.listdir("reddit/NGrams/"):
        if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
            fullfname = "reddit/NGrams/" + fname
            feats = computeFeature(fullfname, vocab)
            outname = fullfname[:-4] + '_feats.txt'
            print fullfname, outname
            writeFeature(feats, outname)
            fsplit = fname.split('_')

    dataset = 'reddit_nondepressed_confession'
    print 'Preprocessing lda for', dataset, '...'
    #SCORERANGE = [3.05,5.0]
    vocabfnames = ['reddit/NGrams/' + dataset + '_' + gramType + '_all.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
    
    for fname in os.listdir("reddit/NGrams/"):
        if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
            fullfname = "reddit/NGrams/" + fname
            feats = computeFeature(fullfname, vocab)
            outname = fullfname[:-4] + '_feats.txt'
            print fullfname, outname
            writeFeature(feats, outname)
            fsplit = fname.split('_')

    dataset = 'reddit_nondepressed_self'
    print 'Preprocessing lda for', dataset, '...'
    #SCORERANGE = [3.05,5.0]
    vocabfnames = ['reddit/NGrams/' + dataset + '_' + gramType + '_all.txt']
    vocab = computeVocab(vocabfnames, 1)
    writeVocab(vocab, 'reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
    
    for fname in os.listdir("reddit/NGrams/"):
        if fname.endswith(gramType + ".txt") and fname.startswith(dataset):
            fullfname = "reddit/NGrams/" + fname
            feats = computeFeature(fullfname, vocab)
            outname = fullfname[:-4] + '_feats.txt'
            print fullfname, outname
            writeFeature(feats, outname)
            fsplit = fname.split('_')


args = sys.argv
if len(args) == 2:
    runPreprocess(args[1])
else:
    print '*****USAGE*****'
    print 'python preprocess_lda.py <gramType>'

