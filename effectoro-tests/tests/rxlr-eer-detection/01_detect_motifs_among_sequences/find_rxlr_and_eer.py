import os
import sys
from shutil import rmtree
import re
from time import sleep
import numpy as np
import pandas as pd
from Bio.SeqIO import parse


# RXLR strings
# RXLR_R1 = "R.LR"
# RXLR_R2 = "[RKHGQ].[LMYFIV][RNK]"
## Kyle's string searches
# RXLR_R3 = "[GHQ].LR"
# RXLR_R4 = "R.L[GKQ]"
## combining Kyle's string search ideas
# RXLR_R5 = "[RGHQ].L[RGKQ]"

RXLR_REGEXES = {
  "rxlr_strict": "R.LR", # literal motif
  "rxlr_degen_1": "[GHQ].LR", # Kyle's
  "rxlr_degen_2": "R.L[GKQ]", # Kyle's
  "rxlr_very_degen": "[RKHGQ].[LMYFIV][RNK]", # Kelsey's
}

# RXLR_REGEXES = [RXLR_R1, RXLR_R2, RXLR_R3, RXLR_R4, RXLR_R5]

# EER strings
# EER_R1 = "[ED][ED][KR]"
# EER_R2 = "[ED][KR]"

# EER_REGEXES = [EER_R1]
EER_REGEXES = {
  "eer_strict": "EER",
  "eer_degen_1": "[ED][ED][KR]",
  "eer_degen_2": "[ED][KR]",
}


def _usage_and_exit():
  print("Usage: python3 find_rxlr.py <FASTA file> [<subsequence starting index> <number of amino acids to search>]")
  exit(1)

def get_inputs()->tuple:
  if not len(sys.argv) in {2, 4}:
    _usage_and_exit()

  infile = sys.argv[1]
  if not os.path.exists(infile) or not infile[infile.rfind('.')+1:] in {"faa", "fasta"} or not os.path.getsize(infile):
    _usage_and_exit()

  # set default parameters for subseq extraction
  start_index = 19
  num_aas_searched = 60

  if len(sys.argv) == 4:
    try:
      # get input arguments
      start_index = int(sys.argv[2])
      num_aas_searched = int(sys.argv[3])

      # determine inputs are valid
      min_aas_searchable = 4
      if start_index < 0 or num_aas_searched < min_aas_searchable:
        raise Exception
    except Exception:
      _usage_and_exit()

  return infile, start_index, num_aas_searched

def find_all_matches(sequence:str, regex:str)->list:
  """
  Returns a tuple containing:
  
  - index of first occurrence of the motif
  - ordered list of matches for the motif in the provided sequence
  """

  return (
    [match.start() for match in re.compile(regex).finditer(sequence)],
    [sequence[match.start():match.end()] for match in re.compile(regex).finditer(sequence)]
  )

