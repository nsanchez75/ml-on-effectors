from datetime import datetime
from os import makedirs, remove
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


  Input: FASTA files
  Output: PDB files of predicted protein folds in a directory
"""

def esm_curl_sequence(header: str, sequence: str, outfilepath: str)->None:
  """
  A function to run ESMFold API on a sequence.
  """

  # declare diff filenames for STDOUT and STDERR
  outfile = outfilepath + ".pdb"
  errfile = outfilepath + ".log"

  # remove the file if it already exists
  if exists(outfile):
    print(f"Warning: PDB file for {header} detected. Overwriting...")


  # run ESMFold
  print(f"Running ESMFold fold prediction on {header}...")
  with open(errfile, 'w') as ferr:
    run(f'curl -X POST --data "{sequence}" https://api.esmatlas.com/foldSequence/v1/pdb/ > {outfile} --insecure', shell=True, stderr=ferr)
  if not exists(outfile):
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
    print(f"Processing {file}...")
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
              exit(f"Error: Header {header} sequence {seq} contains a character which is not allowed.")

          # do not accept sequences greater than 400aa
          if len(seq) > 400: continue

          # print what is being analyzed
          print(f"\tAnalyzing {header}: {seq}")

          # run the curl function
          outfilepath = f"{DIR}/{header}"
          while True:
            esm_curl_sequence(header, seq, outfilepath)
            with open(outfilepath + ".pdb", 'r') as fpdb:
              if fpdb.readline().strip() != "{\"message\":\"Forbidden\"}":
                break
            # sleep for 15 minutes and try to run the curl function again
            print("Sleeping...")
            sleep(900)

          print(f"Successfully ran ESMFold fold prediction on {header}.")
