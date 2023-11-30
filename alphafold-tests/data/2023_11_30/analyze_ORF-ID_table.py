import pandas as pd
from functools import reduce
from itertools import combinations
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
HEADERS_INDEX_START = orf_table.columns.get_loc("qcovs") + 1


# function to produce a conditional identifier (helpful identifying known [non-]effectors)
def make_conditional_identifier(df: pd.DataFrame, include: bool, headers:set={})->list:
    known_effector_conditions = list()
    for header in df.columns[HEADERS_INDEX_START:]:
        if ((header in headers) if include else (header not in headers)):
            known_effector_conditions.append(df[header].astype(int) == 1)
    return known_effector_conditions


# perform analysis
print("Creating summary table ...")

## analyze non-SP
non_sp_table = orf_table[orf_table["SP"].astype(int) == 0].drop(columns=["SP"], inplace=False)
NON_SP_PREDICTED_NON_EFFECTOR = len(non_sp_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(non_sp_table, False))])
NON_SP_PREDICTED_EFFECTOR = len(non_sp_table[non_sp_table["predicted-effectors-ov-85"].astype(int) == 1])   # TODO: make the predicted-effectors be more generalized if needed

## get number of SP
sp_table = orf_table[orf_table["SP"].astype(int) == 1].drop(columns=["SP"], inplace=False)
SP_PREDICTED_NON_EFFECTOR = len(sp_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(sp_table, False))])
### get data on known effectors
sp_predicted_effector_dict = dict()
for header in sp_table.columns[HEADERS_INDEX_START:]:
    # count header count
    sp_header_table = sp_table[sp_table[header].astype(int) == 1]
    HEADER_COUNT = len(sp_header_table)
    
    # count of combinations including header in parentheses
    header_combos_counts = list()   # [((WY, RXLR-EER), <count>), ..., ((WY, CRN, EfO, RXLR-EER), <count>)]
    sp_table_without_header = sp_header_table[HEADERS_INDEX_START:].drop(columns=[header], inplace=False)
    for r in range(1, len(sp_table_without_header.columns[HEADERS_INDEX_START:]) + 1):
        combo_list = list(combinations(sp_table_without_header.columns[HEADERS_INDEX_START:], r))
        for combo in combo_list:
            combo_count = len(sp_header_table[reduce(lambda x, y: (x & y), make_conditional_identifier(sp_header_table, True, combo))])
            # print(f"{header} + {combo}: {combo_count}") # TODO: delete later
            if combo_count != 0: header_combos_counts.append((combo, combo_count))

    # HEADER_ONLY_COUNT = len(sp_header_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(sp_header_table, False, {header}))])
    # add header statistics to dictionary
    sp_predicted_effector_dict[header] = (HEADER_COUNT, header_combos_counts)

## get total
total = len(orf_table)

## create summary log
summary_log_file = f"{infile_no_extensions}.summary.log"
if os.path.exists(summary_log_file):
    print(f"Warning: {summary_log_file} detected. Overwriting...")
    os.remove(summary_log_file)
with open(summary_log_file, 'w') as flog:
    flog.write( "Non-Secreted (No Signal-P):\n" +
               f"\tPredicted Non-Effectors: {NON_SP_PREDICTED_NON_EFFECTOR}\n" +
               f"\tPredicted Effectors: {NON_SP_PREDICTED_EFFECTOR}\n" +
                "Secreted (Signal-P):\n" +
               f"\tPredicted Non-Effectors: {SP_PREDICTED_NON_EFFECTOR}\n"
               )
    for header, header_stats in sp_predicted_effector_dict.items():
        HEADER_COUNT, COMBO_STATS = header_stats
        flog.write(f"\t{header}: {HEADER_COUNT}")
        combo_stats = list()
        for COMBO_HEADERS, COMBO_COUNT in COMBO_STATS:
            if COMBO_COUNT != 0: combo_stats.append(f"{' and '.join(COMBO_HEADERS)}: {COMBO_COUNT}")
        if combo_stats: flog.write(f" ({', '.join(combo_stats)})\n")

    flog.write(f"\nTotal: {total}\n")

## print warning to manually update summary log for context
print("Warning: Make sure to manually add context since statistics may not match the total.")
