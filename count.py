#!/usr/bin/python
from __future__ import division
import os
import pickle
import split_mypersonality_depressed
from util import *
import math
import emotion
import re

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

def count_cog_verbs(group):
  emotion.load()
  cog_count = 0
  for regex in emotion.cognitive_words:
    for verb, count in group['all_verbs'].items():
      if re.search(regex, verb):
        cog_count += 1
  return cog_count

def kasia_count():
  #Compare mypersonality/depression non_depressed versus depressed
  corpusname = 'mypersonality/depression'
  group = load_counts(corpusname)
  nondepressed_group = group['notdepressed']
  depressed_group = group['depressed']
  nondepressed_group = clean_counts(nondepressed_group)
  depressed_group = clean_counts(depressed_group)
  
  depressed_cog_total = depressed_group['cog_nouns'] + depressed_group['cog_adjs'] + depressed_group['cog_advs']
  depressed_neg_total = depressed_group['neg_nouns'] + depressed_group['neg_adjs'] + depressed_group['neg_advs'] + depressed_group['neg_verbs']
  total_dep_neg_words = depressed_neg_total.totalCount()
  total_dep_cog_words = depressed_cog_total.totalCount() + count_cog_verbs(depressed_group)
  nondep_cog_total = nondepressed_group['cog_nouns'] + nondepressed_group['cog_adjs'] + nondepressed_group['cog_advs']
  nondep_neg_total = nondepressed_group['neg_nouns'] + nondepressed_group['neg_adjs'] + nondepressed_group['neg_advs'] + nondepressed_group['neg_verbs']
  total_nondep_neg_words = nondep_neg_total.totalCount()
  total_nondep_cog_words = nondep_cog_total.totalCount() + count_cog_verbs(nondepressed_group)
  print "Depressed total negative words: %d" % (total_dep_neg_words)
  print "Depressed total cognitive words: %d" % (total_dep_cog_words)
  print "Nondepressed total negative words: %d" % (total_nondep_neg_words)
  print "Nondepressed total cognitive words: %d" % (total_nondep_cog_words)

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

def load_counts(cachedir):
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

def smoothing(corpus1, corpus2):
  for key in corpus1.keys():
    vocab = set()
    for word in corpus1[key].keys():
      vocab.add(word)
    for word in corpus2[key].keys():
      vocab.add(word)
    #for key in dict, for word in each type, add new word to the set
    smooth = 1.0/len(vocab)
    for word in vocab:
      if not corpus1[key].has_key(word):
        corpus1[key][word] = smooth
      if not corpus2[key].has_key(word):
        corpus2[key][word] = smooth
  return (corpus1, corpus2)

def calc_kl(corpus1,corpus2):
  kl = 0.0
  keys = corpus1.keys()
  keys.remove('tense')
  keys.sort()
  for key in keys:
    for x in corpus1[key].keys():
      p_x = corpus1[key][x]
      q_x = corpus2[key][x]
      part = (p_x)*math.log(p_x/q_x)
    #if p == 'r' and q == 'd':
    #  heapq.heappush(top10,(part,x))
    kl = kl + part
    print "\t", key, kl

def clean_counts(corpus):
  #remove urls from counts
  for key in corpus.keys():
    for word in corpus[key].keys():
      if word.count('https://') > 0 or word.count('http://') > 0:
        corpus[key].pop(word)
  return corpus

def print_verb_tense_stuff(group):
  total_verb_count = 0
  past_tense_count = group['tense']['past']
  future_tense_count = group['tense']['modal']
  for verb,count in group['all_verbs'].items():
    total_verb_count += count
  print "\tTotal # of verbs in corpus: %d" % (total_verb_count)
  print "\t{:.4%} past tense, {:.4%} future tense".format(past_tense_count/total_verb_count, future_tense_count/total_verb_count)
  
def compare_everything():
  #Compare mypersonality/depression non_depressed versus depressed
  corpusname = 'mypersonality/depression'
  group = load_counts(corpusname)
  nondepressed_group = group['notdepressed']
  depressed_group = group['depressed']
  nondepressed_group = clean_counts(nondepressed_group)
  depressed_group = clean_counts(depressed_group)
  print "COMPARING %s" % (corpusname.upper())
  print_verb_tense_stuff(nondepressed_group)
  print_verb_tense_stuff(depressed_group)
  normalize_counts(nondepressed_group)
  normalize_counts(depressed_group)
  (nondepressed_group, depressed_group) = smoothing(nondepressed_group, depressed_group)
  print "CALCULATE K-L DIVERGENCE"
  calc_kl(nondepressed_group, depressed_group)
  
  reddit = []
  reddit.append(('reddit/depressed', 'reddit/casualconversation'))
  reddit.append(('reddit/depressed', 'reddit/confession'))
  reddit.append(('reddit/depressed', 'reddit/changemyview'))
  reddit.append(('reddit/depressed', 'reddit/self'))
  for t in reddit:
    group_0 = load_counts(t[0])
    group_1 = load_counts(t[1])
    group_0 = clean_counts(group_0)
    group_1 = clean_counts(group_1)
    print "\nCOMPARING %s WITH %s" % (t[0].upper(), t[1].upper())
    print_verb_tense_stuff(group_0)
    print_verb_tense_stuff(group_1)
    normalize_counts(group_0)
    normalize_counts(group_1)
    (group_0, group_1) = smoothing(group_0, group_1)
    print "CALCULATE K-L DIVERGENCE"
    calc_kl(group_0, group_1)
  
  #Comparisons are:
  #neg_nouns, neg_adjs, neg_advs (or together)
  #neg_verbs, all_verbs
  #tense['past'], tense['modal']
  #cog_nouns, cog_adjs, cog_advs (cog_verbs?)
  #mypersonality/depression, non_depressed, depressed
  #reddit/depressed with reddit/{casualconversation, confession, changemyview}
  #mypersonality/neuroticism, high, low

if __name__ == '__main__':
  compare_everything()
