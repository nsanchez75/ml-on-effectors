#!/bin/bash

input=$1
dir_to_check=$2

echo "Checking if AF entries exist..."

echo "Following entries do not exist in directory ${dir_to_check}" >> "entry_existence_results.log"

while IFS= read -r entry_name
do
    entry_name="${entry_name}-model_v4.pdb"
    if [ ! -e "$dir_to_check/$entry_name" ]; then
        echo "$entry_name" >> "entry_existence_results.log"
    #else
    #    echo "$entry_name exists"
    fi
done < $input

echo "Done."

