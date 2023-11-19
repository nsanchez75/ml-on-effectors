# input: csv file
# output: fasta file

import sys

with open(sys.argv[1], 'r') as fin, open("output_fasta.fasta", 'w') as fout:
    for line in fin:
        line = line.strip().split('\t')
        fout.write('>' + line[0] + '\n')
        fout.write(line[1] + '\n')

