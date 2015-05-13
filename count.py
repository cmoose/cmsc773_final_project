#!/usr/bin/python
from __future__ import division
import os
import pickle
import split_mypersonality_depressed
from util import *
import math
import emotion
import re
import heapq
import colormap

counter_keys = ['neg_nouns', 'all_verbs', 'cog_adjs', 'neg_advs', 'cog_advs', 'tense', 'neg_verbs', 'cog_nouns', 'neg_adjs', 'cog_verbs']

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
  
  total_dep_neg_words = depressed_group['neg_words_count']
  total_dep_cog_words = depressed_group['cog_words_count']
  total_nondep_neg_words = nondepressed_group['neg_words_count']
  total_nondep_cog_words = nondepressed_group['cog_words_count']
  total_dep_words = depressed_group['all_words_count']
  total_nondep_words = nondepressed_group['all_words_count']
  print "Depressed total words: %d" % (total_dep_words)
  print "Depressed total negative words: {0}, percentage: {1:.4%}".format(total_dep_neg_words, total_dep_neg_words/total_dep_words)
  print "Depressed total cognitive words: {0}, percentage: {1:.4%}".format(total_dep_cog_words, total_dep_cog_words/total_dep_words)
  print "Nondepressed total words: %d" % (total_nondep_words)
  print "Nondepressed total negative words: {0}, percentage: {1:.4%}".format(total_nondep_neg_words, total_nondep_neg_words/total_nondep_words)
  print "Nondepressed total cognitive words: {0}, percentage: {1:.4%}".format(total_nondep_cog_words, total_nondep_cog_words/total_nondep_words)

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
  #Initialize
  for k in counter_keys:
    agg[k] = Counter()
  agg['cog_words_count'] = 0
  agg['neg_words_count'] = 0
  agg['all_words_count'] = 0
  agg['ner'] = {}
  
  for item in group:
    for key in counter_keys:
      agg[key] += item[key]
    #do ner, cog_words_count, neg_words_count, all_words_count
    for entity_type, counts in item['ner'].items():
      if not agg['ner'].has_key(entity_type):
        agg['ner'][entity_type] = Counter()
      agg['ner'][entity_type] += counts
    agg['cog_words_count'] += item['cog_words_count']
    agg['neg_words_count'] += item['neg_words_count']
    agg['all_words_count'] += item['all_words_count']
  return agg
    
def normalize_counts(group):
  for key in counter_keys:
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
  for key in counter_keys:
    vocab = set()
    for word in corpus1[key].keys():
      vocab.add(word)
    for word in corpus2[key].keys():
      vocab.add(word)
    #for key in dict, for word in each type, add new word to the set
    smooth = 1.0/len(vocab)
    for word in vocab:
      if not corpus1[key].has_key(word):
        corpus1[key][word] = 1
      else:
        corpus1[key][word] += 1
      if not corpus2[key].has_key(word):
        corpus2[key][word] = 1
      else:
        corpus2[key][word] += 1
  return (corpus1, corpus2)

def calc_kl(corpus1,corpus2):
  keys = corpus1.keys()
  keys.remove('tense')
  keys.remove('neg_words_count')
  keys.remove('ner')
  keys.remove('cog_words_count')
  keys.remove('all_words_count')
  keys.sort()
  heaps = {}
  kl_counts = {}
  for key in keys:
    kl = 0.0
    pq = []
    for x in corpus1[key].keys():
      p_x = corpus1[key][x]
      q_x = corpus2[key][x]
      part = (p_x)*math.log(p_x/q_x)
      heapq.heappush(pq, (part, x))
      heaps[key] = pq
      kl = kl + part
    kl_counts[key] = kl
    #if key.count('cog') > 0: 
    #  print "\t", key, kl, ' --cog-- ', colormap.rgb_to_hex(colormap.get_color(kl/1.41864815901))
    #else:
    #  print "\t", key, kl, ' -- ', colormap.rgb_to_hex(colormap.get_color(kl/1.25107049293))
  return (heaps,kl_counts)

def clean_counts(corpus):
  #remove urls from counts
  for key in counter_keys:
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
  
def print_kl_avg(kl_counts_1, kl_counts_2):
  sym_counts = {}
  for key in kl_counts_1.keys():
    kl_1 = kl_counts_1[key]
    kl_2 = kl_counts_2[key]
    avg_kl = (kl_1 + kl_2)/2
    sym_counts[key] = avg_kl
  keys = sym_counts.keys()
  keys.sort()
  for key in keys:
    kl = sym_counts[key]
    #print "\t", key, kl
    if key.count('cog') > 0: 
      print "\t", key, kl, ' --cog-- ', colormap.rgb_to_hex(colormap.get_color(kl/1.23225533578))
    else:
      print "\t", key, kl, ' -- ', colormap.rgb_to_hex(colormap.get_color(kl/1.18640149793))
def print_pq_top_scores(heaps):
  for key, pq in heaps.items():
    largest = heapq.nlargest(20, pq)
    print "\t%s" % (key)
    for score in largest:
      print score[1] + ":" + str(score[0])
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
  (nondepressed_group, depressed_group) = smoothing(nondepressed_group, depressed_group)
  normalize_counts(nondepressed_group)
  normalize_counts(depressed_group)
  print "CALCULATE K-L DIVERGENCE"
  (heaps,kl_counts_1) = calc_kl(nondepressed_group, depressed_group)
  #print_pq_top_scores(heaps)
  (heaps,kl_counts_2) = calc_kl(depressed_group, nondepressed_group)
  print_kl_avg(kl_counts_1, kl_counts_2)
  #print_pq_top_scores(heaps)
  
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
    (group_0, group_1) = smoothing(group_0, group_1)
    normalize_counts(group_0)
    normalize_counts(group_1)
    print "CALCULATE K-L DIVERGENCE"
    (heaps,kl_counts_1) = calc_kl(group_0, group_1)
    #print_pq_top_scores(heaps)
    (heaps,kl_counts_2) = calc_kl(group_1, group_0)
    print_kl_avg(kl_counts_1, kl_counts_2)
    #print_pq_top_scores(heaps)
  
if __name__ == '__main__':
  compare_everything()
