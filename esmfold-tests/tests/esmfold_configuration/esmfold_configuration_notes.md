# ESMFold Configuration

Notes about my attempts at getting ESMFold to work.

## 2/5/2024

```bash
srun --pty --gpus 2 -t 60 -p gpu /bin/bash submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
srun: job 61004969 queued and waiting for resources
srun: job 61004969 has been allocated resources
Auks API init failed : unable to parse configuration file
submit_esm.sh: line 16: 723537 Killed                  python3 kakawaESM_include_ptm.py "$1" "$2"
slurmstepd: error: Detected 1 oom_kill event in StepId=61004969.0. Some of the step tasks have been OOM Killed.
srun: error: kakawa-0: task 0: Out Of Memory
```

-------------

```bash
# I removed the SBATCH commands in submit_esm.sh because it kept telling me the time partition was invalid (originally 72:00:00) and that I was still not able to use gpu-siegel
sbatch -t 60 -p gpu --mem 36G submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
Auks API init failed : unable to parse configuration file
Traceback (most recent call last):
  File "kakawaESM_include_ptm.py", line 30, in <module>
    model = model.eval().cuda()
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in cuda
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 602, in _apply
    param_applied = fn(param)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in <lambda>
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/cuda/__init__.py", line 217, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No CUDA GPUs are available
```

```bash
sbatch -t 60 -p gpu --mem 36G --auks=yes submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result
Auks API init failed : unable to parse configuration file
Traceback (most recent call last):
  File "kakawaESM_include_ptm.py", line 30, in <module>
    model = model.eval().cuda()
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in cuda
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 602, in _apply
    param_applied = fn(param)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in <lambda>
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/cuda/__init__.py", line 217, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No CUDA GPUs are available
```

```bash
# I uncommented the esm environment activation in submit_esm.sh to see if the sbatch will run in esm
sbatch -t 60 -p gpu --mem 36G --auks=yes submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
Auks API init failed : unable to parse configuration file
Traceback (most recent call last):
  File "kakawaESM_include_ptm.py", line 30, in <module>
    model = model.eval().cuda()
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in cuda
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 602, in _apply
    param_applied = fn(param)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in <lambda>
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/cuda/__init__.py", line 217, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No CUDA GPUs are available
```

```bash
sbatch -t 60 -p gpu --mem 36G --auks=no submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
Traceback (most recent call last):
  File "kakawaESM_include_ptm.py", line 30, in <module>
    model = model.eval().cuda()
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in cuda
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 602, in _apply
    param_applied = fn(param)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in <lambda>
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/cuda/__init__.py", line 217, in _lazy_init
    torch._C._cuda_init()
RuntimeError: No CUDA GPUs are available
```

```bash
sacctmgr show assoc user=nsanc

```

Result:

```text
Cluster    Account       User  Partition     Share   Priority GrpJobs       GrpTRES GrpSubmit     GrpWall   GrpTRESMins MaxJobs       MaxTRES MaxTRESPerNode MaxSubmit     MaxWall   MaxTRESMins                  QOS   Def QOS GrpTRESRunMin
---------- ---------- ---------- ---------- --------- ---------- ------- ------------- --------- ----------- ------------- ------- ------------- -------------- --------- ----------- ------------- -------------------- --------- -------------
      wopr        rwm      nsanc               parent                                                                                                                                                             normal
      wopr   jbsiegel      nsanc               parent                                                                                                                                                             normal
```

```bash
srun --pty --gpus 2 -t 120 -p gpu-jbsiegel -A jbsiegel /bin/bash submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
srun: job 61004976 queued and waiting for resources
srun: job 61004976 has been allocated resources
Auks API init failed : unable to parse configuration file
submit_esm.sh: line 25: 726278 Killed                  python3 kakawaESM_include_ptm.py "$1" "$2"
slurmstepd: error: Detected 1 oom_kill event in StepId=61004976.0. Some of the step tasks have been OOM Killed.
srun: error: kakawa-0: task 0: Out Of Memory
```

```bash
srun --pty --gpus 2 -t 120 -p gpu-jbsiegel -A jbsiegel --auks=no /bin/bash submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
srun: job 61004977 queued and waiting for resources
srun: job 61004977 has been allocated resources
submit_esm.sh: line 25: 726369 Killed                  python3 kakawaESM_include_ptm.py "$1" "$2"
slurmstepd: error: Detected 1 oom_kill event in StepId=61004977.0. Some of the step tasks have been OOM Killed.
srun: error: kakawa-0: task 0: Out Of Memory
```

```bash
srun -A jbsiegel --auks=no /bin/bash submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/src/test_outdir/

# result:
srun: error: Unable to allocate resources: Requested time limit is invalid (missing or exceeds some limit)
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

## 4/3/2024

Note: `seqs_to_test.fasta` has been changed to `AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta`

```bash
python3 predict_folds.py -i AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta

# result:
Traceback (most recent call last):
  File "predict_folds.py", line 11, in <module>
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

## 4/10/2024

It ended up working! All I needed to do was run the scripts with the conda environment activation commands in the shell script uncommented. This was done during the meeting with Kelsey.

## 4/11/2024

I am now going to try re-running the script to make sure that everything works perfectly fine still. Here is the script that was run yesterday:

```bash
./submit_esm.sh AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta test_outdir_2024_04_11 
# this is an error that shows up but other than this it is fine
ArgumentError: activate does not accept more than one argument:
['AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta', 'test_outdir_2024_04_11']
```

Now I am going to try running it on both the public and Siegel GPU partitions:

```bash
# public partition (ID 61802478)
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/esmfold_configuration/AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/esmfold_configuration/test_outdir_public_partition_2024_04_11  
```

Error message:

```text
/var/spool/slurmd/job61802478/slurm_script: line 25: 3490966 Killed                  python3 kakawaESM_constructs_metadata.py -i $1 -o $2 2> time.log

real    0m45.335s
user    0m18.368s
sys     0m14.053s
slurmstepd: error: Detected 1 oom_kill event in StepId=61802478.batch. Some of the step tasks have been OOM Killed.
```

I have a hunch that maybe the argparse is giving me the errors (maybe bash cannot properly run Python scripts that use argparse) so I created a Python and bash script with the `_non_argparse` suffix.

```bash
./submit_esm_non_argparse.sh AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta test_outdir_non_argparse_2024_04_11
python3 kakawaESM_constructs_metadata
# which works so now I am going to run with the public SLURM paritition (ID 61802561)
sbatch submit_esm_non_argparse.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/esmfold_configuration/AF_seqs_to_analyze_in_ESMFold/two_seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/tests/esmfold_configuration/test_outdir_non_argparse_public_partition_2024_04_11
```

Here is the error:

```text
/var/spool/slurmd/job61802561/slurm_script: line 25: 3492598 Killed                  python3 kakawaESM_old_non_argparse.py $1 $2 2> time.log

real    0m44.639s
user    0m18.432s
sys     0m13.658s
slurmstepd: error: Detected 1 oom_kill event in StepId=61802561.batch. Some of the step tasks have been OOM Killed.
```

So it has nothing to do with argparse.

Since it involves an out-of-memory error, I am going to increase the SLURM mem usage.

