import pandas as pd
from functools import reduce
import os
import sys

# check if input argument is correct
INFILE = sys.argv[1]
if not os.path.exists(INFILE):
    exit(f"Error: {INFILE} does not exist.")
if not INFILE.endswith(".tsv"):
    exit(f"Error: {INFILE} does not appear to be a tsv file.")

# remove extensions from input file (WARNING: removes everything behind first '.')
infile_no_extensions = INFILE[:INFILE.find('.')]

# get ORF table
orf_table = pd.read_csv(INFILE, sep='\t')
HEADERS_INDEX_START = 13


# function to produce a conditional identifier (helpful identifying known [non-]effectors)
def make_conditional_identifier(df: pd.DataFrame, include: bool, headers:set)->list:
    known_effector_conditions = list()
    for header in df.columns[HEADERS_INDEX_START:]:
        if ((header in headers) if include else (header not in headers)):
            known_effector_conditions.append(df[header].astype(int) == 1)
    return known_effector_conditions


# perform analysis
print("Creating summary table ...")

## analyze non-SP
non_sp_table = orf_table[orf_table["SP"].astype(int) == 0]
NON_SP_PREDICTED_NON_EFFECTOR = len(non_sp_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(non_sp_table, False, {"SP"}))])
NON_SP_PREDICTED_EFFECTOR = len(non_sp_table[non_sp_table["predicted-effectors-ov-85"].astype(int) == 1])   # TODO: make the predicted-effectors be more generalized if needed

## get number of SP
sp_table = orf_table[orf_table["SP"].astype(int) == 1]
SP_PREDICTED_NON_EFFECTOR = len(sp_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(sp_table, False, {"SP"}))])
### get data on known effectors
sp_predicted_effector_dict = dict()
for header in sp_table.columns[HEADERS_INDEX_START:]:
    if header == "SP": continue
    else: sp_predicted_effector_dict[header] = len(sp_table[sp_table[header].astype(int) == 1])

## get total
total = len(orf_table)

## create summary log
summary_log_file = f"{infile_no_extensions}.summary.log"
if os.path.exists(summary_log_file):
    print(f"Warning: {summary_log_file} detected. Overwriting...")
    os.remove(summary_log_file)
with open(summary_log_file, 'w') as flog:
    flog.write( "No SP:\n" +
               f"\tPredicted Non-Effectors: {NON_SP_PREDICTED_NON_EFFECTOR}\n" +
               f"\tPredicted Effectors: {NON_SP_PREDICTED_EFFECTOR}\n" +
                "SP:\n" +
               f"\tPredicted Non-Effectors: {SP_PREDICTED_NON_EFFECTOR}\n"
               )
    for header, count in sp_predicted_effector_dict.items():
        flog.write(f"\t{header}: {count}\n")
    flog.write(f"\nTotal: {total}\n")
