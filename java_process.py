#!/usr/bin/python
#This doesn't work at the moment, is here just because it was another way of processing through corenlp
from subprocess import Popen, PIPE, call
import os

scriptdir = './stanford-corenlp-full-2015-01-29'
basejava = ['java', '-mx3g', '-cp', scriptdir + '/*']
javaargs = {}
javaargs['pos'] = ['edu.stanford.nlp.tagger.maxent.MaxentTagger', '-model', 'edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger', '-outputFormat', 'slashTags']
def split_reddit_posts():
  fh = open('reddit/depressed.txt')
  i = 1
  for line in fh:
    items = line.split('\t')
    if len(items) == 3:
      post = items[2]
      postid = items[0]
      filename = postid + "_%d" % i
      fhw = open('corenlp-python/depressed/%s.txt' % (filename), 'wb')
      fhw.write(post)
      fhw.close()
      i+=1
def slow_separate_process():
  datadir = 'reddit/depressed/'
  files = [f for f in os.listdir(datadir)]
  action = 'pos'
  for filename in files:
    ftmp = filename.split('.')
    newfilename = ftmp[0] + '_%s.' % (action) + ftmp[1]
    #This is super slow because it creates a new jvm for each file, but it works
    #TODO: get the Stanford API working
    p = Popen(basejava + javaargs[action] + ['-textFile', datadir + filename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    fhw = open(datadir + newfilename, 'wb')
    fhw.write(output)
    fhw.close()
def main():
  datadir = 'reddit/depressed/'
  files = [f for f in os.listdir(datadir)]
  action = 'pos'
  for filename in files:
    ftmp = filename.split('.')
    newfilename = ftmp[0] + '_%s.' % (action) + ftmp[1]
    #This is super slow because it creates a new jvm for each file, but it works
    #TODO: get the Stanford API working
    p = Popen(basejava + javaargs[action] + ['-textFile', datadir + filename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    fhw = open(datadir + newfilename, 'wb')
    fhw.write(output)
    fhw.close()
      #Create dir to hold metadata
      #Run POS tagging, store
      #Run NER, store
      #Run PCFG, store
      #Run dependency parsing, store

def pos_tag(text):
  pass
split_reddit_posts()
