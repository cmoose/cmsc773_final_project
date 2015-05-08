#1/usr/bin/python
#This creates the cross validation lists
#Don't rerun this because we all want to use the same cv lists

import pickle
import os
from util import *
import split_mypersonality_depressed
import random

def load_pickle(dirprefix):
  all_pkl = []
  pklfiles = [f for f in os.listdir('cache/%s' % (dirprefix)) if f.endswith('pkl') and not f.startswith('depression')]
  for pklfile in pklfiles:
    d = pickle.load(open('cache/%s/' % (dirprefix) + pklfile))
    all_pkl.append(d)
  return all_pkl

def save_pickle(data):
  fhw = open('cache/cross_valid_lists.pkl', 'wb')
  pickle.dump(data, fhw)
  fhw.close()

def randomize(corpusids):
  num_cv = 5 #5-way cross validation
  (size, remain_size) = divmod(len(corpusids), num_cv)
  cv_list = []
  while len(corpusids) >= size:
    chunk = []
    for i in range(size):
      _id = random.choice(corpusids)
      corpusids.remove(_id)
      chunk.append(_id)
    cv_list.append(chunk)
  #Randomly distribute remainders
  for _id in corpusids:
    ints = range(0,num_cv-1)
    index = random.choice(ints)
    ints.remove(index)
    cv_list[index].append(_id)
  return cv_list

def get_ids(corpus):
  """Return a list of ids from the corpus chunk list"""
  corpusids = []
  for chunk in corpus:
    for _id in chunk.keys():
      corpusids.append(_id)
  return corpusids
def main():
  if os.path.isfile('cache/cross_valid_lists.pkl'):
    print "Cross validation list already exists, exiting..."
    exit()
  corpora = {}
  corpora['mypersonality'] = {}
  corpora['reddit'] = {}
  
  pklobjs = load_pickle('mypersonality/depression')
  (non_depressed_ids, depressed_ids) = split_mypersonality_depressed.split_groups()
  nondepressed = randomize(non_depressed_ids)
  depressed = randomize(depressed_ids)
  corpora['mypersonality']['nondepressed'] = nondepressed
  corpora['mypersonality']['depressed'] = depressed
  
  for corpusname in ['depressed', 'casualconversation', 'confession', 'changemyview', 'self']: 
    pkl = load_pickle('reddit/' + corpusname)
    corpusids = get_ids(pkl)
    cvl = randomize(corpusids)
    corpora['reddit'][corpusname] = cvl
  
  save_pickle(corpora)

if __name__ == '__main__':
  main()
