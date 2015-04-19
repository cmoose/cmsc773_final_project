#!/usr/bin/python
# Simple driver module that orchestrates the loading of the xml files
# into memory using posts.py
# TODO: use pickle for serialization to disk

import os
import posts

def main():
  xmldir = 'reddit/depressed/'
  files = [f for f in os.listdir(xmldir) if f.endswith('xml')] 
  for fn in files:
    print xmldir + fn
    f = posts.File(xmldir + fn)
    f.load()

main()
