#!/bin/bash

#SBATCH -J esmfold
#SBATCH -e %j.stderr.out
#SBATCH -o %j.stout.out
#SBATCH --partition=gpu
#SBATCH --time=59
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --ntasks=8

if [ $# -lt 2 ]; then
    echo "Usage: $0 <fasta_file_path> <output_directory>"
    exit 1
fi

# Set the TORCH_HOME environment variable
export TORCH_HOME=/share/siegellab/aian/scripts/torch_cache

# Activate the new conda environment
source '/toolbox/softwares/anaconda3/bin/activate'
conda activate '/toolbox/envs/esm'

# Run the Python script with the FASTA file path and output directory as arguments
time python3 kakawaESM_constructs_metadata.py -i $1 -o $2 2> time.log
