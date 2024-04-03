#!/bin/bash

# input parameters
originalFastaFile=$1
filteredBestBlastp=$2

# create output filename
outFilename=$(echo $originalFastaFile | sed 's/\(^[^.]*\).*$/\1/').filtered_for_missing.fasta

# determine differences between filtered list and original FASTA file
## grep -Po '^>\K\S+' af-uniprot-id_uniprot-seq.fasta | sort
## awk -F' ' '{print $1}' blastp_output_db_B_lac-SF5_q_blac-uniprot.filtered_best_hits.txt | tail -n +2 | sort
## grep -Po '< \S+' | cut -c 3-
diff <(grep -Po '^>\K\S+' $originalFastaFile | sort) <(awk -F' ' '{print $1}' $filteredBestBlastp | tail -n +2 | sort) | grep -Po '< \S+' | cut -c 3- > missing_ids.txt

# overwrite filename if needed
if [ -e "$outFilename" ]; then
  echo "Warning: $outFilename detected. Overwriting..."
  rm $outFilename
fi

# create filtered fasta file
while IFS= read -r id; do
  # check if ID is present in file
  if grep -q "$id" "$originalFastaFile"; then
    grep -A 1 -F "$id" "$originalFastaFile" | grep -v "^--$" >> $outFilename
  fi
done < missing_ids.txt

rm missing_ids.txt

