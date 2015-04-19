#!/usr/bin/python

cat_id_map = {}
categories = {}
depression_categories = ['sad', 'anger', 'anx', 'inhib', 'death', 'negemo', 'swear']
depression_words = []
depression_verbs = []

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
      for cat_id in cats:
        categories[cat_id].add(word)
  s = set()
  for cat in depression_categories:
    s = s.union(categories[cat_id_map[cat]])
  global depression_words
  depression_words = list(s)
  print "Loaded emotion.categories and emotion.cat_id_map structures..."
def load():
  """Loads the liwc file plus the manually created depression verbs file"""
  load_liwc('project_materials/liwc/LIWC2007.dic')
  fhw = open('depression_verbs.txt')
  global depression_verbs
  for line in fhw:
    depression_verbs.append(line.strip())

