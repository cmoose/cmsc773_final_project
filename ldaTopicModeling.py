import numpy as np
import lda
import os

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

if not os.path.exists('NGrams'):
    print 'Run python findNGrams.py before doing this...'
    sys.exit()

if not os.path.exists('NGrams/mypersonality_unigrams_vocab_10-15.txt'):
    print 'Run python preprocess_lda.py before doing this...'
    sys.exit()

print 'Topic Modeling for MyPersonality CESD<16...'

fnames = []
for s in range(10, 16):
    fname = 'NGrams/mypersonality_unigrams_' + str(s) + '_feats.txt'
    if os.path.exists(fname):
        fnames.append(fname)

feats = loadFeatures(fnames)
vocab = loadVocab('NGrams/mypersonality_unigrams_vocab_10-15.txt')

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
    fname = 'NGrams/mypersonality_unigrams_' + str(s) + '_feats.txt'
    if os.path.exists(fname):
        fnames.append(fname)

feats = loadFeatures(fnames)
vocab = loadVocab('NGrams/mypersonality_unigrams_vocab_44-48.txt')

model = lda.LDA(n_topics=5, n_iter=100, random_state=1)
X = np.array(feats)
model.fit(X)
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))


print 'Topic Modeling for Reddit Depressed...'

fnames = ['NGrams/reddit_depressed_unigrams_feats.txt']

feats = loadFeatures(fnames)
vocab = loadVocab('NGrams/reddit_depressed_unigrams_vocab.txt')

model = lda.LDA(n_topics=5, n_iter=100, random_state=1)
X = np.array(feats)
model.fit(X)
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 8
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))

