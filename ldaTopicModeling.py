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

def writeTopics(fname, topic_word, vocab, n_top_words):
    fout = open(fname, 'w')
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        fout.write('Topic {}: {}'.format(i, ' '.join(topic_words)) + '\n')
        #print('Topic {}: {}'.format(i, ' '.join(topic_words)))


def runLDA(dataset, gramType):
    print 'LDA for ' + dataset + ' ' + gramType + '...'
    if dataset == 'mypersonality_depressed':
        if not os.path.exists('mypersonality/NGrams'):
            print 'Run python findNGrams.py before doing this...'
            sys.exit()

        
        if not os.path.exists('mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_0-15.txt'):
            print 'Run python preprocess_lda.py before doing this...'
            sys.exit()

        print 'Topic Modeling for MyPersonality CESD<=15...'

        SCORERANGE = [0,15]
        fnames = []
        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith("_feats_0-15.txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = int(fsplit[-3])
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('mypersonality/NGrams/mypersonality_depressed_' + gramType + '_vocab_0-15.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('mypersonality/mypersonality_depressed_' + gramType + '_topics_0-15.txt', topic_word, vocab, 8)

        
        if not os.path.exists('mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_0-24.txt'):
            print 'Run python preprocess_lda.py before doing this...'
            sys.exit()

        print 'Topic Modeling for MyPersonality CESD<=24...'

        SCORERANGE = [0,24]
        fnames = []
        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith("_feats_0-24.txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = int(fsplit[-3])
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('mypersonality/NGrams/mypersonality_depressed_' + gramType + '_vocab_0-24.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('mypersonality/mypersonality_depressed_' + gramType + '_topics_0-24.txt', topic_word, vocab, 8)

        if not os.path.exists('mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_44-60.txt'):
            print 'Run python preprocess_lda.py before doing this...'
            sys.exit()

        print 'Topic Modeling for MyPersonality CESD>=44...'

        SCORERANGE = [44,60]
        fnames = []
        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith("_feats_-44-60.txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = int(fsplit[-3])
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('mypersonality/NGrams/mypersonality_depressed_' + gramType + '_vocab_44-60.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('mypersonality/mypersonality_depressed_' + gramType + '_topics_44-60.txt', topic_word, vocab, 8)

        if not os.path.exists('mypersonality/NGrams/' + dataset + '_' + gramType + '_vocab_31-60.txt'):
            print 'Run python preprocess_lda.py before doing this...'
            sys.exit()

        
        print 'Topic Modeling for MyPersonality CESD>=31...'
        
        SCORERANGE = [31,60]
        fnames = []
        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith("_feats_31-60.txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = int(fsplit[-3])
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('mypersonality/NGrams/mypersonality_depressed_' + gramType + '_vocab_31-60.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('mypersonality/mypersonality_depressed_' + gramType + '_topics_31-60.txt', topic_word, vocab, 8)

    if dataset == 'mypersonality_neurotic':
        print 'Topic Modeling for MyPersonality score<=2.25...'
        
        SCORERANGE = [0,2.25]
        fnames = []
        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith("_feats_0.0-2.25.txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = int(fsplit[-3])
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('mypersonality/NGrams/mypersonality_depressed_' + gramType + '_vocab_0.0-2.25.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('mypersonality/mypersonality_depressed_' + gramType + '_topics_0.0-2.25.txt', topic_word, vocab, 8)
        
        print 'Topic Modeling for MyPersonality score>=3.05...'
        
        SCORERANGE = [3.05,5.0]
        fnames = []
        for fname in os.listdir("mypersonality/NGrams/"):
            if fname.endswith("_feats_0.0-3.05.txt") and fname.startswith(dataset + '_' + gramType):
                fsplit = fname.split('_')
                score = int(fsplit[-3])
                if score >= SCORERANGE[0] and score <= SCORERANGE[1]:
                    fullfname = "mypersonality/NGrams/" + fname
                    fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('mypersonality/NGrams/mypersonality_depressed_' + gramType + '_vocab_3.05-5.0.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('mypersonality/mypersonality_depressed_' + gramType + '_topics_3.05-5.0.txt', topic_word, vocab, 8)

    if dataset == 'reddit_depressed':
        print 'Topic Modeling for reddit_depressed...'
        
        fnames = []
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + "_feats.txt") and fname.startswith(dataset):
                fullfname = "reddit/NGrams/" + fname
                fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('reddit/NGrams/reddit_depressed_' + gramType + '_vocab_all.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('reddit/reddit_depressed_' + gramType + '_topics.txt', topic_word, vocab, 8)

    if dataset == 'reddit_nondepressed':
        print 'Topic Modeling for reddit_nondepressed...'
        
        fnames = []
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + "_feats_full.txt") and fname.startswith(dataset):
                fullfname = "reddit/NGrams/" + fname
                fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('reddit/NGrams/reddit_nondepressed_' + gramType + '_vocab_all.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('reddit/reddit_nondepressed_' + gramType + '_topics.txt', topic_word, vocab, 8)


    if dataset == 'reddit_nondepressed_changemyview':
        print 'Topic Modeling for reddit_nondepressed_changemyview...'
        
        fnames = []
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + "_feats.txt") and fname.startswith(dataset):
                fullfname = "reddit/NGrams/" + fname
                fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('reddit/' + dataset + '_' + gramType + '_topics.txt', topic_word, vocab, 8)


    if dataset == 'reddit_nondepressed_casualconversation':
        print 'Topic Modeling for reddit_nondepressed_casualconversation...'
        
        fnames = []
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + "_feats.txt") and fname.startswith(dataset):
                fullfname = "reddit/NGrams/" + fname
                fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('reddit/' + dataset + '_' + gramType + '_topics.txt', topic_word, vocab, 8)


    if dataset == 'reddit_nondepressed_confession':
        print 'Topic Modeling for reddit_nondepressed_confession...'
        
        fnames = []
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + "_feats.txt") and fname.startswith(dataset):
                fullfname = "reddit/NGrams/" + fname
                fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('reddit/' + dataset + '_' + gramType + '_topics.txt', topic_word, vocab, 8)


    if dataset == 'reddit_nondepressed_self':
        print 'Topic Modeling for reddit_nondepressed_self...'
        
        fnames = []
        for fname in os.listdir("reddit/NGrams/"):
            if fname.endswith(gramType + "_feats.txt") and fname.startswith(dataset):
                fullfname = "reddit/NGrams/" + fname
                fnames.append(fullfname)

        feats = loadFeatures(fnames)
        vocab = loadVocab('reddit/NGrams/' + dataset + '_' + gramType + '_vocab_all.txt')
        topic_word = findTopics(10, 900, feats)
        writeTopics('reddit/' + dataset + '_' + gramType + '_topics.txt', topic_word, vocab, 8)



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
