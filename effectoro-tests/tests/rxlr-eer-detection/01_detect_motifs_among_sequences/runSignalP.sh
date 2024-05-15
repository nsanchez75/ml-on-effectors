#!/bin/bash

# note: obtained this script from Munir Nur

#SBATCH -c 2  ## number of cores
#SBATCH -B 1  ## Number of machines cores are located on (1 is optimal)
#SBATCH -J B.lacSF5 ## Job name
#SBATCH -p gc512  ## partitional to submit to -- generally gc
#SBATCH --mem=3G # Memory pool required - Not currently implemented on cabernet
#SBATCH --mem-per-cpu 1000
#SBATCH --time=7-0 # day-hours:min:sec   min:sec
#SBATCH --mail-type=END # Tpe of email notification to recieve
#SBATCH --mail-user=mjnur@ucdavis.edu # email to which notifications will be sent. Not implemented yet.


#usage: ./runSignalP.sh Path_to_genome_file
#output: segnalP_results_Path_to_genome directory (located in your current working directory)
#        secretome:     signalP_results_fileName/hasSignalPeptide.fasta 
#        non-secreted:  signalP_results_fileName/noSignalPeptide.fasta
#        raw results:   signalP_results_fileName/rawResults.fasta


source /etc/profile.d/modules_sh.sh
module load signalp/4.1c #sensitive mode, with -u 0.34 and -U 0.34

#get genome name, check if it exists 
    GENOME="$1"
    file="${1##*/}"

    if [ ! -f $GENOME ]; then 
        echo -e "\nFile "$1" was not found.\n" && exit 1 ; fi
 
    echo -e "\nRunning SignalP 4.1 (sensitive) on $1\n"
    echo -e "results will be found in signalP_results_${file}/\n"

#create new, empty signalP_results_${file} file
    rm -fr -- signalP_results_${file}/ && 
        mkdir signalP_results_${file}
    rm -f -- signalP_results_${file}/noSignalPeptide.fasta && 
        touch signalP_results_${file}/noSignalPeptide.fasta
    rm -f -- signalP_results_${file}/hasSignalPeptide.fasta && 
        touch signalP_results_${file}/hasSignalPeptide.fasta
    rm -f -- signalP_results_${file}/rawResults.txt && 
        touch signalP_results_${file}/rawResults.txt
    
    #temp files
    rm -f -- signalP_results_${file}/tempGene.fasta && 
        touch signalP_results_${file}/tempGene.fasta
    rm -f -- signalP_results_${file}/tempRawResults.txt && 
        touch signalP_results_${file}/tempRawResults.txt


    #extract/loop through genes in GENOME, submit <5K at a time for signalP processing
        FILE_POSITION=1
        FILE_LENGTH=$(grep -c '' $1)

        while  [ $FILE_LENGTH -gt $FILE_POSITION  ] ; do
            END=$(($FILE_POSITION + 6999))

            if [ $END -gt $FILE_LENGTH ] ; then
               END=$FILE_LENGTH            
            fi
                
            echo -e "processing lines $FILE_POSITION - $END  of $FILE_LENGTH" 
            sed -n $FILE_POSITION,$END'p' $GENOME > signalP_results_${file}/tempGene.fasta 
            signalp -u 0.34 -U 0.34 signalP_results_${file}/tempGene.fasta > signalP_results_${file}/tempRawResults.txt
            
            #remove headers from intermediate results
            if [ $FILE_POSITION -ne 1 ] ; then
                sed -i -e 1,2d signalP_results_${file}/tempRawResults.txt
            fi

            cat signalP_results_${file}/tempRawResults.txt >> signalP_results_${file}/rawResults.txt

            FILE_POSITION=$(($END + 1))
        done

        echo -e "\ngenerating secretome from tabular raw signalP results file..."

    #now look through tabular signalP_results_${file} file, generating secretome file 
        NUM_RESULTS=$(grep -c '' signalP_results_${file}/rawResults.txt)

        for (( GENE=3; GENE<=NUM_RESULTS; ((GENE++)) )) ; do
            #put tabular line signalP_results_${file} in array
            LINE=$(head -$GENE signalP_results_${file}/rawResults.txt | tail -n -1)
            COLS=()

            for val in $LINE ; do
                COLS+=("$val")
            done
            SIGNAL=${COLS[9]}

            SAFE=$(printf '%s\n' "$COLS" | sed 's/[[\.*^$/]/\\&/g')
            LINE_NUM=$(sed -n "/>$SAFE /=" $GENOME)

            if [ $SIGNAL = "Y" ]
            then
                tail -n+$LINE_NUM $GENOME | head -n2 >> signalP_results_${file}/hasSignalPeptide.fasta
            else
                tail -n+$LINE_NUM $GENOME | head -n2  >> signalP_results_${file}/noSignalPeptide.fasta 
            fi

        done
            
    echo -e "\nPROCESS COMPLETED, results found in signalP_results_${file}"


    rm -f -- temp*
    rm -f -- signalP_results_${file}/temp*
   
