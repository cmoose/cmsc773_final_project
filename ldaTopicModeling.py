import numpy as np
import lda
import os
import string
import sys

def loadVocab(fname):
    vocab = []
    f = open(fname, 'r')
    for line in f:
        line = line.strip()
        vocab.append(line)
    f.close()
    return vocab

def loadFeatures(fnames):
    feats = []
    for fname in fnames:
        feat = []
        f = open(fname, 'r')
        for line in f:
            line = line.strip()
            feat.append(int(line))
        feats.append(feat)
    return feats

def findTopics(numTopics, numIter, feats):
    model = lda.LDA(n_topics=numTopics, n_iter=numIter, random_state=1)
    X = np.array(feats)
    model.fit(X)
    topic_word = model.topic_word_  # model.components_ also works
    return topic_word

def writeTopics(fname, topic_word, n_top_words):
    fout = open(fname, 'w')
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        fout.write('Topic {}: {}'.format(i, ' '.join(topic_words)) + '\n')
        #print('Topic {}: {}'.format(i, ' '.join(topic_words)))


def runLDA(flag, gramType):
    if flag == 'mypersonality_depressed':
        if not os.path.exists('NGrams'):
            print 'Run python findNGrams.py before doing this...'
            sys.exit()

        if not os.path.exists('NGrams/mypersonality_' + gramType + '_vocab_10-15.txt'):
            print 'Run python preprocess_lda.py before doing this...'
            sys.exit()

        print 'Topic Modeling for MyPersonality CESD<16...'

        fnames = []
        for s in range(10, 16):
            fname = 'NGrams/mypersonality_' + gramType + '_' + str(s) + '_feats.txt'
            if os.path.exists(fname):
                fnames.append(fname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('NGrams/mypersonality_' + gramType + '_vocab_10-15.txt')

        model = lda.LDA(n_topics=5, n_iter=100, random_state=1)
        X = np.array(feats)
        model.fit(X)
        topic_word = model.topic_word_  # model.components_ also works
        n_top_words = 8
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))


        print 'Topic Modeling for MyPersonality CESD>43...'

        fnames = []
        for s in range(44, 49):
            fname = 'NGrams/mypersonality_' + gramType + '_' + str(s) + '_feats.txt'
            if os.path.exists(fname):
                fnames.append(fname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('NGrams/mypersonality_' + gramType + '_vocab_44-48.txt')

        model = lda.LDA(n_topics=5, n_iter=100, random_state=1)
        X = np.array(feats)
        model.fit(X)
        topic_word = model.topic_word_  # model.components_ also works
        n_top_words = 8
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
            print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        topic_word = findTopics(5, 200, feats)
        writeTopics('mypersonality_topics_' + gramType + '.txt', topic_word, 8)

    elif flag == 'reddit_depressed':
        print 'Topic Modeling for Reddit Depressed Using ' + gramType + '...'
        fnames = []
        f = open('reddit/filelist.txt', 'r')
        for line in f:
            line = line.strip()
            fname = string.replace(line, 'depressed', 'NGrams')
            fname = fname[:-4] + '_' + gramType + '_feats.txt'
            fnames.append(fname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('NGrams/reddit_depressed_' + gramType + '_vocab.txt')
        topic_word = findTopics(5, 200, feats)
        writeTopics('reddit_depressed_' + gramType + '.txt', topic_word, 8)

    else:
        print "Wrong dataset flag"
        sys.exit()




#TODO saveTopics to file

args = sys.argv
args = sys.argv
if len(args) == 3:
    runLDA(args[1], args[2])
else:
    print '*****USAGE*****'
    print 'python ldaTopicModeling.py <dataset> <gramType>'
    print 'dataset: mypersonality_depressed, reddit_depressed'
    print 'gramType: unigrams, bigrams, trigrams'
