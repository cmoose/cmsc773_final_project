#1/usr/bin/python

import xmltodict
from util import *
import re

class File():
  """This class loads a Stanford NLP xml file"""
  def __init__(self, filename=None):
    self.filename = filename
    self.sentences = []
  def load(self):
    if self.sentences:
      return
    d = xmltodict.parse(open(self.filename))
    #TODO: add coreferences
    sents_d = d['root']['document']['sentences']['sentence']
    try:
      #Grrr xmltodict...
      #Try to access this as an array, if it fails, there is only one sentence
      sents_d[0] 
      for i in range(0, len(sents_d)):
        self.sentences.append(Sentence(sents_d[i]))
    except KeyError:
      #If we got here, it means there is only one sentence in this file
      self.sentences.append(Sentence(sents_d))
    print "Loaded all sentences in file: %s..." % (self.filename)
  
  #File aggregation functions
  def count_verbs(self):
    self.load()
    total_count = Counter()
    for s in self.sentences:
      v = s.verbs.values()
      for verb in v:
        total_count[verb] += 1
    return total_count
  def count_verbs_byfilter(self, verbset):
    self.load()
    total_count = Counter()
    for s in self.sentences:
      count = s.count_verbs_byfilter(verbset)
      total_count += count
    return total_count
  def count_nsubj_dependents(self):
    self.load()
    total_count = Counter()
    for s in self.sentences:
      count = s.count_nsubj_dependents()
      total_count += count
    return total_count

class Sentence():
  #Initialize the object with data
  def __init__(self, sent_dict = {}):
    #Hack: if there is only a root dependency item (the sentence is literally a <period>)
    # or some ridiculousness like that, then encapsulate it in an array so it functions
    # like the rest of the xmltodict dictionary structures
    tokens_d = sent_dict['tokens']['token']
    if not isinstance(tokens_d, list):
      tokens_d = [tokens_d]
    deps_d = sent_dict['dependencies'][0]['dep']
    if not isinstance(deps_d, list):
      deps_d = [deps_d]
    
    self.tokens = []
    self.deptree = self.build_deptree(deps_d)
    self.raw_deptree = deps_d
    self.verbs = {}
    self.verbs_count = Counter()
    self.adjs = {}
    self.nouns = {}
    self.advs = {}
    
    for i in range(0,len(tokens_d)):
      token = {}
      token['POS'] = tokens_d[i]['POS']
      token['word'] = tokens_d[i]['word']
      token['@id'] = tokens_d[i]['@id']
      token['lemma'] = tokens_d[i]['lemma']
      #TODO: add NER
      self.tokens.append(token)
      if token['POS'].startswith('VB') or token['POS'] == 'MD':
        #Store @id as key, verb as value
        self.verbs[int(token['@id'])] = tokens_d[i]['lemma']
        self.verbs_count[token['POS']] += 1
      elif token['POS'].startswith('JJ'):
        self.adjs[int(token['@id'])] = tokens_d[i]['lemma']
      elif token['POS'].startswith('NN'):
        self.nouns[int(token['@id'])] = tokens_d[i]['lemma']
      elif token['POS'].startswith('RB') or token['POS'] == 'WRB':
        self.advs[int(token['@id'])] = tokens_d[i]['lemma']
  
  def build_deptree(self, sent_dep):
    deptree = {}
    
    #This just initializes the deptree dictionary so we don't have keyerrors
    for i in range(1,len(sent_dep)+1):
      deptree[i] = {}
      deptree[i]['governors'] = []
      deptree[i]['dependents'] = []
    
    for item in sent_dep:
      _id = int(item['dependent']['@idx'])
      gov_id = int(item['governor']['@idx'])
      _type = item['@type']
      deptree[_id]['#text'] = item['dependent']['#text']
      deptree[_id]['governors'].append((gov_id, _type))
      if _type != 'root':
        deptree[gov_id]['dependents'].append((_id,_type))
    return deptree
  
  def get_root(self):
    """Returns root word"""
    return {self.raw_deptree[0]['dependent']['@idx']: self.raw_deptree[0]['dependent']['#text']}
  
  def get_dependents(self, w_id):
    """Gets word's immediate dependents (children)"""
    return self.deptree[w_id]['dependents']
  
  def get_governors(self, w_id):
    """Gets all word's immediate governors (parents)"""
    return self.deptree[w_id]['governors']
  
  def get_verb_object(self, w_id):
    nobj = {}
    for d in self.get_dependents(w_id):
      if d[1] == 'nobj':
        nobj = {d[0]: self.tokens[d[0]-1]['word']}
        break
    return nobj
  def get_verb_subject(self, w_id):
    """Gets the n_subject of the verb, needs @id position in sentence"""
    nsubj = {}
    if not self.get_dependents(w_id):
      #Verb has no dependents, check if it's copular
      #If it is, find its governor, then find nsubj dependent
      _id = 0
      verb = self.verbs[w_id]
      for g in self.get_governors(w_id):
        if g[1] == 'cop' or verb == 'be':
          _id = g[0]
          break
      if _id != 0:
        for d in self.get_dependents(_id):
          if d[1] == 'nsubj':
            nsubj = {d[0]: self.tokens[d[0]-1]['word']}
            break
    else:
      #We have dependents, find the nsubj
      for d in self.get_dependents(w_id):
        if d[1] == 'nsubj':
          nsubj = {d[0]: self.tokens[d[0]-1]['word']}
          break
    return nsubj
  
  #Counting functions
  def count_verbs_byfilter(self, verbset):
    """Counts verbs based on a verbset filter, returns a Counter() object (see util.py)"""
    counts = Counter()
    for v in self.verbs.values():
      for regex in verbset:
        if re.search(regex, v):
          counts[v] += 1
    return counts
  def count_nsubj_dependents(self):
    """Counts the type and number of each of the nsubj labels, returns a Counter() object (see util.py)"""
    counts = Counter()
    for item in self.raw_deptree:
      if item['@type'] == 'nsubj':
        print item
        counts[item['dependent']['#text']] += 1
    return counts
  
  #Other functions
  def get_raw_text(self):
    """Useful to print out the raw sentence text"""
    raw = " ".join([token['word'] for token in self.tokens])
    return raw
