#!/usr/bin/python
import os
from subprocess import call

def run_data_through_corenlp(filelist, outputdir):
  fh = open(filelist)
  i = 0
  for line in fh:
    if i < 10:
      print "Will process %s" % (line.strip())
      i += 1
    else:
      print "  More files will be processed, but skipping the output here for your sanity...\n"
      break
  fh.close()
  if i == 0:
    #No files in list to process, don't bother calling Stanford parser
    print "No remaining files to process, done"
    return
  vendordir = 'stanford-corenlp-full-2015-01-29/'
  jars = ['stanford-corenlp-3.5.1.jar', 'stanford-corenlp-3.5.1-models.jar', 'xom.jar', 'joda-time.jar', 'jollyday.jar', 'ejml-0.23.jar']
  cp_a = [vendordir + jar for jar in jars]
  cp = ":".join(cp_a)
  basejava = ['java', '-Xmx3g', '-cp', cp, 'edu.stanford.nlp.pipeline.StanfordCoreNLP'] 
  javaargs = {}
  javaargs['props'] = ['-props', 'corenlp.properties']
  javaargs['filelist'] = ['-filelist', filelist]
  javaargs['outputdir'] = ['-outputDirectory', outputdir]
  print " ".join(basejava + javaargs['props'] + javaargs['filelist'] + javaargs['outputdir'])
  call(basejava + javaargs['props'] + javaargs['filelist'] + javaargs['outputdir'])

def process_corpus(corpusdir, corpusfilelist):
  pass
def do_reddit():
  print "PROCESSING REDDIT DATA..."
  reddit_filelist = 'reddit/filelist.txt'
  reddit_outputdir = 'reddit/depressed/'
  if os.path.exists(reddit_filelist):
    reddit_remaining_filelist = 'reddit/remain_filelist.txt'
    fh_remain_w = open(reddit_remaining_filelist, 'wb')
    fh = open(reddit_filelist)
    for filepath in fh:
      #print filepath.strip()
      if not os.path.exists(filepath.strip() + '.xml'):
        fh_remain_w.write(filepath)
    fh_remain_w.close()
    run_data_through_corenlp(reddit_remaining_filelist, reddit_outputdir)
    print "\n  COMPLETED REDDIT DATA...\n\n"
  else:
    print "Run python preprocess_data.py first before this"
    exit(1)
def do_mypersonality():
  for datatype in ['depression', 'neuroticism']:
    print "PROCESSING MYPERSONALITY %s DATA..." % (datatype.upper())
    my_dep_filelist = 'mypersonality/%s_filelist.txt' % (datatype)
    my_dep_outputdir = 'mypersonality/%s/' % (datatype)
    if os.path.exists(my_dep_filelist):
      my_dep_remaining_filelist = 'mypersonality/remain_%s_filelist.txt' % (datatype)
      fh_remain_w = open(my_dep_remaining_filelist, 'wb')
      fh = open(my_dep_filelist)
      for filepath in fh:
        processed_filepath = my_dep_outputdir + filepath.strip().split('/')[-1]
        if not os.path.exists(processed_filepath + '.xml'):
          fh_remain_w.write(filepath)
      fh_remain_w.close()
      run_data_through_corenlp(my_dep_remaining_filelist, my_dep_outputdir)
      print "\n  COMPLETED MYPERSONALITY %s DATA\n\n" % (datatype.upper())
      print "-------------------------"
    else:
      print "Run python preprocess_data.py first before this"
      exit(1)

if __name__ == '__main__':
  do_reddit()
  do_mypersonality()
