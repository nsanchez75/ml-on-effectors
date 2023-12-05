import pandas as pd
from functools import reduce
from itertools import combinations
import re
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
ORF_TABLE = pd.read_csv(INFILE, sep='\t')
HEADERS_INDEX_START = ORF_TABLE.columns.get_loc("qcovs") + 1

# get list of headers not including SP
HEADER_LIST_WO_SP = list(ORF_TABLE.columns[HEADERS_INDEX_START:]).remove("SP")

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
        for header in HEADER_LIST_WO_SP:
            # declare common counts
            HEADER_COUNT_CONDITION = (df[header].astype(int) == 1)
            HEADER_COUNT = df[HEADER_COUNT_CONDITION]

            # write header count to file
            flog_lines.append(f"{header}: {HEADER_COUNT}\n")

            # match header to specified/general case and provide more statistics if necessary
            match header:
                case "WY-domain":
                    # count number including RXLR-EER
                    if "RXLR-EER" in HEADER_LIST_WO_SP:
                        wy__rxlr_eer__count = len(df[HEADER_COUNT_CONDITION & df["RXLR-EER"].astype(int) == 1])
                        flog_lines.append(f"\t\twith RXLR-EER: {wy__rxlr_eer__count}\n")
                    # shouldn't have CRN
                    if "CRN-motif" in HEADER_LIST_WO_SP:
                        if len(df[HEADER_COUNT_CONDITION & df["CRN-motif"].astype(int) == 1]):
                            raise ValueError("One/more sequences with WY-Domain also has CRN-motif. This shouldn't happen.")
                case "CRN-motif":
                    # shouldn't have WY or RXLR-EER
                    if all(i in HEADER_LIST_WO_SP for i in ["WY-domain", "RXLR-EER"]):
                        if len(df[HEADER_COUNT_CONDITION & df["WY-domain"].astype(int) == 1 & df["RXLR-EER"].astype(int) == 1]):
                            raise ValueError("One/more sequences with CRN-motif has either WY-domain, RXLR-EER, or both. This shouldn't happen.")
                case "RXLR-EER":
                    if "WY-domain" in HEADER_LIST_WO_SP:
                        rxlr_eer__wy__count = len(df[HEADER_COUNT_CONDITION & df["RXLR-EER"].astype(int) == 1])
                        flog_lines.append(f"\t\twith WY-domain: {rxlr_eer__wy__count}")
                    # shouldn't have CRN
                    if "CRN-motif" in HEADER_LIST_WO_SP:
                        if len(df[HEADER_COUNT_CONDITION & df["CRN-motif"].astype(int) == 1]):
                            raise ValueError("One/more sequences with RXLR-EER also has CRN-motif. This shouldn't happen.")
                case match_result if (match_result := re.match("predicted-effectors*", header)):
                    efo_wo_motifs = len(df[HEADER_COUNT_CONDITION] & ~reduce(lambda x, y: (x | y), make_conditional_identifier(df, False, {s for s in HEADER_LIST_WO_SP if (re.match("predicted-effectors*", s))}))) # excludes matches with other motifs as well
                    flog_lines[-1] = f"\t{header}: {efo_wo_motifs}" # replace efo's initial header string with this one
    except ValueError as e:
        print(f"An error occurred: {e}")
        exit(1)


# begin summary analysis
print("Creating summary table ...")

# analyze non-SP
## non-SP header
flog_lines.append("Non-Secreted (no SP):")
## create non-SP table
NON_SP_TABLE = ORF_TABLE[ORF_TABLE["SP"].astype(int) == 0].drop(columns=["SP"], inplace=False)
## count known non-effectors (no other headers)
non_sp_non_effector_count = len(NON_SP_TABLE[~reduce(lambda x, y: (x | y), make_conditional_identifier(NON_SP_TABLE, False))])
flog_lines.append(f"\tPredicted non-effectors: {non_sp_non_effector_count}\n")
## count and display header statistics
find_header_statistics(NON_SP_TABLE)
## count total non-SP
flog_lines.append(f"\tTotal Non-Secreted: {len(NON_SP_TABLE)}\n") # account for line in between non-SP and SP

# NON_SP_PREDICTED_NON_EFFECTOR = len(non_sp_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(non_sp_table, False))])
# NON_SP_PREDICTED_EFFECTOR = len(non_sp_table[non_sp_table["predicted-effectors-ov-85"].astype(int) == 1])   # TODO: make the predicted-effectors be more generalized if needed
# NON_SP_COUNT = len(non_sp_table)


