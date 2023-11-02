# INFO:
#   This script takes a FASTA files downloaded from Uniprot and makes a file containing all of the accession IDs.
#   Use this script if the accession IDs follow this pattern: '>[tr | sp]|[accession ID]|...'

input_file=$1
output_endstr=".uniprot_accession_ids.txt"
output_file="${input_file%%.*}${output_endstr}"

cat "$input_file" | grep -Po "^>\w+\|\K[^|]*" > $output_file

