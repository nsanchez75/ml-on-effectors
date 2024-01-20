#!/bin/bash

module load hmmer

file=$1

hmmsearch --incT 0 --incdomT 0 --noali HMMs/WY_fold.hmm $file > temp
cat temp
short_file=$(basename $file)
grep ">> " temp | cut -f2 --delimiter=" " > WYs_${short_file}
awk '{ printf ">"; print}' WYs_${short_file} > with_carrot
mv with_carrot WYs_${short_file}

#rm WYs_${short_file}

