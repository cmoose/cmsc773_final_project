#!/usr/bin/python
# Class to manage a corpus
# Not really used at this point
import emotion
import posts
import os
import pickle

class Corpus():
  def __init__(self, xmldir):
    self.xmldir = xmldir
    self.filelist = []
    self.fileobjs = []
  def load(self):
    emotion.load() #This insures the liwc data for verb and adj filtering is loaded
    files = [f for f in os.listdir(self.xmldir) if f.endswith('pkl')]
    files = files[0:5]
    self.filelist = files
    cachedir = self.xmldir
    #cachedir = self.xmldir + 'cache/'
    
    for fn in files:
      if not os.path.exists(cachedir):
        os.makedirs(cachedir)
      
      #if os.path.exists(cachedir + fn + '.pkl'):
      if os.path.exists(cachedir + fn):
        print "Loading File data %s from cache..." % (cachedir + fn + '.pkl')
        #f = pickle.load(open(cachedir + fn + '.pkl'))
        f = pickle.load(open(cachedir + fn))
      else:
        f = posts.File(self.xmldir + fn)
        f.load()
        pickle.dump(f,open(cachedir + fn + '.pkl', 'wb'))
      self.fileobjs.append(f)
  def what_we_want_to_count(self):
    pass