# analyze SP
## sp header
flog_lines.append("Secreted (SP):")
## create SP table
SP_TABLE = ORF_TABLE[ORF_TABLE["SP"].astype(int) == 1].drop(columns=["SP"], inplace=False)
## count known non-effectors (no other headers)
sp_non_effector_count = len(SP_TABLE[~reduce(lambda x, y: (x | y), make_conditional_identifier(NON_SP_TABLE, True))])
flog_lines.append(f"\tPredicted non-effectors: {sp_non_effector_count}")
## count and display header statistics
find_header_statistics(SP_TABLE)
## count total SP
flog_lines.append(f"\tTotal Secreted: {len(SP_TABLE)}\n") # account for line between SP and Total

## get number of SP
# sp_table = ORF_TABLE[ORF_TABLE["SP"].astype(int) == 1].drop(columns=["SP"], inplace=False)
# SP_PREDICTED_NON_EFFECTOR = len(sp_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(sp_table, False))])
# ### get data on known effectors
# sp_predicted_effector_dict = dict()
# for header in sp_table.columns[HEADERS_INDEX_START:]:
#     # count header count
#     sp_header_table = sp_table[sp_table[header].astype(int) == 1]
#     HEADER_COUNT = len(sp_header_table)
    
#     # count of combinations including header in parentheses
#     header_combos_counts = list()   # [((WY, RXLR-EER), <count>), ..., ((WY, CRN, EfO, RXLR-EER), <count>)]
#     sp_table_without_header = sp_header_table[HEADERS_INDEX_START:].drop(columns=[header], inplace=False)
#     for r in range(1, len(sp_table_without_header.columns[HEADERS_INDEX_START:]) + 1):
#         combo_list = list(combinations(sp_table_without_header.columns[HEADERS_INDEX_START:], r))
#         for combo in combo_list:
#             combo_count = len(sp_header_table[reduce(lambda x, y: (x & y), make_conditional_identifier(sp_header_table, True, combo))])
#             # print(f"{header} + {combo}: {combo_count}") # TODO: delete later
#             if combo_count != 0: header_combos_counts.append((combo, combo_count))

#     # HEADER_ONLY_COUNT = len(sp_header_table[~reduce(lambda x, y: (x | y), make_conditional_identifier(sp_header_table, False, {header}))])
#     # add header statistics to dictionary
#     sp_predicted_effector_dict[header] = (HEADER_COUNT, header_combos_counts)
# SP_COUNT = len(sp_table)


# get total
flog_lines.append(f"Total: {len(ORF_TABLE)}")
# total = len(ORF_TABLE)

## create summary log
summary_log_file = f"{infile_no_extensions}.summary.log"
if os.path.exists(summary_log_file):
    print(f"Warning: {summary_log_file} detected. Overwriting...")
    os.remove(summary_log_file)
with open(summary_log_file, 'w') as flog: flog.writelines(flog_lines)

# ## create summary log
# summary_log_file = f"{infile_no_extensions}.summary.log"
# if os.path.exists(summary_log_file):
#     print(f"Warning: {summary_log_file} detected. Overwriting...")
#     os.remove(summary_log_file)
# with open(summary_log_file, 'w') as flog:
#     flog.write( "Non-Secreted (No Signal-P):\n" +
#                f"\tPredicted Non-Effectors: {NON_SP_PREDICTED_NON_EFFECTOR}\n" +
#                f"\tPredicted Effectors: {NON_SP_PREDICTED_EFFECTOR}\n" +
#                 "Secreted (Signal-P):\n" +
#                f"\tPredicted Non-Effectors: {SP_PREDICTED_NON_EFFECTOR}\n"
#                )
#     for header, header_stats in sp_predicted_effector_dict.items():
#         HEADER_COUNT, COMBO_STATS = header_stats
#         flog.write(f"\t{header}: {HEADER_COUNT}")
#         combo_stats = list()
#         for COMBO_HEADERS, COMBO_COUNT in COMBO_STATS:
#             if COMBO_COUNT != 0: combo_stats.append(f"{' and '.join(COMBO_HEADERS)}: {COMBO_COUNT}")
#         if combo_stats: flog.write(f" ({', '.join(combo_stats)})\n")

#     flog.write(f"\nTotal: {total}\n")

## print warning to manually update summary log for context
print("Warning: Make sure to manually add context (especially for undefined headers) " +
      "since statistics may not match the total.")
