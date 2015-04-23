#!/usr/bin/python
# This file breaks up the data files into more meaningful chunks for
# the stanford parser.
import os
import shutil

def prepare_reddit_data():
  """Takes the depressed.txt file and breaks each post into a separate file
for later processing by Stanford's NLP toolkit.
@output creates reddit_depressed directory, file per post
  postid (and filename) is: <posting_id>_<linenum in the original depressed.txt file>
  ex. 2wotck_2.txt -> from second line of depressed.txt"""
  fh = open('project_materials/reddit/depressed.txt')
  i = 1
  outputdir = 'reddit/depressed'
  if not os.path.exists(outputdir):
    os.makedirs(outputdir)
  fhw_rejects = open('reddit/rejects.txt', 'wb')
  fhw_filelist = open('reddit/filelist.txt', 'wb')
  for line in fh:
    items = line.split('\t')
    if len(items) == 3:
      post = items[2]
      postid = items[0]
      filename = postid + "_%d" % i
      filepath = '%s/%s.txt' % (outputdir, filename)
      fhw = open(filepath, 'wb')
      fhw_filelist.write(filepath + '\n')
      fhw.write(post)
      fhw.close()
      i+=1
    else:
      fhw_rejects.write(line)

def setup_cache_dir():
  pass

def remove_duplicate_statuses():
  inputdir = 'project_materials/mypersonality_depression/text/'
  outputdir = 'project_materials/mypersonality_depression/text_deduped/'
  orig_newinputdir = 'project_materials/mypersonality_depression/text_orig/'
  if os.path.exists(orig_newinputdir):
    print "Already removed duplicates..."
    return
  if not os.path.exists(outputdir):
    os.makedirs(outputdir)
  files = [f for f in os.listdir(inputdir)]
  print "Removing duplicates..."
  for filename in files:
    fh = open(inputdir + filename)
    fhw = open(outputdir + filename, 'wb')
    firstline = fh.readline()
    fhw.write(firstline)
    for line in fh:
      if line == firstline:
        break
      fhw.write(line)
    fh.close()
    fhw.close()
  shutil.move(inputdir, orig_newinputdir) #move original files to text_orig/ subdir
  shutil.move(outputdir, inputdir) #move deduped files to text/ subdir so process_data.py will work

def prepare_mypersonality_data():
  remove_duplicate_statuses()
  for datatype in ['depression', 'neuroticism']:
    outputdir = 'mypersonality/%s/' % (datatype)
    inputdir = 'project_materials/mypersonality_%s/text/' % (datatype)
    if not os.path.exists(outputdir):
      os.makedirs(outputdir)
    files = [f for f in os.listdir(inputdir)]
    fhw = open('mypersonality/%s_filelist.txt' % (datatype), 'wb')
    for filename in files:
      fhw.write(inputdir + filename + '\n')

if __name__ == '__main__':
  prepare_mypersonality_data()
  prepare_reddit_data()

