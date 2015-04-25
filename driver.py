#!/usr/bin/python
# Simple driver module that orchestrates the loading of the xml files
# into memory using posts.py, then grabs all the data/counts we want

import sys
from subprocess import call, Popen
import os
import posts
import corpus
from util import *
import emotion
import re
import pickle

def test():
  xmldir = 'mypersonality/depression/'
  files = [f for f in os.listdir(xmldir) if f.endswith('xml')] 
  for fn in files:
    print fn
    f = posts.File(xmldir + fn)
    f.load()

def filter_completed_chunks(files, dirprefix):
  pklfiles = [f for f in os.listdir('cache/%s' % (dirprefix)) if f.endswith('pkl') and not f.startswith('depression')]
  for pklfile in pklfiles:
    d = pickle.load(open('cache/%s/' % (dirprefix) + pklfile))
    for userid in d.keys():
      if files.count(userid + '.txt.xml') > 0:    
        files.remove(userid + '.txt.xml')
  return files

def create_chunks(dirprefix):
  xmldir = dirprefix + '/'
  files = [f for f in os.listdir(xmldir) if f.endswith('xml')]
  files = filter_completed_chunks(files, xmldir)
  chunks = []
  i = 0
  chunk = []
  for fn in files:
    if i < 20: #Create lists of 20 files each
      chunk.append(xmldir + fn)
      i += 1
    else:
      chunks.append(chunk)
      i = 0
      chunk = [xmldir + fn]
  if chunk:
    chunks.append(chunk)
  return chunks

def count_neg_words(f):
  neg_nouns = Counter()
  neg_adjs = Counter()
  neg_advs = Counter()
  print "\tCounting negative words..."
  for s in f.sentences:
    for regex in emotion.depression_words:
      #Count nouns
      for _id, noun in s.nouns.items():
        if re.search(regex, noun):
          neg_nouns[noun+'_'+s.tokens[_id-1]['POS']] += 1
      for _id, adj in s.adjs.items():
        if re.search(regex, adj):
          neg_adjs[adj+'_'+s.tokens[_id-1]['POS']] += 1
      for _id, adv in s.advs.items():
        if re.search(regex, adv):
          neg_advs[adv+'_'+s.tokens[_id-1]['POS']] += 1
  return {'neg_nouns': neg_nouns, 'neg_adjs': neg_adjs, 'neg_advs': neg_advs}

def count_neg_and_all_verbs(f):
  """Counts verbs within an entire file, returns a Counter() object (see util.py)"""
  neg_verbs = Counter()
  all_verbs = Counter()
  print "\tCounting neg and all verbs..."
  for s in f.sentences:
    for _id, verb in s.verbs.items():
      all_verbs[verb] += 1
      for regex in emotion.depression_verbs:
        if re.search(regex, verb):
          neg_verbs[verb] += 1
  return {'neg_verbs': neg_verbs, 'all_verbs': all_verbs}

def count_verb_tense(f):
  tense = Counter()
  print "\tCounting verb tenses..."
  for s in f.sentences:
    for pos, counter in s.verbs_count.items():
      if ['VBD', 'VBN'].count(pos) == 1:
        #Found past tense
        tense['past'] += counter
      elif pos == 'MD':
        #Found modal/future
        tense['modal'] += counter
  return tense

def process(dirprefix):
  chunks = create_chunks(dirprefix)
  emotion.load()
  for chunk in chunks:
    process_chunk(chunk, dirprefix)

def process_chunk(chunk, dirprefix):
  start_chunk = chunk[0].split('/')[-1].split('.')[0][0:10]
  end_chunk = chunk[-1].split('/')[-1].split('.')[0][0:10]
  chunk_name = start_chunk + '_to_' + end_chunk
  print "\n**Processing new chunk %s**" % (chunk_name)
  chunk_data = {}
  for fn in chunk:
    userid = fn.split('/')[-1].split('.')[0]
    chunk_data[userid] = {}
    f = posts.File(fn)
    print "Processing new file %s..." % (f.filename)
    f.load()
    
    neg_all_verbs_count = count_neg_and_all_verbs(f)
    neg_words_count = count_neg_words(f)
    verb_tense_count = count_verb_tense(f)
    
    #Combine all dictionaries
    for k,v in neg_all_verbs_count.items():
      chunk_data[userid][k] = v
    for k,v in neg_words_count.items():
      chunk_data[userid][k] = v
    chunk_data[userid]['tense'] = verb_tense_count
  fhw = open('cache/%s/%s.pkl' % (dirprefix, chunk_name), 'wb')
  print "Writing chunk's items to disk..."
  print chunk_data
  pickle.dump(chunk_data, fhw)
  fhw.close()

def parse_chunk_args(args):
  chunk = []
  for f in args:
    chunk.append(f)
  return chunk

def parallelize(chunks, dirprefix):
  for chunk in chunks:
    #Create a new process for each directory
    print "CREATING NEW PROCESS TO PROCESS %s" % ("\n\t".join(chunk))
    pid = Popen(['python', 'driver.py', dirprefix] + chunk).pid
    print "NEW PROCESS RUNS AS PID %d" % (pid)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    dirprefix = 'mypersonality/neuroticism'
    chunks = create_chunks(dirprefix)
    #Only create 8 separate processes
    parallelize(chunks[:8], dirprefix)
    
    #No args, process all
    #dirs = ['mypersonality/depression', 'reddit/depressed', 'reddit/casualconveration', 'reddit/confession', 'reddit/changemyview']
    #process('mypersonality/depression')
    #process('reddit/depressed')
    #process('reddit/casualconversation')
    #process('reddit/confession')
    #process('reddit/changemyview')
  elif len(sys.argv) == 2:
    #Process a directory, non-parallel
    process(sys.argv[1])
  elif len(sys.argv) > 2:
    emotion.load()
    chunk = parse_chunk_args(sys.argv[2:])
    dirprefix = sys.argv[1]
    process_chunk(chunk, dirprefix)
