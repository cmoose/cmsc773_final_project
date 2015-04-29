#!/bin/bash
# Use mallet to build topic models

NUM_TOPICS=10
OUTDIR="./mallet"

#Do Reddit datasets
for TYPE in depressed confession casualconversation changemyview;
  do mallet import-dir --input reddit/${TYPE}/mallet/ --output ${OUTDIR}/input-reddit-${TYPE}.mallet \
                       --keep-sequence --remove-stopwords 
done

for TYPE in depressed confession casualconversation changemyview
  do mallet train-topics --input ${OUTDIR}/input-reddit-${TYPE}.mallet --num-topics ${NUM_TOPICS} \
                         --output-state ${OUTDIR}/topic-state-reddit-${TYPE}.gz \
                         --output-topic-keys ${OUTDIR}/topic-keys-reddit-${TYPE} \
                         --output-doc-topics ${OUTDIR}/topic-docs-reddit-${TYPE} 
done


#Do mypersonality datasets

for TYPE in depression neuroticism;
  do mallet import-dir --input project_materials/mypersonality_${TYPE}/text/ --output ${OUTDIR}/input-mypersonality-${TYPE}.mallet \
                       --keep-sequence --remove-stopwords
done

for TYPE in depression neuroticism;
  do mallet train-topics --input ${OUTDIR}/input-mypersonality-${TYPE}.mallet --num-topics ${NUM_TOPICS} \
                                --output-state ${OUTDIR}/topic-state-mypersonality-${TYPE}.gz \
                                --output-topic-keys ${OUTDIR}/topic-keys-mypersonality-${TYPE} \
                                --output-doc-topics ${OUTDIR}/topic-docs-mypersonality-${TYPE}
done
