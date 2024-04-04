# ESMFold Tests

Note: configuration scripts are kept separate in the `esmfold_configuration_notes.md` in the respective directory.

## 2/26/2024

```bash
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_26_02/AF_seqs_to_analyze_in_ESMFold/AF_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_26_02/test_outdir
```

Changed

```bash
source '/toolbox/softwares/anaconda3/etc/profile.d/conda.sh'
```

to

```bash
source /toolbox/softwares/anaconda3/bin/activate
```

```bash
time ./submit_esm.sh AF_seqs_to_analyze_in_ESMFold/AF_seqs_to_test.fasta test_outdir 2> time.log &
```

## 3/4/2024

```bash
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_02_26-03_04/AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_02_26-03_04/test_outdir
```

```bash
python3 kakawaESM_constructs_metadata.py -i AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta -o two_seqs_results
```

## 3/18/2024

```bash
# all commands run in the respective date's folder
awk -F'_' '{gsub(".pdb", "", $3); print $1 "\t" $2 "\t" $3}' esm_pdb_results_2024_02_26.txt > esm_results.tsv
python3 create_histogram_of_pdbs.py esm_results.tsv
```

`create_histogram_of_pdbs.py` was developed, like its name implies, to construct histograms of PDB files (specifically for classification combinations).

## 4/3/2024

Copied `esm_results.tsv` from `2024_03_18` directory and developed `create_violin_plot_of_pdbs.py`.

```bash
python3 create_violin_plot_of_pdbs.py
```
