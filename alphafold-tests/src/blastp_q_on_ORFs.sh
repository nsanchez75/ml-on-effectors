# inputs:
#   - $1 - query fasta file
#   - $2 - datanase fasta file
#   - $3 - output file

blastp -query "$1" -db "$2" -evalue 1e-10 -outfmt "6 std qcovs" -out "$3"
