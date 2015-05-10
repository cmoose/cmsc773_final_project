#!/bin/bash

GRAMS='bigrams'
#FILENAME=outputkldiv_${GRAMS}.txt
<<COMMENT
#echo "mypersonality_depressed " ${GRAMS} " 0-15 compared to 44-60 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed " ${GRAMS} " 0-15 compared to 44-60 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt 1 >> ${FILENAME}
echo "mypersonality_depressed " ${GRAMS} " 0-15 compared to 44-60 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt 2 my_dep_0-15_44-60_${GRAMS}.txt


#echo "mypersonality_depressed " ${GRAMS} " 0-24 compared to 31-60 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed " ${GRAMS} " 0-24 compared to 31-60 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt 1 >> ${FILENAME}
echo "mypersonality_depressed " ${GRAMS} " 0-24 compared to 31-60 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt 2 my_dep_0-24_31-60_${GRAMS}.txt

#echo "mypersonality_neurotic " ${GRAMS} " 0.0-2.25 compared to 3.05-5 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 0 >> ${FILENAME}
#echo "mypersonality_neurotic " ${GRAMS} " 0.0-2.25 compared to 3.05-5 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 1 >> ${FILENAME}
echo "mypersonality_neurotic " ${GRAMS} " 0.0-2.25 compared to 3.05-5 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 2 my_neu_0.0-2.25_3.05-5.0_${GRAMS}.txt

#echo "reddit_depressed with reddit_nondepressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "reddit_depressed with reddit_nondepressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "reddit_depressed with reddit_nondepressed " ${GRAMS} " removing 2"
python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 2 red_dep_red_nondep_${GRAMS}.txt

#echo "reddit_depressed with reddit_nondepressed_changemyview" ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_changemyview_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "reddit_depressed with reddit_nondepressed_changemyview" ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_changemyview_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "reddit_depressed with reddit_nondepressed_changemyview" ${GRAMS} " removing 2"
python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_changemyview_${GRAMS}_all.txt 2 red_dep_red_cmv_${GRAMS}.txt

#echo "reddit_depressed with reddit_nondepressed_casualconversation" ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_casualconversation_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "reddit_depressed with reddit_nondepressed_casualconversation" ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_casualconversation_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "reddit_depressed with reddit_nondepressed_casualconversation" ${GRAMS} " removing 2"
python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_casualconversation_${GRAMS}_all.txt 2 red_dep_red_casconv_${GRAMS}.txt
COMMENT
#echo "reddit_depressed with reddit_nondepressed_confession" ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_confession_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "reddit_depressed with reddit_nondepressed_confession" ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_confession_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "reddit_depressed with reddit_nondepressed_confession" ${GRAMS} " removing 2"
python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_confession_${GRAMS}_all.txt 2 red_dep_red_conf_${GRAMS}.txt
<<C2
#echo "reddit_depressed with reddit_nondepressed_self" ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_self_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "reddit_depressed with reddit_nondepressed_self" ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_self_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "reddit_depressed with reddit_nondepressed_self" ${GRAMS} " removing 2"
python findNGrams.py compare reddit/NGrams/reddit_depressed_${GRAMS}_all.txt reddit/NGrams/reddit_nondepressed_self_${GRAMS}_all.txt 2 red_dep_red_self_${GRAMS}.txt

#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 0-15 with 0.0-2.25 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 0-15 with 0.0-2.25 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt 1 >> ${FILENAME}
echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 0-15 with 0.0-2.25 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt 2 my_dep_0-15_my_neu_0-2.25_${GRAMS}.txt

#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 0-24 with 0.0-2.25 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 0-24 with 0.0-2.25 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt 1 >> ${FILENAME}
echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 0-24 with 0.0-2.25 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt 2 my_dep_0-24_my_neu_0-2.25_${GRAMS}.txt

#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 44-60 with 3.05-5 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 44-60 with 3.05-5 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 1 >> ${FILENAME}
echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 44-60 with 3.05-5 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 2 my_dep_44-60_my_neu_3.05-5.0_${GRAMS}.txt

#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 31-60 with 3.05-5 removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 31-60 with 3.05-5 removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 1 >> ${FILENAME}
echo "mypersonality_depressed with mypersonality_neurotic " ${GRAMS} " 31-60 with 3.05-5 removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt 2 my_dep_31-60_my_neu_3.05-5.0_${GRAMS}.txt

#echo "mypersonality_depressed 0-15 with reddit_depressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed 0-15 with reddit_depressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "mypersonality_depressed 0-15 with reddit_depressed " ${GRAMS} " removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-15.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 2 my_dep_0-15_red_dep_${GRAMS}.txt

#echo "mypersonality_depressed 0-24 with reddit_depressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed 0-24 with reddit_depressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "mypersonality_depressed 0-24 with reddit_depressed " ${GRAMS} " removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_0-24.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 2 my_dep_0-24_red_dep_${GRAMS}.txt

#echo "mypersonality_depressed 44-60 with reddit_nondepressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed 44-60 with reddit_nondepressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "mypersonality_depressed 44-60 with reddit_nondepressed " ${GRAMS} " removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_44-60.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 2 my_dep_44-60_red_nondep_${GRAMS}.txt

#echo "mypersonality_depressed 31-60 with reddit_nondepressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "mypersonality_depressed 31-60 with reddit_nondepressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "mypersonality_depressed 31-60 with reddit_nondepressed " ${GRAMS} " removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_depressed_${GRAMS}_31-60.txt reddit/NGrams/reddit_nondepressed_${GRAMS}_all.txt 2 my_dep_31-60_red_nondep_${GRAMS}.txt

#echo "mypersonality_neurotic 0-2.25 with reddit_depressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "mypersonality_neurotic 0-2.25 with reddit_depressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "mypersonality_neurotic 0-2.25 with reddit_depressed " ${GRAMS} " removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_0.0-2.25.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 2 my_neu_0.0-2.25_red_dep_${GRAMS}.txt

#echo "mypersonality_neurotic 3.05-5 with reddit_nondepressed " ${GRAMS} " removing 0" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 0 >> ${FILENAME}
#echo "mypersonality_neurotic 3.05-5 with reddit_nondepressed " ${GRAMS} " removing 1" >> ${FILENAME}
#python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 1 >> ${FILENAME}
echo "mypersonality_neurotic 3.05-5 with reddit_nondepressed " ${GRAMS} " removing 2"
python findNGrams.py compare mypersonality/NGrams/mypersonality_neurotic_${GRAMS}_3.05-5.0.txt reddit/NGrams/reddit_depressed_${GRAMS}_all.txt 2 my_neu_3.05-5.0_red_nondep_${GRAMS}.txt

C2
