# cmsc773_final_project

## First, you need to parse the raw data using Stanford NLP
- Make sure to run setup.sh first (./setup.sh)
- Then python preprocess_data.py
- Then python process_data.py

## Making use of the parsed (xml) data
```python
import emotion
emotion.load() #this loads the liwc data into memory
emotion.depression_words
emotion.depression_verbs
import posts
f = posts.File('<path to file>') #This encapsulates all the sentences in a file, with functions to do stuff
f.load() #This actually loads the xml file into memory
for s in f.sentences:
  print s.verbs
```

##Doing all processing
- This method processes:
  - Gets lists of all verbs and negative verbs plus counts for each
  - Gets list of negative words plus counts for each (also captures POS via '_')
  - Counts number of past and future (modal) tense verbs
- To run:
  - python driver.py --parallel <corpus directory containing xml files>
  - --parallel param is optional
```bash
$ python driver.py --parallel <corpus directory containing xml files>
$ python driver.py #Process all corpora iteratively (will take a long time)
$ python driver.py --parallel #Process all corpora in parallel
$ python driver.py reddit/depressed #Process the reddit/depressed corpora
$ python driver.py --parallel reddit/depressed #Process the reddit/depressed corpus in parallel
```
- The parallel option will create 8 subprocesses for concurrent processing. This will saturate all cpus/cores on your laptop.

##Class structure in posts.py
- File
  - contains n sentences
  - f.sentences --> gives you a list of sentences objects
- Sentence
  - stores the data and associated functions for operating on a sentence
  - Sentence.verbs --> list of verbs
  - Sentence.tokens --> list of tokens
  - Sentence.adjs --> list of adjectives
