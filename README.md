# cmsc773_final_project

## First, you need to parse the raw data using Stanford NLP
- Make sure to run setup.sh first (./setup.sh)
- Then python preprocess_data.py
- Then python process_data.py

## Making use of the parsed (xml) data
- import emotion
- emotion.load()
-- this loads the liwc data into memory
-- emotion.depression_words
-- emotion.depression_verbs
- import posts
- f = posts.File('<path to file>')
-- This encapsulates all the sentences in a file, with functions to do stuff
- f.load()
-- This actually loads the xml file into memory

##Class structure in posts.py
- File
-- contains n sentences
-- f.sentences -> gives you a list of sentences objects
- Sentence
-- stores the data and associated functions for operating on a sentence
-- Sentence.verbs -> list of verbs
-- Sentence.tokens -> list of tokens
-- Sentence.adjs -> list of adjectives
