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

emotion.load()
depression_words = emotion.depression_words
cognitive_words = emotion.cognitive_words
depression_words_compiled = emotion.depression_words_compiled
cognitive_words_compiled = emotion.cognitive_words_compiled

def test():
  xmldir = 'mypersonality/depression/'
  #files = [f for f in os.listdir(xmldir) if f.endswith('xml')] 
  xmldir = 'testing/'
  files = ['77417f1e4dc8214d722ac60e593783da.txt.xml']
  for fn in files:
    print fn
    f = posts.File(xmldir + fn)
    f.load()
  return f

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

def count_cognitive_words(f):
  cog_nouns = Counter()
  cog_adjs = Counter()
  cog_advs = Counter()
  cog_words_count = 0
  cog_verbs = Counter()
  print "\tCounting cognitive words..."
  for s in f.sentences:
    for token in s.tokens:
      for regex in cognitive_words_compiled:
        if regex.search(token['lemma']):
          word = token['lemma']
          cog_words_count += 1
          if token['POS'].startswith('NN'):
            cog_nouns[word] += 1
          elif token['POS'].startswith('JJ'):
            cog_adjs[word] += 1
          elif token['POS'].startswith('RB') or token['POS'] == 'WRB':
            cog_advs[word] += 1
          elif token['POS'].startswith('VB') or token['POS'] == 'MD':
            cog_verbs[word] += 1
          #If we've matched once, we don't want it matching multiple times
          break
  return {'cog_nouns': cog_nouns, 'cog_adjs': cog_adjs, 'cog_advs': cog_advs, 'cog_verbs': cog_verbs, 'cog_words_count': cog_words_count}

def count_neg_words(f):
  neg_nouns = Counter()
  neg_adjs = Counter()
  neg_advs = Counter()
  neg_verbs = Counter()
  neg_words_count = 0
  print "\tCounting negative words..."
  for s in f.sentences:
    for token in s.tokens:
      for regex in depression_words_compiled:
        if regex.search(token['lemma']):
          word = token['lemma']
          neg_words_count += 1
          if token['POS'].startswith('NN'):
            neg_nouns[word] += 1
          elif token['POS'].startswith('JJ'):
            neg_adjs[word] += 1
          elif token['POS'].startswith('RB') or token['POS'] == 'WRB':
            neg_advs[word] +=1
          elif token['POS'].startswith('VB') or token['POS'] == 'MD':
            neg_verbs[word] += 1
          #If we've matched once, we don't want it matching multiple times
          break
  
  return {'neg_verbs': neg_verbs, 'neg_nouns': neg_nouns, 'neg_adjs': neg_adjs, 'neg_advs': neg_advs, 'neg_words_count': neg_words_count}

def count_all_verbs(f):
  """Counts verbs within an entire file, returns a Counter() object (see util.py)"""
  all_verbs = Counter()
  print "\tCounting all verbs..."
  for s in f.sentences:
    for _id, verb in s.verbs.items():
      all_verbs[verb] += 1
  return {'all_verbs': all_verbs}

def count_all_words(f):
  all_words_count = 0
  for s in f.sentences:
    s_word_count = len(s.tokens)
    all_words_count += s_word_count
  return {'all_words_count': all_words_count}

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

def count_ner(f):
  print "\tCounting named entities..."
  file_ner = {}
  for s in f.sentences:
    for ner_type,counts in s.ner.items():
      if not file_ner.has_key(ner_type):
        file_ner[ner_type] = Counter()
      file_ner[ner_type] += counts
  return file_ner

def process(dirprefix):
  chunks = create_chunks(dirprefix)
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
    
    all_verbs_count = count_all_verbs(f)
    all_words_count = count_all_words(f)
    neg_words_count = count_neg_words(f)
    cog_words_count = count_cognitive_words(f)
    verb_tense_count = count_verb_tense(f)
    ner_count = count_ner(f)
    
    #Combine all dictionaries
    for k,v in all_verbs_count.items():
      chunk_data[userid][k] = v
    for k,v in neg_words_count.items():
      chunk_data[userid][k] = v
    for k,v in cog_words_count.items():
      chunk_data[userid][k] = v
    for k,v in all_words_count.items():
      chunk_data[userid][k] = v
    chunk_data[userid]['tense'] = verb_tense_count
    chunk_data[userid]['ner'] = ner_count
  fhw = open('cache/%s/%s.pkl' % (dirprefix, chunk_name), 'wb')
  print "Writing chunk's items to disk..."
  print chunk_data
  pickle.dump(chunk_data, fhw)
  fhw.close()

def parallelize(chunks, dirprefix):
  procs = []
  for chunk in chunks:
    #Create a new process for each directory
    print "CREATING NEW PROCESS TO PROCESS %s" % ("\n\t".join(chunk))
    p = Popen(['python', 'driver.py', dirprefix] + chunk)
    procs.append(p)
    print "NEW PROCESS RUNS AS PID %d" % (p.pid)
  exit_codes = [p.wait() for p in procs]
  return exit_codes

def parse_chunk_args(args):
  chunk = []
  for f in args:
    chunk.append(f)
  return chunk

def parse_args(args):
  is_parallel = False #Denotes when command-line option is set, not used in subprocesses
  dirs = []
  chunk = [] #Used only when calling ourselves
  if args.count('--parallel') > 0:
    is_parallel = True
    args.remove('--parallel')
  arg_count = len(args)
  if arg_count == 1:
    #Process all corpora
    dirs = ['mypersonality/depression', 
            'mypersonality/neuroticism', 
            'reddit/depressed', 
            'reddit/casualconversation', 
            'reddit/confession', 
            'reddit/self',
            'reddit/changemyview']
  elif arg_count == 2 and os.path.isdir(args[1]):
    #Process a single corpus
    dirs.append(args[1])
  elif arg_count > 2:
    #We're calling ourselves to create subprocesses
    chunk = parse_chunk_args(args[2:])
    dirs = [args[1]]
  return {'parallel_flag': is_parallel, 'corpora': dirs, 'found_chunk': chunk}

if __name__ == '__main__':
  options = parse_args(sys.argv)
  if options['found_chunk']: #args used in subprocess, we're calling ourselves at this point
    #Process a single chunk in subprocess/parallel mode
    corpusdir = options['corpora'][0]
    process_chunk(options['found_chunk'], corpusdir)
  else:
    if options['parallel_flag']:
      for corpusdir in options['corpora']:
        #parallelize each corpus
        chunks = create_chunks(corpusdir) 
        while chunks:
          #Only create 8 separate processes
          num_subprocs = min(8,len(chunks))
          exit_codes = parallelize(chunks[:num_subprocs], corpusdir)
          print "Finished %d chunks, processing more..." % (num_subprocs)
          chunks = chunks[num_subprocs:]
    else:
      for corpusdir in options['corpora']:
        #Process a directory, non-parallel
        process(corpusdir)
