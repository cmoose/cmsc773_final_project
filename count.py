#!/usr/bin/python
import os
import pickle
import split_mypersonality_depressed
from util import *

def load_pickle(dirprefix):
  all_pkl = []
  pklfiles = [f for f in os.listdir('cache/%s' % (dirprefix)) if f.endswith('pkl') and not f.startswith('depression')]
  for pklfile in pklfiles:
    d = pickle.load(open('cache/%s/' % (dirprefix) + pklfile))
    all_pkl.append(d)
  return all_pkl

def save_pickle(data):
  #Save to cache/aggregates
  pass

def group_myper_counts(pkl_list, non, dep):
  group_neg = []
  group_pos = []
  for pklfile in pkl_list:
    for _id in pklfile.keys():
      if non.count(_id) > 0:
        group_neg.append(pklfile[_id])
      elif dep.count(_id) > 0:
        group_pos.append(pklfile[_id])
  return (group_neg, group_pos)

def group_counts(pkl_list):
  group = []
  for pklfile in pkl_list:
    for _id in pklfile.keys():
      group.append(pklfile[_id])
  return group

def aggregate_counts(group):
  agg = {}
  keys = group[0].keys()
  for k in keys:
    agg[k] = Counter()
  for item in group:
    for key in item.keys():
      agg[key] += item[key]
  return agg
    
def normalize_counts(group):
  for key in group.keys():
    group[key].normalize()
  return group
def get_counts(cachedir):
  counts = {}
  if not os.path.isdir('cache/' + cachedir):
    print "Error...cache/%s not a directory" % (cachedir)
    return counts
  if cachedir == 'mypersonality/depression':
    #Count up mypersonality/depression data (two groups)
    pklobjs = load_pickle('mypersonality/depression')
    (non_depressed_ids, depressed_ids) = split_mypersonality_depressed.split_groups()
    (neg_counts, pos_counts) = group_myper_counts(pklobjs, non_depressed_ids, depressed_ids)
    total_n = aggregate_counts(neg_counts)
    total_p = aggregate_counts(pos_counts)
    return {'notdepressed': total_n, 'depressed': total_p}
  else:
    pklobjs = load_pickle(cachedir)
    grouped = group_counts(pklobjs)
    total = aggregate_counts(grouped)
    return total
def main():
  print total_n['neg_adjs']
  print total_n.keys()
  #total_normalized_n = normalize_counts(total_n)
  #total_normalized_p = normalize_counts(total_p)
  #TODO: need to save to pickle, should be one object per directory (except mypersonality/depression)
  
  #Total count reddit/depressed

#main()
