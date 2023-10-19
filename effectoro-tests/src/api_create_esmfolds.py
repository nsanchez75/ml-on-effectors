import os
import sys
import subprocess

# PROGRAM INFO:
#   Description: Python script created to produce protein structure fold prediction files from all
#                sequences found in a FASTA file resulting from running EffectorO. Structure prediction
#                performed with the ESMFold API (https://esmatlas.com/about#api).
#
#   Inputs: FASTA files outputted from EffectorO
#   Outputs: PDB files of predicted protein folds in a directory


# check if arguments given
if len(sys.argv) == 1:
  exit("Error: Input of a FASTA file required.")

FASTA_FILES = sys.argv[1:]
os.makedirs("predicted_esmfolds", exist_ok=True)

# process fasta files
for file in FASTA_FILES:
  if not file.endswith(".fasta"):
    print(f"Error: {file} is not a FASTA file. Skipping.")
  else:
    with open(file, 'r') as infile:
      while True:
        header = infile.readline()
        seq = infile.readline().strip()
        if not header or not seq: break

        # clean header and sequence
        header = header.strip().split()[0].replace('>','')

        allowed_seq_chars_set = {'G', 'Q', 'Y', 'J', 'H', 'C', 'N', 'E', 'Z', 'I', 'K', 'S', 'D', 'R', 'P', 'A', 'T', 'V', 'M', 'W', 'F', 'B', 'X', 'L'}
        seq = seq.replace('*', '')
        for c in seq:
          if c not in allowed_seq_chars_set:
            exit(f"Error: Header {header} sequence {seq} contains a {c} character which is not allowed.")

        # run ESMFold
        print(f"Running ESMFold fold prediction on {header}...")
        subprocess.run(f'curl -X POST --data "{seq}" https://api.esmatlas.com/foldSequence/v1/pdb/ > predicted_esmfolds/{header}.pdb', shell=True)
        if not os.path.exists(f"predicted_esmfolds/{header}.pdb"):
          exit(f"Error: pdb file for {header} not created.")
        print(f"Successfully ran ESMFold fold prediction on {header}.")
