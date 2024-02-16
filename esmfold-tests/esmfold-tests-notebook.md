# ESMFold Tests

## Using ESMFold API

Created a Python program that tried to use the ESMFold API (<https://esmatlas.com/about>)

Code Example from website:

```bash
curl -X POST --data "GENGEIPLEIRATTGAEVDTRAVTAVEMTEGTLGIFRLPEEDYTALENFRYNRVAGENWKPASTVIYVGGTYARLCAYAPYNSVEFKNSSLKTEAGLTMQTYAAEKDMRFAVSGGDEVWKKTPTANFELKRAYARLVLSVVRDATYPNTCKITKAKIEAFTGNIITANTVDISTGTEGSGTQTPQYIHTVTTGLKDGFAIGLPQQTFSGGVVLTLTVDGMEYSVTIPANKLSTFVRGTKYIVSLAVKGGKLTLMSDKILIDKDWAEVQTGTGGSGDDYDTSFN" https://api.esmatlas.com/foldSequence/v1/pdb/
```

This doesn't work because ESMFold API has a limited amount of usage at a time. We have to use Google Colab or ESMFold repository.

Update 10/25/2023: There's a curl issue so the code definitely doesn't work on my own computer for some reason. Maybe test on lab servers?

(12/4/2023)

According to this [GitHub issue](https://github.com/facebookresearch/esm/discussions/627), there seems to be problems with ESMFold's API use of `curl`. At the end of the discussion forum, user 'tomsercu' suggests to use `curl ... --insecure`. I tested this when testing the API out on large sequences (line 95). It works.

## Using ESMFold Colab

Tried to run ESMFold Colab through Google Colab browser. Had issues with inputting the FASTA file:

- would download FASTA file to Google Colab
- couldn't resolve it so kinda just gave up on it

## Using ESMFold Github Repo

Tried to download repo, create Conda environment, etc.

Ran into an issue with "OpenFold" module not being able to be downloaded.

(12/5/2023)

I am recreating the conda environment so that I can log what exactly went wrong before.

(1/18/2024)

I forgot to add the link to the GitHub repo so [here it is](https://github.com/facebookresearch/esm).

### Using Ian Anderson's Code

Tried running Anderson's code. However, "OpenFold" module issue is happening again.

Found an email from Kelsey about working ssh into Kakawa so I'll try to run the code on Kakawa instead.

I received news from Kelsey that Ian made it so that all members of the Michelmore lab should have access to kakawa. However, I am going to see if it is possible to utilize the GPU.

Here is the code to run Ian's code:

```bash
conda activate esmfold # environment created from provided environment.yml from the ESMFold GitHub: https://github.com/facebookresearch/esm/blob/main/environment.yml
python3 kakawaESM.py seqs_to_test.fasta test_output_dir &> test_kakawaESM.log
```

Here is what is in 'seqs_to_test.fasta':

```text
>RXLR3
MPRCLAVLSFALFTCCIDASTAADAAKVKMLTQSRYPGTVDRIEKVARFLRSHSMDEAEEERLSIWTSFKELLFGGPFSPTRLRAMTADNAVVQFTFSAWNKFSHDDIRKLLAEGMKDMDKQEKEKLNSIIELYFMIRGPD*
>RXLR3B
MLRCLVTIAFTFALFIETLTATEAANVKILTQSRQPKAVDRTINVIRFLRSHSINEAAEERLNVWACLEELLIGGPFSQARLSAMTGDNEIVKLTFSAWNKFSHDDIRNLLAHGMKDMDIREKEMLSSIINLYFLIRGAQ*
```

After running the code, this error occurred:

```text
Traceback (most recent call last):
  File "kakawaESM.py", line 4, in <module>
    import esm
ModuleNotFoundError: No module named 'esm'
```

To fix this, I am following the processes to install the esm module from [this part](https://github.com/facebookresearch/esm/tree/main?tab=readme-ov-file#quick-start-) of the ESMFold GitHub repository.

(1/22/2023)

I cloned the Facebook GitHub repo in order to grab the esm folder. Now with the esm folder in the proper place, we can test the previous code again. This is the new error I get:

```text
Traceback (most recent call last):
  File "kakawaESM.py", line 27, in <module>
    model = esm.pretrained.esmfold_v1()
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/pretrained.py", line 419, in esmfold_v1
    import esm.esmfold.v1.pretrained
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/esmfold/v1/pretrained.py", line 10, in <module>
    from esm.esmfold.v1.esmfold import ESMFold
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/esmfold/v1/esmfold.py", line 17, in <module>
    from esm.esmfold.v1.misc import (
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/esmfold/v1/misc.py", line 10, in <module>
    from einops import rearrange, repeat
  File "/share/rwmwork/nsanc/conda/envs/esmfold/lib/python3.7/site-packages/einops/__init__.py", line 14, in <module>
    from .einops import rearrange, reduce, repeat, einsum, parse_shape, asnumpy
  File "/share/rwmwork/nsanc/conda/envs/esmfold/lib/python3.7/site-packages/einops/einops.py", line 807
    def einsum(tensor: Tensor, pattern: str, /) -> Tensor:
                                             ^
SyntaxError: invalid syntax
```

Looking at the error message, it appears that there is an issue with the einops package in conda. I am going to try re-installing/updating [einops](https://anaconda.org/esri/einops) in the esmfold environment.

Here is a [GitHub issue](https://github.com/facebookresearch/esm/issues/626) about this. It says to downgrade einops to version 0.61 because the syntax above was created with Python 3.8's syntax in mind.

```bash
conda install -c conda-forge einops=0.6.1
```

The old issue has been resolved. However, a new (old) issue has arisen:

```text
Traceback (most recent call last):
  File "kakawaESM.py", line 27, in <module>
    model = esm.pretrained.esmfold_v1()
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/pretrained.py", line 419, in esmfold_v1
    import esm.esmfold.v1.pretrained
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/esmfold/v1/pretrained.py", line 10, in <module>
    from esm.esmfold.v1.esmfold import ESMFold
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/esmfold/v1/esmfold.py", line 17, in <module>
    from esm.esmfold.v1.misc import (
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/esm/esmfold/v1/misc.py", line 12, in <module>
    from openfold.np import residue_constants
ModuleNotFoundError: No module named 'openfold'
```

I will try running these commands from the ESM GitHub while using kakawa-0:

```bash
pip install 'dllogger @ git+https://github.com/NVIDIA/dllogger.git'
pip install 'openfold @ git+https://github.com/aqlaboratory/openfold.git@4b41059694619831a7db195b7e0988fc4ff3a307'
```

These worked! Now I am going to run Ian's code.

Now I'm having even more issues than before. This most recent issue will be named `test_kakawaESM_2024_1_22.log` and it is a long one.

I am now going to try to run the `submit_esm.sh` script:

```bash
./submit_esm.sh seqs_to_test.fasta test_output_dir &> test_kakawaESM.log
```

(1/24/2024)

I have been looking through the differences between kakawa-0's esm environment and my ESMFold environment. Most things in my environment appear to be newer package versions; however, I noticed that `fair-esm` is a package found in esm and not my environment.

I ran ESMFold again on kakawa-0 and it now works. Based on this error that I had emailed Kelsey earlier:

```text
Traceback (most recent call last):
  File "/share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/kakawaESM.py", line 30, in <module>
    model = model.eval().cuda()
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in cuda
    return self._apply(lambda t: t.cuda(device))
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 579, in _apply
    module._apply(fn)
  [Previous line repeated 2 more times]
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 602, in _apply
    param_applied = fn(param)
  File "/toolbox/envs/esm/lib/python3.7/site-packages/torch/nn/modules/module.py", line 689, in <lambda>
    return self._apply(lambda t: t.cuda(device))
RuntimeError: CUDA out of memory. Tried to allocate 20.00 MiB (GPU 0; 79.15 GiB total capacity; 6.38 GiB already allocated; 3.44 MiB free; 6.59 GiB reserved in total by PyTorch) If reserved memory is >> allocated memory try setting max_split_size_mb to avoid fragmentation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
```

the Runtime Error seems like the GPU had been working on someone else's scripts at the same time, which could have prevented me from using it.

Kelsey also mentioned that SLURM will allow me to schedule the script to run when space is available. Additionally, SLURM requires paths to be absolute. Thus, this will be the new script

```bash
sbatch submit_esm.sh /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/seqs_to_test.fasta /share/rwmwork/nsanc/kelsey_work/ml-on-effectors/esmfold-tests/data/2024_01_18-22/test_outdir
```

I get this error:

```text
sbatch: error: Batch job submission failed: Invalid account or account/partition combination specified
```

but this is just because I am not allowed to utilize the Siegel Lab's GPU. So instead I have to use the public GPU partition.

I am editing the kakawa script to potentially grab the PTM score data, which is done in the ESM Colab script. I am going to try to use the code from there:

```bash
 with torch.no_grad():
        for name, sequence in proteins:
            chunk_size = set_chunk_size_based_on_length(len(sequence))
            if chunk_size is not None:
                model.set_chunk_size(chunk_size)
            output = model.infer(sequence,
                                 num_recycles=3,
                                 chain_linker="X"*25,
                                 residue_index_offset=512)  # modified from infer_pdb(sequence)
            ptm = output["ptm"][0] # new
            with open(os.path.join(output_directory, f"{name}_{ptm}.pdb"), "w") as f: # added pTM to filename
                f.write(model.output_to_pdb(output)[0]) # modified
```

and it works!

### Conda bio-embeddings-esm

(1/18/2024)

There is [this conda package](https://anaconda.org/conda-forge/bio-embeddings-esm) that could download the esm module onto conda. I will give it a try:

```text
conda install conda-forge::bio-embeddings-esm
```

(1/22/2024)

I removed esm and stuck with this package being installed; unfortunately, it wouldn't work.

## Experiments: Data & Results

### 10/25/2023

- used `api_create_esmfolds.py` on a small FASTA file (also edited the script to warn the user that the FASTA file must be small or else the API won't work)
- encountered a curl issue that is preventing the script to work (error pasted below). I guess I'll be using Colab instead.

```text
Running ESMFold fold prediction on RXLR3...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
Successfully ran ESMFold fold prediction on RXLR3.
Running ESMFold fold prediction on RXLR3B...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
Successfully ran ESMFold fold prediction on RXLR3B.
```

- copied ESMFold Colab onto my school Google Drive (Michelmore Lab / ML Colabs Folder) and ran the sequences on it
  - made sure to omit the '*' at the end of the sequences
  - didn't run ESMFold with optional code blocks (things about the color of the plots and the plot confidence). Maybe use them next time?
- results found in 10/25/2023 (obviously)

### Creating an ESMFold Pipeline

- ~~long reads on API~~
- short reads on API
- long reads using Kakawa GPU

#### Further Usage of the API

(12/4/2023)

I am going to try using the ESMFold API on this sequence:

```text
>Blac_SF5_v8_1_ORF945_fr4 Blac_SF5_v8_1:1170137..1172389
MSKSIFRSKSGCISANYCVRCMENTMAKEGSTVRLGDIDFDELDDYLEQFQQDEVIKEALSQGVDIREYAQQIEQELRAAEAAAVSQYVMKSADIVELHEEVQECDNLLAKMQEMLLGFQADLGGIGDEIRHLQNESIGMNVKFKNRRETEEKLQTYLDQVAVSPSFVKSIDEGEVDEAYLHALVTLNGKLRYAALKAPDPSGPILDLIPSQTVAFNDVKAQLQKLKGRAVAKIREFLLDKMNEIKKPKTNVQMLQQNTLLPMKYLMTFLVNNAPEVEAEFRDFYAEAMSKTLVNVFKSYYAGLMKFHEEVASNADFIVVDEQTLKGIFSYRVNLSKRKDTFSVTERENILEFASAPPLILHVAQQERSKLPYEAIYRNVQQHLMDSATSEYLFLINFFKPHNQQETSFRSRDLFMRVFAKTLSLCLENLENYLFTCYDAIGLLLMIRITYAQRLVMEKRSITCLGAYFDHVALLLWPRFKAVFELNLMSVKGANVKKLSPIDLHPHLVIRRYAEFASSILSLSLHTKHNQLKHGAVDSKISNAQMHENGAKDMVLTNLAILCDEILSLLSRLSNQHTTAKDKCIFLINNYDLVLSHFEERRVNTEESSKFEKLLATQRDKFVEEELMTFHVKLIQFVRQHEQVTLDNGERLSTESNQQVDTSQIEAIVREYAATWKAGIEKMNGNVMTYFSNFRNGMEILKQVLTQLLLYYTRFVEIVKRSFQQPPSFYSEIVTTQEILNEIKKYSRSF*
```

and using this command:

```bash
time curl -X POST --data "MSKSIFRSKSGCISANYCVRCMENTMAKEGSTVRLGDIDFDELDDYLEQFQQDEVIKEALSQGVDIREYAQQIEQELRAAEAAAVSQYVMKSADIVELHEEVQECDNLLAKMQEMLLGFQADLGGIGDEIRHLQNESIGMNVKFKNRRETEEKLQTYLDQVAVSPSFVKSIDEGEVDEAYLHALVTLNGKLRYAALKAPDPSGPILDLIPSQTVAFNDVKAQLQKLKGRAVAKIREFLLDKMNEIKKPKTNVQMLQQNTLLPMKYLMTFLVNNAPEVEAEFRDFYAEAMSKTLVNVFKSYYAGLMKFHEEVASNADFIVVDEQTLKGIFSYRVNLSKRKDTFSVTERENILEFASAPPLILHVAQQERSKLPYEAIYRNVQQHLMDSATSEYLFLINFFKPHNQQETSFRSRDLFMRVFAKTLSLCLENLENYLFTCYDAIGLLLMIRITYAQRLVMEKRSITCLGAYFDHVALLLWPRFKAVFELNLMSVKGANVKKLSPIDLHPHLVIRRYAEFASSILSLSLHTKHNQLKHGAVDSKISNAQMHENGAKDMVLTNLAILCDEILSLLSRLSNQHTTAKDKCIFLINNYDLVLSHFEERRVNTEESSKFEKLLATQRDKFVEEELMTFHVKLIQFVRQHEQVTLDNGERLSTESNQQVDTSQIEAIVREYAATWKAGIEKMNGNVMTYFSNFRNGMEILKQVLTQLLLYYTRFVEIVKRSFQQPPSFYSEIVTTQEILNEIKKYSRSF" https://api.esmatlas.com/foldSequence/v1/pdb/ --insecure > time_test.log
```

However this produces this output:

```text
Sequence is longer than 400.
```

Using the archived API outputs from October 10th (now copied into a directory under data/2023_10_10), I am analyzing how many files the API can detect before it stops properly analyzing the sequence. Here are some commands I am using to analyze the directory:

```bash
# list files w/ sizes
ls -Slh predicted_esmfolds_from_api/ > api_esmfold_predictions.log
# list files w/ size >23 bytes (the 'message forbidden' is this many bytes)
find predicted_esmfolds_from_api/ -type f -size +23c > api_esmfold_predictions.not_message_forbidden.log
# count of files w/ size >23 bytes ->
wc -l api_esmfold_predictions.not_message_forbidden.log # there's 75
```

I am thinking that we can cheeze the system and try running the API after 30ish minutes or so after running the API on a bunch of sequences.

--------

##### Looking into the ESMFold Metadata

In addition, I found some metadata that I could use to find any Bremia lactucae sequences that may be in the ESMFold database. I used the command below to access the file. I found out about this through [the ESMFold GitHub repo](https://github.com/facebookresearch/esm/tree/main/scripts/atlas#esm-metagenomic-atlas):

```bash
wget https://dl.fbaipublicfiles.com/esmatlas/v2023_02/metadata-rc2.parquet &
```

When trying to run it in the background, it prevented me from using the CLI again as a 'redirecting output to 'wget-log' message that stays up for a while. I ended the session and ran htop on another session and the wget was still running, so hopefully it still works.

Here is the result of me trying to run the mentioned use of pandas via the python3 shell:

```python
>>> import pandas as pd
>>> df = pd.read_parquet('metadata.parquet')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/share/rwmwork/nsanc/conda/lib/python3.9/site-packages/pandas/io/parquet.py", line 491, in read_parquet
    impl = get_engine(engine)
  File "/share/rwmwork/nsanc/conda/lib/python3.9/site-packages/pandas/io/parquet.py", line 52, in get_engine
    raise ImportError(
ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'.
A suitable version of pyarrow or fastparquet is required for parquet support.
Trying to import the above resulted in these errors:
 - Missing optional dependency 'pyarrow'. pyarrow is required for parquet support. Use pip or conda to install pyarrow.
 - Missing optional dependency 'fastparquet'. fastparquet is required for parquet support. Use pip or conda to install fastparquet.
```

This means I will have to create an environment that defines the 'pyarrow' and 'fastparquet' dependencies; I'm going to use conda.

(12/5/2023)

I created a conda environment with `esmfold_metadata.yml`.

(01/09/2024)

I checked to see if the esmfold-metadata environment contains 'pyarrow' and 'fastparquet' and they are:

- fastparquet 2023.10.1
- pyarrow 14.0.1

I reran the command previously attempted:

```python
>>> import pandas as pd
>>> df = pd.read_parquet('metadata-rc2.parquet') # corrected from error in previous .parquet name
```

It is taking a while, presumably because the dataframe is being created from parsing 16 GB of data. Additionally, I looked into MGnify, of which its IDs are what ESMFold use for sequence identification in its database, and I was unable to find any lettuce or Bremia lactucae sequences. Thus, I believe that I should not continue working on ESMFold's metadata for the time being.

--------

I will create a script that will use the ESMFold API that implements the cheeze method I mentioned in line 121. Since I already have it available, I am going to update my `api_create_esmfolds.py` script from a while ago.

<!--
I am going to run this script:

```bash
time (python3 api_create_esmfolds.py B_lac-SF5.protein.fasta &> esmfold_api_test.log) &> esmfold_api_test_time.log &
```
-->

(12/5/2023)

After runnning it at around 9:00 am, I checked to see how the script was doing at around 10:40 am. I found that the script stopped running and that the resulting directory has a blank PDB file for this sequence:

```text
>Blac_SF5_v8_2_ORF39667_fr1 Blac_SF5_v8_2:872773..873234
MLAVRIHRLRLRISRKRSQKQCNSCFCRQFQQDGTSCCKPESISAPGCARVFIDTAFKLHALPHELVSDRDSRFTAEFWQSVFREIGTRLTMTTSDYLETDGQTERVNHVHEEILRGYFQSYPNWSEFLPMVEIVINNSVHASTTHTPFFVNG*
```

This is on lines 4021-4022 in `B_lac-SF5.protein.fasta`. This means that there were 2011 sequences analyzed. The directory has 2083 PDB files in it.

I am going to run the curl method on it to test if the API is still working or if it is being limited at the moment:

```bash
curl -X POST --data "MLAVRIHRLRLRISRKRSQKQCNSCFCRQFQQDGTSCCKPESISAPGCARVFIDTAFKLHALPHELVSDRDSRFTAEFWQSVFREIGTRLTMTTSDYLETDGQTERVNHVHEEILRGYFQSYPNWSEFLPMVEIVINNSVHASTTHTPFFVNG" https://api.esmatlas.com/foldSequence/v1/pdb/ --insecure > test.pdb
```

I am noticing that the statistics of the curl function is sent using STDERR and the PDB file creation is sent to STDOUT, so I am going to separate them under the subprocess.

Also, I am going to use this command instead of the previous one to run the API fetcher:

```bash
time python3 api_create_esmfolds.py B_lac-SF5.protein.fasta > esmfold_api_test.log 2> esmfold_api_time.log
```

**TODO:** figure out how to get the pTM score for the PDBs.

#### Running ESMFold Colab on WY-Domain

(12/7/2023)

Kelsey gave me an excel sheet (which I converted from xslx -> csv) called `Bremia-WY-NCBI-seqs.csv`. I isolated the NCBI IDs and sequences into a file called `Bremia-WY_NCBI-ID_seqs.tsv`. I am running the ESMFold Colab on each sequence and putting their results `into data/2023_12_07/esmfold_colab_results`. There are a total of 60 sequences provided and I am also going to run these sequences until Colab tells me to upgrade. All options specified in the ESMFold Colab by default are used:

- version: 1
- copies: 1
- num_recycles: 3
- color: confidence
- uncheck show_sidechains and show_mainchains
- dpi: 100

note: ESMFold removes the '.' in the NCBI sequence so remember to keep this in mind later.

Since the ESMFold Colab can only work on sequences up to ~900 aas, I may not be able to run it on the last 5ish sequences in the file.

I am using this in the `esmfold_colab_results` directory to determine if I missed any sequences when running them on Colab:

```bash
ls | awk -F'_' '{print $1}' | sed 's/1$/.1/' | less
```

(12/8/2023)

My school account ran out of free GPU usage, but I was able to bypass it by using my personal account. In the end, I managed to get all the sequences except for {TDH72527.1, TDH69657.1, TDH69683.1} since they were well over 900aa.

I made sure I got all of the sequences by running this code:

```bash
diff <(ls | awk -F'_' '{print $1}' | sed 's/1$/.1/' | sort) <(awk -F'\t' '{print $1}' ../Bremia-WY_NCBI-ID_seqs.tsv | tail -n +2 | sort)
```
