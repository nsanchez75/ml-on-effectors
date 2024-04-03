# ESMFold Tests

## 3/18/2024

```bash
# all commands run in the respective date's folder
awk -F'_' '{gsub(".pdb", "", $3); print $1 "\t" $2 "\t" $3}' esm_pdb_results_2024_02_26.txt > esm_results.tsv
python3 create_histogram_of_pdbs.py esm_results.tsv
```

`create_histogram_of_pdbs.py` was developed, like its name implies, to construct histograms of PDB files (specifically for classification combinations).

