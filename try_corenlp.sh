#!/bin/bash
#Dependencies: http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip
#To visualize dep tree: http://chaoticity.com/dependensee-a-dependency-parse-visualisation-tool/

scriptdir="./stanford-corenlp-full-2015-01-29"
cp="$scriptdir/*"

#Some weird pipeline thing that is supposed to do "all" processing - produces really verbose output
#echo java -mx3g -cp \"$scriptdir/*\" edu.stanford.nlp.pipeline.StanfordCoreNLP $*
#java -mx3g -cp "$scriptdir/*" edu.stanford.nlp.pipeline.StanfordCoreNLP $*
#java -Xmx3g -cp stanford-corenlp-full-2015-01-29/stanford-corenlp-3.5.1.jar:stanford-corenlp-full-2015-01-29/stanford-corenlp-3.5.1-models.jar:stanford-corenlp-full-2015-01-29/xom.jar:stanford-corenlp-full-2015-01-29/joda-time.jar:stanford-corenlp-full-2015-01-29/jollyday.jar:stanford-corenlp-full-2015-01-29/ejml-0.23.jar edu.stanford.nlp.pipeline.StanfordCoreNLP -props corenlp.properties -filelist test_filelist.txt -outputDirectory testing -sentences

#POS tagger - tokenizes and parses
#java -mx3g -cp "$scriptdir/*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger -textFile reddit/depressed.txt -outputFormat slashTags > depressed3_pos.txt
java -mx3g -cp "$scriptdir/*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger -textFile depressed.txt -outputFormat slashTags > depressed_pos.txt

#CFG parsing - assumes POS tagged input
#java -mx1g -cp "$scriptdir/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz depressed_pos.txt > depressed_cfg.txt

#Dependency parse
java -mx3g -cp "$scriptdir/*" edu.stanford.nlp.parser.nndep.DependencyParser -model edu/stanford/nlp/models/parser/nndep/english_SD.gz -textFile depressed.txt -outFile depressed_dependency.txt

#Visualize the parse tree
#java -cp "$cp" com.chaoticity.dependensee.Main -t depressed_dependency.txt out.png

#NER
#java -cp "$cp" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier "${scriptdir}/classifiers/english.all.3class.distsim.crf.ser.gz" -textFile sentence.txt -outFile depressed_ner.txt

#java -Xmx3g -cp stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar:stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1-models.jar:stanford-corenlp-full-2014-08-27//xom.jar:stanford-corenlp-full-2014-08-27//joda-time.jar:stanford-corenlp-full-2014-08-27//jollyday.jar:stanford-corenlp-full-2014-08-27/ejml-0.23.jar edu.stanford.nlp.pipeline.StanfordCoreNLP -props /Users/chris/School/UMCP/CMSC773-S15/final_project/project_materials/corenlp-python/corenlp/default.properties -filelist /var/folders/yj/t9z4w2kd7fbcykwwpk4_hhn00000gn/T/tmpnlMdW1 -outputDirectory /var/folders/yj/t9z4w2kd7fbcykwwpk4_hhn00000gn/T/tmpw5ydeI
