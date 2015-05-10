#!/bin/bash

GRAMS='trigrams'
FILENAME=outputlda_${GRAMS}.txt

DATASET='mypersonality_depressed'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='mypersonality_neurotic'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='reddit_depressed'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='reddit_nondepressed'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='reddit_nondepressed_changemyview'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='reddit_nondepressed_casualconversation'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='reddit_nondepressed_confession'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}

DATASET='reddit_nondepressed_self'
echo ${DATASET} ${GRAMS}
python ldaTopicModeling.py ${DATASET} ${GRAMS}
