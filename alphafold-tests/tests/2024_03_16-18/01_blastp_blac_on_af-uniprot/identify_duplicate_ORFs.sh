#!/bin/bash

blastp_result=$1
duplicate_ORFs=$2
out_dup_filename=$3
out_unique_filename=$4

cat $blastp_result > $out_unique_filename
echo "### blastp output with only duplicate ORFs\n" > $out_dup_filename

while read ORF; do
    # add duplicate ORF lines to duplicate file
    echo $(cat "$blastp_result" | grep "$ORF") >> $out_dup_filename
    
    # remove duplicate ORF lines from unique file
    cat $out_unique_filename | grep -v -e "$ORF" > tmp_file.txt
    cat tmp_file.txt > $out_unique_filename
done < $duplicate_ORFs

rm tmp_file.txt
