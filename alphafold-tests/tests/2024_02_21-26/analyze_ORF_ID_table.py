from argparse import ArgumentParser
import os
import sys
from shutil import rmtree
from time import sleep
import re
from functools import reduce
import pandas as pd

"""
Note: As of now only the following classifications are supported:
- WY-domain
- CRN-motif
- RXLR-EER
- EffectorO-predicted effectors (with probability bounds)")
  parser.add_argument()
"""

def main():
  parser = ArgumentParser(prog="ORF ID Table Analyzer", description="This is a Python script that performs an analysis on an ORF ID table.") 
  parser.add_argument("-i", "--input_file", type=str, required=True, help="Input ORF table TSV file")
  parser.add_argument("-o", "--output_dir", type=str, required=False, help="Directory where results will be placed", default="ORF_ID_table_analysis_results")
  args = parser.parse_args()
  INFILE:str = args.input_file
  OUTDIR:str = args.output_dir

  # check if input arguments are correct
  ## TSV file
  if not os.path.exists(INFILE):
    exit(f"Error: {INFILE} does not exist.")
  if not INFILE.endswith(".tsv"):
    exit(f"Error: {INFILE} does not appear to be a tsv file.")
  ## output directory
  if os.path.exists(OUTDIR):
    print(f"Warning: directory '{OUTDIR}' already detected. Removing its contents in 3 seconds...")
    sleep(3)
    rmtree(OUTDIR)
  os.makedirs(OUTDIR, exist_ok=False)

  # remove extensions from input file (WARNING: removes everything behind first '.')
  infilename_no_extensions = INFILE[INFILE.rfind('/')+1:INFILE.find('.')]

  # get ORF table
  ORF_TABLE = pd.read_csv(INFILE, sep='\t')
  HEADERS_INDEX_START = ORF_TABLE.columns.get_loc("qcovs") + 1

  # get list of headers not including SP
  HEADERS_WO_SP = ORF_TABLE.columns[HEADERS_INDEX_START:].tolist()
  HEADERS_WO_SP.remove("SP")

  # declare list that stores strings to be written to summary log file
  flog_lines = list()

  # declare functions
  def make_conditional_identifier(df: pd.DataFrame, include: bool, headers: set={})->list:
    """
    Used to identify specific headers.

    If `include` parameter is:
      - True: detect for defined headers
      - False: detect for headers that are not defined
    
    Returns a conditional used for dataframes
    """
    known_effector_conditions = list()
    for header in df.columns[HEADERS_INDEX_START:]:
      if ((header in headers) if include else (header not in headers)):
        known_effector_conditions.append(df[header].astype(int) == 1)
    return known_effector_conditions

  def find_header_statistics(df: pd.DataFrame)->None:
    """
    Used to determine statistics of both defined and undefined headers

    Defined Headers (exact spelling and capitalization required):
      - WY-domain
      - CRN-motif
      - RXLR-EER
      - predicted-effectors*

    Deals with appending new lines to defined `flog_lines`
    """
    try:
      for header in HEADERS_WO_SP:
        # declare common counts
        HEADER_COUNT_CONDITION = df[header].astype(int) == 1
        HEADER_COUNT = len(df[HEADER_COUNT_CONDITION])

        # write header count to file
        flog_lines.append(f"\t{header}: {HEADER_COUNT}\n")

        # match header to specified/general case and provide more statistics if necessary
        match header:
          case "WY-domain":
            # count number including RXLR-EER
            if "RXLR-EER" in HEADERS_WO_SP:
                wy__rxlr_eer__count = len(df[(HEADER_COUNT_CONDITION) & (df["RXLR-EER"].astype(int) == 1)])
                flog_lines.append(f"\t\twith RXLR-EER: {wy__rxlr_eer__count}\n")
            # shouldn't have CRN
            if "CRN-motif" in HEADERS_WO_SP:
              if len(df[(HEADER_COUNT_CONDITION) & (df["CRN-motif"].astype(int) == 1)]):
                raise ValueError("One/more sequences with WY-domain also has CRN-motif. This shouldn't happen.")
          case "CRN-motif":
            # shouldn't have WY or RXLR-EER
            if all(i in HEADERS_WO_SP for i in ["WY-domain", "RXLR-EER"]):
              if len(df[(HEADER_COUNT_CONDITION) & (df["WY-domain"].astype(int) == 1) & (df["RXLR-EER"].astype(int) == 1)]):
                raise ValueError("One/more sequences with CRN-motif has either WY-domain, RXLR-EER, or both. This shouldn't happen.")
          case "RXLR-EER":
            if "WY-domain" in HEADERS_WO_SP:
              rxlr_eer__wy__count = len(df[(HEADER_COUNT_CONDITION) & (df["WY-domain"].astype(int) == 1)])
              flog_lines.append(f"\t\twith WY-domain: {rxlr_eer__wy__count}\n")
            # shouldn't have CRN
            if "CRN-motif" in HEADERS_WO_SP:
              if len(df[HEADER_COUNT_CONDITION & df["CRN-motif"].astype(int) == 1]):
                raise ValueError("One/more sequences with RXLR-EER also has CRN-motif. This shouldn't happen.")
          case match_result if (match_result := re.match("predicted-effectors*", header)):
            # TODO: 2/21/2024
            flog_lines.pop()
            efo = len(df[HEADER_COUNT_CONDITION & ~reduce(lambda x, y: (x | y), make_conditional_identifier(df, False, {s for s in HEADERS_WO_SP if (re.match("predicted-effectors*", s))}))]) # excludes matches with other motifs as well
            flog_lines.append(f"\t{header}: {efo}\n")
    except ValueError as e:
      print(f"An error occurred: {e}")
      exit(1)


  # begin summary analysis
  print("Creating summary table ...")

  # analyze non-SP
  ## non-SP header
  flog_lines.append("Non-Secreted (no SP):\n")
  ## create non-SP table
  NON_SP_TABLE = ORF_TABLE[ORF_TABLE["SP"].astype(int) == 0].drop(columns=["SP"], inplace=False)
  ## count known non-effectors (no other headers)
  non_sp_non_effector_count = len(NON_SP_TABLE[~reduce(lambda x, y: (x | y), make_conditional_identifier(NON_SP_TABLE, False))])
  flog_lines.append(f"\tPredicted non-effectors: {non_sp_non_effector_count}\n")
  ## count and display header statistics
  find_header_statistics(NON_SP_TABLE)
  ## count total non-SP
  flog_lines.append(f"\tTotal Non-Secreted: {len(NON_SP_TABLE)}\n") # account for line in between non-SP and SP

  # analyze SP
  ## sp header
  flog_lines.append("Secreted (SP):\n")
  ## create SP table
  SP_TABLE = ORF_TABLE[ORF_TABLE["SP"].astype(int) == 1].drop(columns=["SP"], inplace=False)
  ## count known non-effectors (no other headers)
  sp_non_effector_count = len(SP_TABLE[~reduce(lambda x, y: (x | y), make_conditional_identifier(SP_TABLE, False))])
  flog_lines.append(f"\tPredicted non-effectors: {sp_non_effector_count}\n")
  ## count and display header statistics
  find_header_statistics(SP_TABLE)
  ## count total SP
  flog_lines.append(f"\tTotal Secreted: {len(SP_TABLE)}\n") # account for line between SP and Total

  # get total
  flog_lines.append(f"Total: {len(ORF_TABLE)}")

  ## create summary log
  summary_log_file = f"{OUTDIR}/{infilename_no_extensions}.summary.log"
  if os.path.exists(summary_log_file):
    print(f"Warning: {summary_log_file} detected. Overwriting...")
    os.remove(summary_log_file)
  with open(summary_log_file, 'w') as flog: flog.writelines(flog_lines)

  print("Done!")

  ## print warning to manually update summary log for context
  print("Warning: Make sure to validate (especially for unsupported headers) " +
        "in case statistics may not match the total.")


if __name__ == "__main__":
  main()