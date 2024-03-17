from argparse import ArgumentParser
from time import sleep
from shutil import rmtree
import os
import pandas as pd

# INFO:
#   - inputs:
#       - input table that identifies ORFs w/ best AF-uniprot ID hit
#       - 1/more inputs describing what ORF classification exists via this format: [name of column] [input file]
#           - examples for what this input file can be are: WY ORFs, >= 0.85 predicted effectors, RXLR ORFs, etc.
#           - note: these input files should just be lists of what ORF sequence names apply to the given classification
#   - output: TSV file containing:
#       - ORF ID
#       - (0/1) values of whether or not each uniprot ID can be associated to the ORF classifications
#       - EffectorO score
#       - best hit AF-uniprot ID
#       - BLASTp information between AF-uniprot ID and ORF ID
#       - summary log for all combinations of headers (TODO: fix)

def main():
  parser = ArgumentParser(prog="Create ORF ID Table",
                                   description="A script to produce a table with ORF IDs and all analyses associated with them")
  parser.add_argument('-i', '--input', type=str, required=True, help="BLASTp result of best-fit ORF IDs to AF-uniprot IDs")
  parser.add_argument('-l', '--listsdir', type=str, required=True, help="Directory containing files of lists of sequence IDs associated with a classification. Field names are denoted in the list files at the beginning with '#'")
  parser.add_argument('-o', '--outdir', type=str, help="Directory to send results to", default="ORF_ID_table_creation_results")
  args = parser.parse_args()
  INPUT_FILE:str         = args.input
  INPUT_DIR_OF_LIST_FILES:str = args.listsdir
  OUTPUT_DIR:str         = args.outdir

  # check arguments
  if not os.path.exists(INPUT_FILE):
    print(f"Error: File {INPUT_FILE} does not exist.")
    exit(1)
  if not os.path.exists(INPUT_DIR_OF_LIST_FILES):
    print(f"Error: directory {INPUT_DIR_OF_LIST_FILES} does not exist.")
    exit(1)
  if os.path.exists(OUTPUT_DIR):
    print(f"Warning: directory {OUTPUT_DIR} detected. Removing its contents in 3 seconds...")
    sleep(3)
    rmtree(OUTPUT_DIR)
  os.makedirs(OUTPUT_DIR, exist_ok=False)

  print("Constructing the ORF table...")
  ORF_TABLE = (pd.read_csv(INPUT_FILE, sep='\t')).rename(columns={"qseqid": "best_blast_hit_AF_ID", "sseqid": "ORF_seq_ID"})
  LIST_FILES = os.listdir(INPUT_DIR_OF_LIST_FILES)

  # determine if ORF IDs are present in classification files
  headers = list()
  for file in LIST_FILES:
    with open(f"{INPUT_DIR_OF_LIST_FILES}/{file}", 'r') as fclass:
      # get header
      header = fclass.readline()
      if not header.startswith('#'):
        exit(f"An error occurred: Header not specified in {fclass.name}.")
      header = header.removeprefix("#").strip()
      headers.append(header)

      # add to table binary values of whether tabulated ORF sequence IDs are found in the file
      valid_ORFs = set(line.strip() for line in fclass)
      ORF_TABLE[header] = ORF_TABLE["ORF_seq_ID"].astype(str).isin(valid_ORFs).astype(int)

  # define output file name template
  out_filename = f"{args.input.split('.')[0]}_on_{'_'.join(headers)}"

  # create table file
  out_filename_table = f"{OUTPUT_DIR}/{out_filename}.tsv"
  if os.path.exists(out_filename_table):
    print(f"File {out_filename_table} detected. Overwriting...")
    os.remove(out_filename_table)
  ORF_TABLE.to_csv(out_filename_table, sep='\t', index=False)
  print("Done!")


if __name__ == "__main__":
  main()