from argparse import ArgumentParser
import subprocess
import os

def detect_categorization(fasta: str, hmm_path: str):
  '''
  Input:

  - fasta :: FASTA file
  - hmm_path :: path to HMM for specified categorization

  Method:

  This function will produce a filtered FASTA file containing sequences from
  the input FASTA file that are predicted to be classified under the
  categorization associated with the input HMMs.
  '''

  hmm_results = subprocess.run(args=["hmmsearch", "--incT", '0', "--incdomT", '0', "--noali", hmm_path])
  hmm_results = hmm_results.stdout.decode()
  print(hmm_results)

def main():
  parser = ArgumentParser(prog="Identify Sequence Categorizations",
                          description="A Python script to identify and filter \
                                       a FASTA file based on its categorization \
                                       prediction via a Hidden Markov Model. \
                                       Warning: This script requires that \
                                       PyHMMR is installed.")
  parser.add_argument("--input", '-I',
                      type=str, help="Input FASTA file",
                      required=True)
  parser.add_argument("--hmm_dir", '-H',
                      type=str,
                      help="Path to directory containing category HMMs to be \
                            used (must either be absolute or relative to the \
                            current working directory)",
                      required=True)
  args = parser.parse_args()

  # declare variables
  input_fasta_file = args.input
  hmm_dir_path = args.hmm_dir

  # get filenames from HMM directory
  hmm_filenames = os.listdir(hmm_dir_path)
  for filename in hmm_filenames:
    detect_categorization(input_fasta_file, f"{hmm_dir_path}/{filename}")


if __name__ == "__main__":
  main()