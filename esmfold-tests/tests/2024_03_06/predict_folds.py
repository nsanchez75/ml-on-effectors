import torch
import esm
import os
import sys

# PROGRAM INFO:
#
#
#   original code structure found in ESM github: https://github.com/facebookresearch/esm

model = esm.pretrained.esmfold_v1()
model = model.eval()

# Optionally, uncomment to set a chunk size for axial attention. This can help reduce memory.
# Lower sizes will have lower memory requirements at the cost of increased speed.
# model.set_chunk_size(128)

# check if arguments given
if len(sys.argv) == 1:
  exit("Error: Input of a FASTA file required.")

FASTA_FILES = sys.argv[1:]
os.makedirs("predicted_esmfolds", exist_ok=True)

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
           if c not in allowed_seq_chars_set: exit(f"Error: forbidden character '{c}' found in {header}.")

        with torch.no_grad():
            output = model.infer_pdb(seq)

        with open(f"predicted_esmfolds/{header}.pdb", "w") as f:
            f.write(output)
