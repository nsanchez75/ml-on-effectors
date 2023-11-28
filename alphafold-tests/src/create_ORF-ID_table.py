import argparse
from functools import reduce
from itertools import combinations
import pandas as pd
import os

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
#       - summary log for all combinations of headers

# argument parser
parser = argparse.ArgumentParser(prog="Create ORF ID Table",
                                 description="A script to produce a table with ORF IDs and all analyses associated with them")
parser.add_argument('-i', '--input', type=str, required=True, help="BLASTp result of best-fit ORF IDs to AF-uniprot IDs")
parser.add_argument('-f', '--files', type=argparse.FileType('r'), nargs='+', help="Files of lists of ORF IDs that satisfy an ORF classification (make sure that the header is given at the top of the file as '# <header>'")
args = parser.parse_args()

# create ORF ID table
orf_table = (pd.read_csv(args.input, sep='\t')).rename(columns={"qseqid": "best_blast_hit_AF_ID", "sseqid": "ORF_seq_ID"})
## determine where header columns start (useful for summary table below)
headers_start_index = len(orf_table.columns)

# determine if ORF IDs are present in classification files
headers = list()
for fclass in args.files:
    # get header
    header = fclass.readline()
    if not header.startswith('#'):
        exit(f"An error occurred: Header not specified in {fclass.name}.")
    header = header.removeprefix("#").strip()
    headers.append(header)

    # add to table binary values of whether tabulated ORF sequence IDs are found in the file
    valid_ORFs = set(line.strip() for line in fclass)
    orf_table[header] = orf_table["ORF_seq_ID"].astype(str).isin(valid_ORFs).astype(int)

# define output file name template
out_filename = f"{args.input.split('.')[0]}_on_{'_'.join(headers)}"

# create table file
out_filename_table = f"{out_filename}.tsv"
if os.path.exists(out_filename_table):
    print(f"File {out_filename_table} detected. Overwriting...")
    os.remove(out_filename_table)
orf_table.to_csv(out_filename_table, sep='\t', index=False)

## create summary table
#def get_i_and_h_from_orf_table()->list[tuple]:
#    return [(i, h) for i, h in enumerate(orf_table.columns[headers_start_index:], start=headers_start_index)]
#
#out_filename_log = f"{out_filename}.summary_table.log"
#if os.path.exists(out_filename_log):
#    print(f"File {out_filename_log} detected. Overwriting...")
#    os.remove(out_filename_log)
#
#with open(out_filename_log, 'w') as fst:
#    # get all header combinations
#    header_combos = list()
#    for r in range(len(headers) + 1):
#        for combo in combinations(set(headers), r):
#            # determine which headers are in combo
#            headers_check = [1 if (h in combo) else 0 for i, h in get_i_and_h_from_orf_table()]
#            
#            # get conditions
#            conditions = list()
#            for i, h in get_i_and_h_from_orf_table():
#                conditions.append(orf_table[h] == headers_check[i - headers_start_index])
#            conditions = reduce(lambda x, y: (x & y), conditions)
#    
#            # write count to file
#            combo_count = len(orf_table[conditions])
#            if not len(combo): fst.write(f"Neither {' nor '.join(h for i, h in get_i_and_h_from_orf_table())}: {combo_count}\n")
#            else:              fst.write(f"{' and '.join(combo)}: {combo_count}\n")

