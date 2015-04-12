#!/bin/bash

#Insure project materials are in dir
PROJECT_MATERIALS="project_materials"
if [ ! -d "$PROJECT_MATERIALS" ]; then
  echo "ERROR!!"
  echo "copy and unzip the project_materials.zip file to this directory first, then rerun this"
  exit 1
fi

#Download corenlp from Stanford
STANFORD_CORENLP="stanford-corenlp-full-2015-01-29"
if [ ! -d "$STANFORD_CORENLP" ]; then
  wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip
  #unzip
  unzip stanford-corenlp-full-2015-01-29.zip
fi

