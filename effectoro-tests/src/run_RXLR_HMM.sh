#!/bin/bash

module load hmmer

for file in $(ls /share/rwmwork/mjnur/effectR/kelsey_secretomes/signalP_4.1_secretomes/cleaved_signalP_secretomes/*.fasta | sort)
do
    hmmsearch --incT 0 --incdomT 0 --noali whisson_et_al_rxlr_eer_cropped.hmm $file > temp
    short_file=$(basename $file)
    grep ">> " temp | cut -f2 --delimiter=" " > RXLR_EER_ids${short_file}
    #grep ">> " temp > WY_IDs_${short_file}
    rm temp
done

