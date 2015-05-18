#!/bin/bash

#DATASET='mypersonality'
#FEAT='neg_nouns'
OUTFILE='output_svm_reddit_part.txt'


#finished 'unigrams' 'bigrams' 'trigrams' 'neg_verbs' 'neg_nouns' 'neg_adjs' 'neg_advs' 'all_verbs' 'cog_verbs'
DATASET='reddit'
SET1='depressed'
for FEAT in '[cog_verbs,cog_adjs]'
do
    echo '**********************' ${FEAT} '************************'
    for SET2 in 'self' 'changemyview' 'casualconversation' 'confession'
    do
        TRAINSET='[0,1,2,3]'
        TESTSET='4'
        echo ${DATASET} ${FEAT} ${SET1} ${SET2} ${TRAINSET} ${TESTSET}  >> ${OUTFILE}
        python classifier.py ${DATASET} ${FEAT} ${TRAINSET} ${TESTSET} svm ${SET1} ${SET2} >> ${OUTFILE}
        echo '----------------------------------------------' >> ${OUTFILE}

        TRAINSET='[0,1,2,4]'
        TESTSET='3'
        echo ${DATASET} ${FEAT} ${SET1} ${SET2} ${TRAINSET} ${TESTSET}  >> ${OUTFILE}
        python classifier.py ${DATASET} ${FEAT} ${TRAINSET} ${TESTSET} svm ${SET1} ${SET2} >> ${OUTFILE}
        echo '----------------------------------------------' >> ${OUTFILE}

        TRAINSET='[0,1,3,4]'
        TESTSET='2'
        echo ${DATASET} ${FEAT} ${SET1} ${SET2} ${TRAINSET} ${TESTSET}  >> ${OUTFILE}
        python classifier.py ${DATASET} ${FEAT} ${TRAINSET} ${TESTSET} svm ${SET1} ${SET2} >> ${OUTFILE}
        echo '----------------------------------------------' >> ${OUTFILE}

        TRAINSET='[0,2,3,4]'
        TESTSET='1'
        echo ${DATASET} ${FEAT} ${SET1} ${SET2} ${TRAINSET} ${TESTSET}  >> ${OUTFILE}
        python classifier.py ${DATASET} ${FEAT} ${TRAINSET} ${TESTSET} svm ${SET1} ${SET2} >> ${OUTFILE}
        echo '----------------------------------------------' >> ${OUTFILE}

        TRAINSET='[1,2,3,4]'
        TESTSET='0'
        echo ${DATASET} ${FEAT} ${SET1} ${SET2} ${TRAINSET} ${TESTSET}  >> ${OUTFILE}
        python classifier.py ${DATASET} ${FEAT} ${TRAINSET} ${TESTSET} svm ${SET1} ${SET2} >> ${OUTFILE}
        echo '**********************************************' >> ${OUTFILE} 

    done
done


