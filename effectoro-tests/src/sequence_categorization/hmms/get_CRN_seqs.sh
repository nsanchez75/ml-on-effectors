#!/bin/bash

module load hmmer

file=$1

hmmsearch --incT 0 --incdomT 0 --noali BlacSF5_CRN.hmm $file > temp
cat temp
short_file=$(basename $file)
grep ">> " temp | cut -f2 --delimiter=" " > CRNs_${short_file}
awk '{ printf ">"; print}' CRNs_${short_file} > with_carrot
mv with_carrot MU_CRNs_${short_file}

