#!/usr/bin/python
import pickle
import os
import re

cat_id_map = {}
categories = {}
depression_categories = ['sad', 'anger', 'anx', 'inhib', 'death', 'negemo', 'swear']
cognitive_categories = ['insight']
depression_words = []
depression_verbs = []
cognitive_words = []
depression_words_compiled = []
cognitive_words_compiled = []

def compile_regexes():
  depression_words_regex = []
  cognitive_words_regex = []
  for regex in depression_words:
    compiled = re.compile(regex)
    depression_words_regex.append(compiled)
  for regex in cognitive_words:
    compiled = re.compile(regex)
    cognitive_words_regex.append(compiled)
  return (depression_words_regex, cognitive_words_regex)

def load_liwc(filename):
  """Loads the LIWC file and drops the words into an in-memory structure"""
  fh = open(filename)
  percent_mark_count = 0
  for line in fh:
    if line.strip() == '%':
      percent_mark_count += 1  
      continue
    if percent_mark_count < 2:
      #We are in an area of the file describing the categories and their ids
      cat = line.strip().split()
      cat_id_map[cat[1]] = cat[0]
      categories[cat[0]] = set() #initialize the second structure now
    elif percent_mark_count >= 2:
      #We are in the bottom half of the file
      items = line.strip().split()
      cats = items[1:]
      word = items[0]
      word = word.replace('*', '.*')
      word = '^' + word + '$' #make it a real regex
      for cat_id in cats:
        categories[cat_id].add(word)
  s = set()
  for cat in depression_categories:
    s = s.union(categories[cat_id_map[cat]])
  depression_words = list(s)
  q = set()
  for cat in cognitive_categories:
    q = q.union(categories[cat_id_map[cat]])
  cognitive_words = list(q)
  print "Loaded emotion.categories and emotion.cat_id_map structures..."
  return (depression_words, cognitive_words)
def load():
  """Loads the liwc file plus the manually created depression verbs file"""
  global depression_verbs
  global depression_words
  global cognitive_words
  global depression_words_compiled
  global cognitive_words_compiled
  #Check cache first
  if os.path.exists('cache/depression_verbs.pkl') and os.path.exists('cache/depression_words.pkl'):
    depression_verbs = pickle.load(open('cache/depression_verbs.pkl'))
    depression_words = pickle.load(open('cache/depression_words.pkl'))
    cognitive_words = pickle.load(open('cache/cognitive_words.pkl'))
    depression_words_compiled = pickle.load(open('cache/depression_words_compiled.pkl'))
    cognitive_words_compiled = pickle.load(open('cache/cognitive_words_compiled.pkl'))
  else:
    #Load depression words
    (depression_words,cognitive_words) = load_liwc('project_materials/liwc/LIWC2007.dic')
    (depression_words_compiled, cognitive_words_compiled) = compile_regexes()
    #Load depression verbs
    fh = open('depression_verbs.txt')
    for line in fh:
      depression_verbs.append('^' + line.strip() + '$')
    fh.close()
    
    if not os.path.exists('cache'):
      os.makedirs('cache')
    
    fhw = open('cache/depression_words_compiled.pkl', 'wb')
    pickle.dump(depression_words_compiled, fhw)
    fhw.close()
    fhw = open('cache/cognitive_words_compiled.pkl', 'wb')
    pickle.dump(cognitive_words_compiled, fhw)
    fhw.close()
    
    #Cache depression words
    fhw = open('cache/depression_words.pkl', 'wb')
    pickle.dump(depression_words, fhw)
    fhw.close()
    
    #Cache depression verbs
    fhw = open('cache/depression_verbs.pkl', 'wb')
    pickle.dump(depression_verbs, fhw)
    fhw.close()
    
    fhw = open('cache/cognitive_words.pkl', 'wb')
    pickle.dump(cognitive_words, fhw)
    fhw.close()
