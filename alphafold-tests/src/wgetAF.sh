#!/bin/bash

file=$1

while read -r line
do
  wget  "https://alphafold.ebi.ac.uk/files/"$line"-model_v4.pdb"
done <$file

