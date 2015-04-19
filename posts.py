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
    d = xmltodict.parse(open(self.filename))
    #TODO: add coreferences
    sents_d = d['root']['document']['sentences']['sentence']
    for i in range(0, len(sents_d)):
      self.sentences.append(Sentence(sents_d[i]))
    print "Loaded all sentences in file: %s..." % (self.filename)

class Sentence():
  #Initialize the object with data
  def __init__(self, sent_dict = {}):
    self.tokens = []
    self.deptree = self.build_deptree(sent_dict['dependencies'][0]['dep'])
    self.raw_deptree = sent_dict['dependencies'][0]['dep']
    self.verbs = {}
    self.adjs = {}
    
    for i in range(0,len(sent_dict['tokens']['token'])):
      token = {}
      token['POS'] = sent_dict['tokens']['token'][i]['POS']
      token['word'] = sent_dict['tokens']['token'][i]['word']
      token['@id'] = sent_dict['tokens']['token'][i]['@id']
      #TODO: add NER
      self.tokens.append(token)
      if token['POS'].startswith('VB'):
        #Store @id as key, verb as value
        self.verbs[int(token['@id'])] = sent_dict['tokens']['token'][i]['lemma']
      if token['POS'].startswith('JJ'):
        self.adjs[int(token['@id'])] = sent_dict['tokens']['token'][i]['lemma']
  
  def build_deptree(self, sent_dep):
    deptree = {}
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
  
  #Adjective related functions
  def find_adjs(self, wordset):
    """Finds matching words from text, returns @id positions in sentence
Note: Due to the size of the wordset and the fact they're regexes, this will be slow"""
    ids = []
    for k,v in self.adjs.items():
      for regex in wordset:
        if re.search(regex, v):
          print k, v, regex
          ids.append(k)
    return ids
  
  #Verb related functions
  def find_verb(self, verbset):
    """Finds existence of verb(s) from set of verbs, returns @id positions in sentence"""
    ids = []
    for k,v in self.verbs.items():
      for regex in verbset:
        if re.search(regex, v):
          print k, v, regex
          ids.append(k)
    return ids
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
  def count_verbs(self, verbset):
    """Counts verbs based on a verbset, returns a Counter() object (see util.py)"""
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
        counts[item['dependent']['#text']] += 1
    return counts
  
  #Other functions
  def get_raw_text(self):
    """Useful to print out the raw sentence text"""
    raw = " ".join([token['word'] for token in self.tokens])
    return raw
  def some_deptree_function(self):
    """Write your own..."""
    pass
