from datetime import datetime
from os import makedirs
from os.path import exists
from time import sleep
from sys import argv
from subprocess import run

"""
PROGRAM INFO:
  Description: Python script created to produce protein structure fold prediction files from all
               sequences found in a FASTA file resulting from running EffectorO. Structure prediction
               performed with the ESMFold API (https://esmatlas.com/about#api).

               (12/4/2023 update)
               This script will also wait to rerun a file if the API is no longer accepting any
               more requests.


  Input: FASTA files outputted from EffectorO
  Output: PDB files of predicted protein folds in a directory
"""

def esm_curl_sequence(header: str, sequence: str, outfilename: str)->None:
  """
  A function to run ESMFold API on a sequence.
  """

  # remove the file if it already exists
  if exists(f"predicted_esmfolds/{header}.pdb"):
    print(f"Warning: PDB file for {header} detected. Overwriting...")

  # run ESMFold
  print(f"Running ESMFold fold prediction on {header}...")
  run(f'curl -X POST --data "{sequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > predicted_esmfolds/{header}.pdb --insecure', shell=True)
  if not exists(outfilename):
    exit(f"Error: pdb file for {header} not created.")


if __name__ == "__main__":
  # check if arguments given
  if len(argv) == 1:
    exit("Error: Input of a FASTA file required.")

  # grab inputs and create the directory
  FASTA_FILES = argv[1:]

  DIR = f"predicted_esmfolds_" + datetime.now().strftime("%Y_%m_%d")
  makedirs(DIR, exist_ok=True)

  # process fasta files
  for file in FASTA_FILES:
    if not file.endswith(".fasta"):
      print(f"Error: {file} is not a FASTA file. Skipping.")
    else:
      with open(file, 'r') as infile:
        while True:
          header = infile.readline().strip()
          seq = infile.readline().strip()
          if not header or not seq: break

          # clean header
          header = header.strip().split()[0].replace('>','')
          # clean sequence
          ALLOWED_CHARS = {'G', 'Q', 'Y', 'J', 'H', 'C', 'N', 'E', 'Z', 'I', 'K', 'S', 'D', 'R', 'P', 'A', 'T', 'V', 'M', 'W', 'F', 'B', 'X', 'L'}
          seq = seq.replace('*', '')
          for c in seq:
            if c not in ALLOWED_CHARS:
              exit(f"Error: Header {header} sequence {seq} contains a {c} character which is not allowed.")

          # do not accept sequences greater than 400aa
          if len(seq) > 400: continue

          # run the curl function
          outfile = f"{DIR}/{header}.pdb"
          while True:
            esm_curl_sequence(header, seq, outfile)
            with open(outfile, 'r') as fpdb:
              if fpdb.readline() != "{\"message\":\"Forbidden\"}":
                break
            # sleep for 30 minutes and try to run the curl function again
            sleep(1800)

          print(f"Successfully ran ESMFold fold prediction on {header}.")
