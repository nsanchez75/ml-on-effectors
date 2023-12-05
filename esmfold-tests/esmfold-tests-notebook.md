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

## Using Ian Anderson's Code

### Before 10/19/2023

Tried running Anderson's code. However, "OpenFold" module issue is happening again.

Found an email from Kelsey about working ssh into Kakawa so I'll try to run the code on Kakawa instead

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

#### Further Tests on the API

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

which makes no sense because according to the ESMFold Colab notebook, "For short monomeric proteins under the length 400, consider using ESMFold API." Kinda dumb.

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

```text
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

**TODO:** create a Conda environment to access the ESMFold metadata

--------

I will create a script that will use the ESMFold API that implements the cheeze method I mentioned in line 121. Since I already have it available, I am going to update my `api_create_esmfolds.py` script from a while ago.

I am going to run this script:

```bash
python3 api_create_esmfolds.py B_lac-SF5.protein.fasta &> test.log &
```
