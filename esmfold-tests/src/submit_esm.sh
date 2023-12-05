#!/bin/bash

#SBATCH --partition=gpu
#SBATCH --time=72:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --ntasks=8
#SBATCH --output=output.txt
#SBATCH --error=error.txt

if [ $# -lt 2 ]; then
    echo "Usage: $0 <fasta_file_path> <output_directory>"
    exit 1
fi

# Set the TORCH_HOME environment variable
export TORCH_HOME=/share/rwmwork/nsanc/kelsey_work/run_esmfold/torch_cache

# Activate the new conda environment
# . '/toolbox/softwares/anaconda3/etc/profile.d/conda.sh'
# conda activate /toolbox/envs/esm
conda activate esmfold


# Run the Python script with the FASTA file path and output directory as arguments
python ./scripts/kakawaESM.py "$1" "$2"
