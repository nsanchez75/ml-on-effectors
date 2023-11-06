# AlphaFold Tests

## What AlphaFold2 Produces

TODO

## Papers to Cite

- Jumper, J et al. Highly accurate protein structure prediction with AlphaFold. Nature (2021).
- Varadi, M et al. AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models. Nucleic Acids Research (2021).

## Experiments: Data and Results

### 10/25/2023

- ran AlphaFold2 Colab file on test sequences (found in data) similar to how I had run the data on ESMFold
  - made sure to omit the '*' at the end of the sequences
  - didn't touch anything in the Colab (just did 'Run All' like it says to do in the Colab)
- results found in 10/25/2023

### 11/1/2023

- found some sequences in Uniprot that come from Bremia Lactucae. Apparently, Alphafold provides predicted structures for the sequences. Link: <https://www.uniprot.org/uniprotkb?query=(taxonomy_id:4779)>
- I created the fasta file `uniprotkb_taxonomy_id_4779_2023_11_01.fasta` by downloading a fasta file from the website above. The file lists all of the Bremia lactucae sequences found in the Uniprot database.
- I will use this to extract all of the Uniprot accession IDs so that I can download all of the AlphaFold predictions associated with Bremia lactucae.
- The predictions may be found in this dataset on Google Cloud: <https://console.cloud.google.com/storage/browser/public-datasets-deepmind-alphafold-v4;tab=objects?prefix=&forceOnObjectsSortingFiltering=false>

### 11/2/2023

I created a Google Cloud account and explored methods to get the AlphaFold sequences from the database. So far, this is what I've found:

- Bremia lactucae's taxonomy ID is 4779 (<https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=4779>)
- The list of sequences can be found in the BigQuery metadata of the database
- You need to get a Google Cloud account in order to access BigQuery (means inputting credit/debit card info)
- **MAKE SURE YOU KNOW WHAT YOU'RE DOING W/ GOOGLE CLOUD**
  - costs can sneak up on you sometimes so make sure to not activate your account (permits payments to begin after the free trial) and, if you do need to activate it, set up budget alerts

### 11/3/2023

I used these steps provided by the [AlphaFold DB Github README.md repo](https://github.com/google-deepmind/alphafold/blob/main/afdb/README.md). So far, I successfully downloaded gsutil using [this guide](https://cloud.google.com/storage/docs/gsutil_install) and tried to make it work, but I need to figure out how to input my credentials as the provided gsutil code (`gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-[TAX ID]-*_v4.tar .`) doesn't work.

I'll start looking more into the authentication stuff while also figuring out if I can access the database in other ways (ex: use the Uniprot list file).

Here is a screenshot of my SQL script in BigQuery where I managed to find all of the Bremia-lactucae AF results:

![Screenshot of BigQuery SQL script into metadata](notebook-images/image.png)

I downloaded the `alphafoldbulk.py` script that may help me download all of the sequences. Kelsey also sent me a bash script that is much simpler:

```bash
file=$1

while read -r line
do
  wget  "https://alphafold.ebi.ac.uk/files/"$line"-model_v4.pdb"
done <$file
```

She also gathered all of the data, so I will look into her directory later and grab all of the data. I might change this code later if I find a better way to specifically grab the Bremia lactucae related pdf files.
