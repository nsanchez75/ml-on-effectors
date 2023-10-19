#!/bin/bash

module load signalp/4.1c # will be run in sensitive mode (-u 0.34 and -U 0.34)

# get fasta file info
FASTA_FILE=$1
if [[ "$FASTA_FILE" =~ \.fasta$ ]]; then
  echo "$FASTA_FILE is a FASTA file. Continuing operations."
else
  echo "$FASTA_FILE is a FASTA file. Please enter a proper FASTA file."
  exit 1
fi

# run effectoro on the FASTA file (must have effectoro conda environment available)
# TODO: figure out how conda activate will work
# conda activate effectoro
## NOTE: make sure that effectoro path is correct
python3 ./effectoro_mlc/scripts/predict_effectors.py "$FASTA_FILE"
effectoro_output="predicted_effectors.fasta"

# run signalP on effectoro output
bash ./runSignalP.sh "$effectoro_output"

echo "Finished running EffectorO -> SignalP pipeline"
