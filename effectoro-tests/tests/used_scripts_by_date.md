# EffectorO Scripts

## 4/8/2024

```bash
makeblastdb -in B_lac-SF5.protein.fasta -title "Bremia Lactucae ORF Sequences" -dbtype prot > B_lac-SF5_db_creation.log
python3 test_biopython_blastp.py -i af-uniprot-id_uniprot-seq.fasta -d B_lac-SF5.protein.fasta -n Blac
```
