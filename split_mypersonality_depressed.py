#!/usr/bin/python

import csv

scores = {}

def load_scores():
  """Load userscores from csv"""
  global scores
  if not scores:
    fh = open('project_materials/mypersonality_depression/939_userScores.csv')
    fh.readline()
    csvreader = csv.reader(fh)
    for line in csvreader:
      _id = line[0]
      score = line[2]
      scores[_id] = score

def bin_data():
  """Bin data into two groups, top third and bottom third of scores"""
  global scores
  a = scores.values()
  a.sort()
  _range = len(a)/3
  low = _range
  high = len(a) - _range
  low_score = a[low]
  high_score = a[high]
  non_depressed = []
  depressed = []
  for _id,score in scores.items():
    if int(score) <= 24:
      non_depressed.append(_id)
    if int(score) >= 31:
      depressed.append(_id)
  return (non_depressed, depressed)
  
def split_groups():
  load_scores()
  return bin_data()
  

