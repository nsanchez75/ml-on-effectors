from argparse import ArgumentParser
import subprocess
import os
import shutil

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

  # get fasta basename and categorization name
  fasta_name = fasta[fasta.rfind('/')+1:fasta.find('.')]
  category_name = hmm_path[hmm_path.rfind('/')+1:].replace(".hmm",'')

  # run hmmsearch using a provided HMM
  hmm_results = subprocess.run(args=["hmmsearch", "--incT", "0", "--incdomT", "0", "--noali", hmm_path, fasta], stdout=subprocess.PIPE).stdout.decode()
  
  # iterate through lines to extract identified classifications
  results_file = f"seq_categorization_results/{fasta_name}_{category_name}_list.txt"
  with open(results_file, 'w') as fres:
    for line in hmm_results.split('\n'):
      line = line.strip().split()
      
      if not line or not line[0]: continue
      if line[0] == ">>":
        fres.write(f"{line[1]}\n")


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

  # create/overwrite sequence categorization directory
  if os.path.exists("seq_categorization_results"):
    print("Warning: 'seq_categorization_results' directory identified. Overwriting...")
    shutil.rmtree("seq_categorization_results")
  os.makedirs("seq_categorization_results", exist_ok=False)

  # get filenames from HMM directory
  hmm_filenames = os.listdir(hmm_dir_path)
  for filename in hmm_filenames:
    if filename[-4:] == '.hmm':
      detect_categorization(input_fasta_file, f"{hmm_dir_path}/{filename}")


if __name__ == "__main__":
  main()
