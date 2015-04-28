#process data for topic modeling
import sys
import os
import string

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

def computeVocab(fnames):
    vocab = []
    for fname in fnames:
       grams, cnts = loadNGramFile(fname)
       vocab += grams
    myset = set(vocab)
    vocab = list(myset)
    return vocab

def computeFeature(fname, vocab):
    grams, cnts = loadNGramFile(fname)
    res = [0]*len(vocab)
    for g in grams:
        ind = vocab.index(g)
        res[ind] = 1
    return res

def writeFeature(feat, fname):
    fout = open(fname, 'w')
    for item in feat:
        fout.write(str(item) + '\n')
    fout.close()

if not os.path.exists('NGrams'):
    print 'Run python findNGrams.py before doing this...'
    sys.exit()

def runPreprocess(flag, gramType):
    if flag == 'mypersonality_depressed':
        print 'Computing vocab for CESD<16...'
        fnames = []
        for s in range(10, 16):
            fname = 'NGrams/mypersonality_' + gramType + '_' + str(s) + '.txt'
            if os.path.exists(fname):
                fnames.append(fname)

        vocab = computeVocab(fnames)
        writeVocab(vocab, 'NGrams/mypersonality_' + gramType + '_vocab_10-15.txt')

        print 'Writing features for CESD<16...'
        for f in fnames:
            feats = (computeFeature(f, vocab))
            outname = f[:-4] + '_feats.txt'
            writeFeature(feats, outname)

        print 'Computing vocab for CESD>43...'
        fnames = []
        for s in range(44, 49):
            fname = 'NGrams/mypersonality_' + gramType + '_' + str(s) + '.txt'
            if os.path.exists(fname):
                fnames.append(fname)

        vocab = computeVocab(fnames)
        writeVocab(vocab, 'NGrams/mypersonality_' + gramType + '_vocab_44-48.txt')

        print 'Writing features for CESD>43...'
        for f in fnames:
            feats = (computeFeature(f, vocab))
            outname = f[:-4] + '_feats.txt'
            writeFeature(feats, outname)

    elif flag == 'reddit_depressed':
        print 'Computing vocab for reddit depressed...'

        fnames = []
        f = open('reddit/filelist.txt', 'r')
        for line in f:
            line = line.strip()
            fname = string.replace(line, 'depressed', 'NGrams')
            fname = fname[:-4] + '_' + gramType + '.txt'
            if os.path.exists(fname):
                fnames.append(fname)

        vocab = computeVocab(fnames)
        writeVocab(vocab, 'reddit/NGrams/reddit_depressed_' + gramType + '_vocab.txt')

        print 'Writing features for reddit depressed...'
        for f in fnames:
            feats = (computeFeature(f, vocab))
            outname = f[:-4] + '_feats.txt'
            writeFeature(feats, outname)

    else:
        print "Dataset not recognized..."
        sys.exit()

args = sys.argv
if len(args) == 3:
    runPreprocess(args[1], args[2])
else:
    print '*****USAGE*****'
    print 'python preprocess_lda.py <dataset> <gramType>'
    print 'dataset: mypersonality_depressed, reddit_depressed'
    print 'gramType: unigrams, bigrams, trigrams'

