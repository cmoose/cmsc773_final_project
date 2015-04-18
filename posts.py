#1/usr/bin/python

import xmltodict
from util import *

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

class Sentence():
  #Initialize the object with data
  def __init__(self, sent_dict = {}):
    self.tokens = []
    self.deptree = sent_dict['dependencies'][2]['dep']
    self.verbs = {}
    
    for i in range(0,len(sent_dict['tokens']['token'])):
      token = {}
      token['POS'] = sent_dict['tokens']['token'][i]['POS']
      token['word'] = sent_dict['tokens']['token'][i]['word']
      token['@id'] = sent_dict['tokens']['token'][i]['@id']
      #TODO: add NER
      self.tokens.append(token)
      if token['POS'].startswith('VB'):
        #Store @id as key, verb as value
        self.verbs[token['@id']] = sent_dict['tokens']['token'][i]['lemma']
  
  def get_root(self):
    """Returns root word"""
    return self.deptree[0]['dependent']['#text']
  
  #Verb related functions
  def find_verb(self, verbset):
    """Finds existence of verb(s) from set of verbs, returns @id positions in sentence"""
    ids = []
    for k,v in self.verbs.items():
      if v in verbset: #TODO: This may need to be a regex, not sure how well sets work for this
        ids.append(k)
    return ids
  def get_verb_subject(self, w_id):
    """Gets the n_subject of the verb, needs @id position in sentence"""
    nsubj = {}
    for item in self.deptree:
      if int(item['governor']['@idx']) == w_id:
        if item['@type'] == 'nsubj':
          nsubj = item['dependent']
    return nsubj
  
  #Counting functions
  def count_verbs(self, verbset):
    """Counts verbs based on a verbset, returns a Counter() object (see util.py)"""
    counts = Counter()
    for v in self.verbs.values():
      if v in verbset:
        counts[v] += 1
    return counts
  def count_nsubj_dependents(self):
    """Counts the type and number of each of the nsubj labels, returns a Counter() object (see util.py)"""
    counts = Counter()
    for item in self.deptree:
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
