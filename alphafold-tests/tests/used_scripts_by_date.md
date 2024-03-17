# Used Scripts

## 2/21-26/2024

- analyze_ORF_ID_table.py
- create_ORF_ID_table.py
- get_sp_predicted_effectors.py

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
