#!/usr/bin/python
# Simple driver module that orchestrates the loading of the xml files
# into memory using posts.py
# TODO: use pickle for serialization to disk

import os
import posts
import corpus

def test():
  xmldir = 'mypersonality/depression/'
  files = [f for f in os.listdir(xmldir) if f.endswith('xml')] 
  for fn in files:
    print fn
    f = posts.File(xmldir + fn)
    f.load()

def load_all_corpora():
  #for corpusdir in ['reddit/depressed/', 'mypersonality/depression/', 'mypersonality/neuroticism/']:
  for corpusdir in ['mypersonality/neuroticism/']:
    reddit_corpus = corpus.Corpus(corpusdir)
    reddit_corpus.load()
#test()
load_all_corpora()
