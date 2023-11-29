#!/bin/bash

# input parameters
fasta_file=$1
input_list=$2

# create output filename
outfilename=$(echo $input_list | sed 's/\(^[^.]*\).*$/\1/').filtered.fasta

# overwrite filename if needed
if [ -e "$outfilename" ]; then
  echo "Warning: $outfilename detected. Overwriting..."
  rm $outfilename
fi

# create filtered fasta file
while IFS= read -r id; do
  # check if ID is present in file
  if grep -q "$id" "$fasta_file"; then
    grep -A 1 -F "$id" "$fasta_file" | grep -v "^--$" >> $outfilename
  fi
done < "$input_list"