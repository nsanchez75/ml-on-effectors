# ESMFold Tests

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

## 2/28-29/2024

```bash
sacctmgr show assoc user=nsanc
```

results in

```text
   Cluster    Account       User  Partition     Share   Priority GrpJobs       GrpTRES GrpSubmit     GrpWall   GrpTRESMins MaxJobs       MaxTRES MaxTRESPerNode MaxSubmit     MaxWall   MaxTRESMins                  QOS   Def QOS GrpTRESRunMin
---------- ---------- ---------- ---------- --------- ---------- ------- ------------- --------- ----------- ------------- ------- ------------- -------------- --------- ----------- ------------- -------------------- --------- -------------
      wopr        rwm      nsanc               parent                                                                                                                                                             normal
      wopr   jbsiegel      nsanc               parent                                                                                                                                                             normal
```

retry this config:

  3 #SBATCH -J esmfold
  4 #SBATCH -e %j.stderr.out
  5 #SBATCH -o %j.stout.out
  6 #SBATCH --partition=gpu-jbsiegel
  7 #SBATCH --time=72:00:00
  8 #SBATCH --gres=gpu:1
  9 #SBATCH --mem=16G
 10 #SBATCH --ntasks=8

which results in

```bash
sbatch: error: Batch job submission failed: Invalid account or account/partition combination specified
```

specify account:

```bash
sbatch -A nsanc submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_26_02/AF_seqs_to_analyze_in_ESMFold/AF_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_26_02/test_outdir
```

results in

```bash
sbatch: error: Batch job submission failed: Invalid account or account/partition combination specified
```

submit_esm.sh sbatch config:

  3 #SBATCH -J esmfold
  4 #SBATCH -e %j.stderr.out
  5 #SBATCH -o %j.stout.out
  6 #SBATCH --partition=jbsiegel
  7 #SBATCH --time=72:00:00
  8 #SBATCH --gres=gpu:1
  9 #SBATCH --mem=16G
 10 #SBATCH --ntasks=8

```bash
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_26_02/AF_seqs_to_analyze_in_ESMFold/AF_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_26_02/test_outdir
```

results in

```bash
sbatch: error: invalid partition specified: jbsiegel
sbatch: error: Batch job submission failed: Invalid partition name specified
```

## 3/4/2024

```bash
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_02_26-03_04/AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_02_26-03_04/test_outdir
```

```bash
python3 kakawaESM_constructs_metadata.py -i AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta -o two_seqs_results
```

## 3/6/2024

```bash
python3 kakawaESM_constructs_metadata.py -i AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta

# returned output:
Traceback (most recent call last):
  File "/toolbox/esm/esm/pretrained.py", line 33, in load_hub_workaround
    data = torch.hub.load_state_dict_from_url(url, progress=False, map_location="cpu")
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/hub.py", line 731, in load_state_dict_from_url
    return torch.load(cached_file, map_location=map_location)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/serialization.py", line 705, in load
    with _open_zipfile_reader(opened_file) as opened_zipfile:
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/serialization.py", line 242, in __init__
    super(_open_zipfile_reader, self).__init__(torch._C.PyTorchFileReader(name_or_buffer))
RuntimeError: PytorchStreamReader failed reading zip archive: failed finding central directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "kakawaESM_old.py", line 39, in <module>
    model = esm.pretrained.esmfold_v1()
  File "/toolbox/esm/esm/pretrained.py", line 420, in esmfold_v1
    return esm.esmfold.v1.pretrained.esmfold_v1()
  File "/toolbox/esm/esm/esmfold/v1/pretrained.py", line 59, in esmfold_v1
    return _load_model("esmfold_3B_v1")
  File "/toolbox/esm/esm/esmfold/v1/pretrained.py", line 23, in _load_model
    model = ESMFold(esmfold_config=cfg)
  File "/toolbox/esm/esm/esmfold/v1/esmfold.py", line 59, in __init__
    self.esm, self.esm_dict = esm_registry.get(cfg.esm_type)()
  File "/toolbox/esm/esm/pretrained.py", line 387, in esm2_t36_3B_UR50D
    return load_model_and_alphabet_hub("esm2_t36_3B_UR50D")
  File "/toolbox/esm/esm/pretrained.py", line 63, in load_model_and_alphabet_hub
    model_data, regression_data = _download_model_and_regression_data(model_name)
  File "/toolbox/esm/esm/pretrained.py", line 54, in _download_model_and_regression_data
    model_data = load_hub_workaround(url)
  File "/toolbox/esm/esm/pretrained.py", line 39, in load_hub_workaround
    map_location="cpu",
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/serialization.py", line 705, in load
    with _open_zipfile_reader(opened_file) as opened_zipfile:
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/serialization.py", line 242, in __init__
    super(_open_zipfile_reader, self).__init__(torch._C.PyTorchFileReader(name_or_buffer))
RuntimeError: PytorchStreamReader failed reading zip archive: failed finding central directory
```

```bash
# script below did not work either
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_02_26-03_04/AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/2024_02_26-03_04/test_outdir
```

```bash
python3 predict_folds.py seqs_to_test.fasta
```

## 3/18/2024

```bash
# all commands run in the respective date's folder
awk -F'_' '{gsub(".pdb", "", $3); print $1 "\t" $2 "\t" $3}' esm_pdb_results_2024_02_26.txt > esm_results.tsv
python3 create_histogram_of_pdbs.py esm_results.tsv
```

`create_histogram_of_pdbs.py` was developed, like its name implies, to construct histograms of PDB files (specifically for classification combinations).
