#!/bin/bash

#Insure project materials are in dir
PROJECT_MATERIALS="project_materials"
REDDIT_DIR="reddit-control"
if [ ! -d "$PROJECT_MATERIALS" ]; then
  echo "ERROR!!"
  echo "copy and unzip the project_materials.zip file to this directory first, then rerun this"
  exit 1
fi
if [ ! -d "$REDDIT_DIR" ]; then
  echo "ERROR!!"
  echo "copy and untar the reddit-for-project.tgz file to this directory first, then rerun this"
  exit 1
fi

#Download corenlp from Stanford
STANFORD_CORENLP="stanford-corenlp-full-2015-01-29"
if [ ! -d "$STANFORD_CORENLP" ]; then
  wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip
  #unzip
  unzip stanford-corenlp-full-2015-01-29.zip
fi

