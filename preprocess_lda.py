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

'''
print 'Computing vocab for CESD<16...'
fnames = []
for s in range(10, 16):
    fname = 'NGrams/mypersonality_unigrams_' + str(s) + '.txt'
    if os.path.exists(fname):
        fnames.append(fname)

vocab = computeVocab(fnames)
writeVocab(vocab, 'NGrams/mypersonality_unigrams_vocab_10-15.txt')

print 'Writing features for CESD<16...'
for f in fnames:
    feats = (computeFeature(f, vocab))
    outname = f[:-4] + '_feats.txt'
    writeFeature(feats, outname)

print 'Computing vocab for CESD>43...'
fnames = []
for s in range(44, 49):
    fname = 'NGrams/mypersonality_unigrams_' + str(s) + '.txt'
    if os.path.exists(fname):
        fnames.append(fname)

vocab = computeVocab(fnames)
writeVocab(vocab, 'NGrams/mypersonality_unigrams_vocab_44-48.txt')

print 'Writing features for CESD>43...'
for f in fnames:
    feats = (computeFeature(f, vocab))
    outname = f[:-4] + '_feats.txt'
    writeFeature(feats, outname)
'''

print 'Computing vocab for reddit depressed...'
#fnames = ['NGrams/reddit_depressed_unigrams.txt']

fnames = []
f = open('reddit/filelist.txt', 'r')
for line in f:
    line = line.strip()
    fname = string.replace(line, 'depressed', 'NGrams')
    fname = fname[:-4] + '_unigrams.txt'
    fnames.append(fname)

vocab = computeVocab(fnames)
writeVocab(vocab, 'reddit/NGrams/reddit_depressed_unigrams_vocab.txt')

print 'Writing features for reddit depressed...'
for f in fnames:
    feats = (computeFeature(f, vocab))
    outname = f[:-4] + '_feats.txt'
    writeFeature(feats, outname)

