# Used Scripts

## 2/21-26/2024

- `analyze_ORF_ID_table.py`
- `create_ORF_ID_table.py`
- `get_sp_predicted_effectors.py`

### Commands Run

(2/21/2024)

```bash
python3 create_ORF_ID_table.py -i blastp_output_db_B_lac-SF5_q_blac-uniprot.filtered_best_hits.txt -l known_effector_id_lists

python3 analyze_ORF_ID_table.py -i ORF_ID_table_creation_results/blastp_output_db_B_lac-SF5_q_blac-uniprot_on_predicted-effectors-ov-85_RXLR-EER_WY-domain_CRN_motif_SP.tsv
```

(2/26/2024)

```bash
python3 create_ORF_ID_table.py -i blastp_output_db_B_lac-SF5_q_blac-uniprot.filtered_best_hits.txt -l known_effector_id_lists

python3 analyze_ORF_ID_table.py -i ORF_ID_table_creation_results/blastp_output_db_B_lac-SF5_q_blac-uniprot_on_predicted-effectors-ov-85_RXLR-EER_WY-domain_CRN-motif_SP.tsv
```

Ran `get_sp_predicted_effectors.py` to produce `AF_seqs_to_analyze_in_ESMFold/AF_seqs_to_test.fasta`

## 3/6/2024

All scripts I used this day are not going to be moved to the src directory because of how particular they are.

```bash
# if all of this is run from directory 2024_03_06
python3 01_append_ncbi/add_ncbi_to_table.py
python3 02_extract_ptm_score/parse_pdb_filenames.py
python3 03_append_ptm_score/append_ptm_score.py
```

## 3/16/2024 - 3/18/2024

```bash
# done in the 01 directory associated w/ the date
makeblastdb -in B_lac-SF5.protein.fasta -title "Bremia Lactucae ORF Sequences" -dbtype prot > B_lac-SF5_db_creation.log
./blastp_q_on_ORFs.sh af-uniprot-id_uniprot-seq.fasta B_lac-SF5.protein.fasta blastp_output_db_B_lac-SF5_q_blac-uniprot.txt
Rscript tabularize_blastp_output.r blastp_output_db_B_lac-SF5_q_blac-uniprot.txt
```

Note: when checking the length of the files (by lines), `blastp_output_db_B_lac-SF5_q_blac-uniprot.txt` is 31593 lines long (including header) and `blastp_output_db_B_lac-SF5_q_blac-uniprot.filtered_best_hits.txt` is 4255 lines (including header).

```bash
# get filtered best hits + AF FASTA file
cp ../01_blastp_blac_on_af-uniprot/af-uniprot-id_uniprot-seq.fasta .
cp ../01_blastp_blac_on_af-uniprot/blastp_output_db_B_lac-SF5_q_blac-uniprot.filtered_best_hits.txt .
```

I also copied `filter_fasta_with_list.sh` into `find_missing_seqs.sh` and changed it so that you just need to input the original FASTA file and the filtered best hits.

```bash
./find_missing_seqs.sh af-uniprot-id_uniprot-seq.fasta blastp_output_db_B_lac-SF5_q_blac-uniprot.filtered_best_hits.txt
```

The following commands identify the blastp results so that it can be determined why they were removed by the Rscript filter. Note that the e-value threshold determined by `blastp_q_on_ORFs.sh` is 1e-10.

```bash
makeblastdb -in af-uniprot-id_uniprot-seq.fasta -title "AF Bremia Lactucae Sequences" -dbtype prot > af-uniprot-id_uniprot-seq_db_creation.log
blastp -query af-uniprot-id_uniprot-seq.filtered_for_missing.fasta -db af-uniprot-id_uniprot-seq.fasta -outfmt "6 std qcovs" -out blastp_on_missing-seqs.txt
Rscript tabularize_blastp_output.r blastp_on_missing-seqs.txt
```
