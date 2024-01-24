#!/bin/bash

#SBATCH -J esmfold
#SBATCH -e %j.stderr.out
#SBATCH -o %j.stout.out
#SBATCH --partition=gpu
#SBATCH --time=72:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --ntasks=8

if [ $# -lt 2 ]; then
    echo "Usage: $0 <fasta_file_path> <output_directory>"
    exit 1
fi

# Set the TORCH_HOME environment variable
export TORCH_HOME=/share/siegellab/aian/scripts/torch_cache

# Activate the new conda environment
# source '/toolbox/softwares/anaconda3/etc/profile.d/conda.sh'
# conda activate /toolbox/envs/esm

# Run the Python script with the FASTA file path and output directory as arguments
python /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/kakawaESM_include_ptm.py "$1" "$2"
