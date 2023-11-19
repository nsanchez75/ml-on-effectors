import pandas as pd
import os
import sys

# INFO:
#   - inputs:
#       - input table linking uniprot IDs and ORFs
#       - 1/more inputs describing what ORF classification exists via this format: [name of column] [input file]
#           - examples for what this input file can be are: WY ORFs, >= 0.85 predicted effectors, RXLR ORFs, etc.
#           - note: these input files should just be lists of what ORF sequence names apply to the given classification
#   - output: TSV file containing (0/1) values of whether or not each uniprot ID can be associated to the ORF classifications

# checking arguments pass
print("Checking arguments...")
if len(sys.argv) <= 1 or len(sys.argv) % 2 != 0:
    sys.exit("Usage: python3 create_uniprot-id_table.py <input file where uniprotID <-> ORFs> {<name of ORF classification> <ORF classification file path>}")

# get linker file
print("Getting linker file...")
if not os.path.exists(sys.argv[1]):
    sys.exit("Input file that links uniprot IDs to ORFs cannot be found")
linker_file = sys.argv[1]

# get ORF classifications
print("Getting ORF classifications...")
orf_classes = list()
orf_class_files = list()
for i in range(2, len(sys.argv), 2):
    orf_classes.append(sys.argv[i])
    
    # check if ORF classification file exists
    if not os.path.exists(sys.argv[i + 1]):
        sys.exit(f"File {sys.argv[i + 1]} for class '{sys.argv[i]}' does not exist.")
    orf_class_files.append(sys.argv[i + 1])

print("Creating table")
table_df = pd.read_csv(linker_file, sep='\t', names=["Uniprot_ID", "ORF_Sequence"])

# add classifications to table
for i in range(len(orf_classes)):
    with open(orf_class_files[i], 'r') as forfc:
        valid_ORFs = set(line.strip() for line in forfc)
        table_df[orf_classes[i]] = table_df["ORF Sequence"].astype(str).isin(valid_ORFs).astype(int)

print("Successfully created table!")
table_df.to_csv(f"uniprot-IDs_to_ORFs_{'_'.join(orf_classes)}.tsv", sep='\t', index=False)