def construct_motif_df(seqs_info:tuple, start:int, num_aas:int)->list[list]:
  # creates a list that allows for regex key sequences to be next to regex key
  rxlr_cols = [item for pair in zip(RXLR_REGEXES.keys(), [key + "_seqs" for key in RXLR_REGEXES.keys()]) for item in pair]
  eer_cols = [item for pair in zip(EER_REGEXES.keys(), [key + "_seqs" for key in EER_REGEXES.keys()]) for item in pair]
  
  columns = ["seq_ID"] + rxlr_cols + eer_cols + ["valid_rxlr_and_eer"]

  # initialize dictionary to be converted into a dataframe
  dataset = {col: [] for col in columns}

  # analyze each provided sequences
  for i, seq_info in enumerate(seqs_info):
    # update progress bar
    bar_size = 50
    progress = (i + 1) / len(seqs_info)
    sys.stdout.write("\r[{:<50}] {:.2f}%".format("=" * int(progress * bar_size), progress * 100))
    sys.stdout.flush()

    # initialize data to be appended to dataset
    data = {col: np.nan for col in columns}

    # get sequence info
    seq_id, seq = seq_info
    data["seq_ID"] = seq_id

    # get subsequence for analysis
    end = min(start + num_aas, len(seq))
    subseq = str(seq[start:end])

    # perform RXLR analysis
    lowest_rxlr_index = np.inf
    for regex_type, regex in RXLR_REGEXES.items():
      rxlr_indices, rxlr_seqs = find_all_matches(subseq, regex)

      # list as null value if regex not found
      if not rxlr_seqs:
        data[regex_type] = 0
      # add regex data if found
      else:
        data[regex_type] = 1
        data[regex_type + "_seqs"] = rxlr_seqs

        # update lowest rxlr index if possible
        lowest_rxlr_index = min(lowest_rxlr_index, rxlr_indices[0])

    # perform EER analysis
    highest_eer_index = -np.inf
    for regex_type, regex in EER_REGEXES.items():
      eer_indices, eer_seqs = find_all_matches(subseq, regex)

      # list as null value if regex not found
      if not eer_seqs:
        data[regex_type] = 0
      # add regex data if found
      else:
        data[regex_type] = 1
        data[regex_type + "_seqs"] = eer_seqs

        # update highest eer index if possible
        highest_eer_index = max(highest_eer_index, eer_indices[-1])

    # determine if sequence contains valid combo of RXLR-EER (RXLR before EER)
    data["valid_rxlr_and_eer"] = int(lowest_rxlr_index < highest_eer_index)

    # append data to dataset
    for col in columns:
      dataset[col].append(data[col])

  # print a newline for the progress bar
  print()

  return pd.DataFrame(dataset)

def analyze_motif_df(df:pd.DataFrame, dir_path:str)->None:
  # analyze RXLR regexes
  rxlr_df = df[["seq_ID"] + RXLR_REGEXES]
  rxlr_counts = rxlr_df.count().rename(index={"seq_ID": "num_sequences"}).to_frame()
  rxlr_analysis_file = os.path.join(dir_path, "rxlr_analysis.tsv")
  rxlr_counts.to_csv(rxlr_analysis_file, sep='\t', header=False)

  # analyze EER regexes
  eer_df = df[["seq_ID"] + EER_REGEXES]
  eer_counts = eer_df.count().rename(index={"seq_ID": "num_sequences"}).to_frame()
  eer_analysis_file = os.path.join(dir_path, "eer_analysis.tsv")
  eer_counts.to_csv(eer_analysis_file, sep='\t', header=False)

  # get list of sequences that contain both RXLR and EER
  rxlr_and_eer_df = df[["seq_ID", "valid_rxlr_and_eer"]][df["valid_rxlr_and_eer"].astype(bool) == True]
  rxlr_and_eer_seqs_file = os.path.join(dir_path, "seqs_with_rxlr_and_eer.txt")
  with open(rxlr_and_eer_seqs_file, 'w') as fo:
    fo_lines = ["# sequences that contain an RXLR motif before an EER motif"] + rxlr_and_eer_df["seq_ID"].values.tolist()
    fo_lines = [line + '\n' for line in fo_lines]
    fo.writelines(fo_lines)

def main():
  # initialize arguments
  FASTA, START_INDEX, NUM_AAS_SEARCHED = get_inputs()

  # initialize results directory
  DIR = "results"
  if os.path.exists(DIR):
    print(f"Warning: {DIR} directory already exists. Overwriting content in 3 seconds...")
    sleep(3)
    rmtree(DIR)
  os.makedirs(DIR, exist_ok=False)

  # extract sequences from the FASTA file
  sequences = list()
  for seq in parse(FASTA, "fasta"):
    sequences.append((seq.id, str(seq.seq)))

  # analyze each sequence in the FASTA file
  motif_df = construct_motif_df(sequences, start=START_INDEX, num_aas=NUM_AAS_SEARCHED)

  # perform analyses
  # analyze_motif_df(motif_df, DIR)

  # write dataframe to file
  fout = os.path.join(DIR, "rxlr_eer_motifs.tsv")
  motif_df.to_csv(fout, sep='\t', na_rep='NaN', index=False)


if __name__ == "__main__":
  main()
