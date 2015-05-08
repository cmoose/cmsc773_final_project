#!/usr/bin/python

import create_crossvalid_lists as cvl
from util import *
import pickle

corpora = ['mypersonality/depression',
           'reddit/depressed',
           'reddit/casualconversation',
           'reddit/confession',
           'reddit/changemyview',
           'reddit/self']

def get_corpora_vocabs(corpora):
  vocabs = {}
  vocab_keys = ['neg_nouns', 'neg_verbs', 'neg_adjs', 'neg_advs', 'all_verbs', 'cog_verbs', 'cog_nouns', 'cog_adjs', 'cog_advs']
  for key in vocab_keys:
    vocabs[key] = set()
  for corpusname in corpora:
    pkl_list = cvl.load_pickle(corpusname)
    for chunk in pkl_list:
      for _id, counts in chunk.items():
        for vocab_key in counts.keys():
          if vocab_key in vocab_keys:
            words = counts[vocab_key].keys()
            for word in words:
              vocabs[vocab_key].add(word)
  return vocabs

def set_keys_for_corpus(corpusname, vocabs):
  pkl_list = cvl.load_pickle(corpusname)
  corpus = {}
  for chunk in pkl_list:
    for _id, counts in chunk.items():
      corpus[_id] = {}
      for vocab_key in vocabs.keys():
        filewords = set(counts[vocab_key].keys())
        vocab_words = set(vocabs[vocab_key])
        missing = vocab_words.difference(filewords)
        for word in missing:
          counts[vocab_key][word] = 0
      corpus[_id] = counts
  return corpus

def save_pickle(corpusname, corpusdata):
  corpusfn = corpusname.replace('/', '_') + '_corpus_data.pkl'
  fhw = open('cache/%s' % corpusfn, 'wb')
  pickle.dump(corpusdata, fhw)
  fhw.close()

def main():
  global corpora
  print "Creating vocabs..."
  vocabs = get_corpora_vocabs(corpora)
  
  enhanced_corpora = {}
  for corpusname in corpora:
    print "Enhancing %s..." % (corpusname)
    corpusdata = set_keys_for_corpus(corpusname, vocabs)
    #enhanced_corpora[corpusname] = corpusdata #Uncomment if you want everything in memory
    print "\ttotal number of files: %d" % (len(corpusdata.keys()))
    
    #Take out this line if you just want to use the corpusdata
    print "Saving %s to disk..." % (corpusname)
    save_pickle(corpusname, corpusdata) 

if __name__ == '__main__':
  main()
