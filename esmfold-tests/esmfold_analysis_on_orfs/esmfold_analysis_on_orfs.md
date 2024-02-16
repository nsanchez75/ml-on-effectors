# Pipeline for Effector Analysis Using ESMFold

## Getting Started

## Step 1: Running ESMFold

### Input(s)

- FASTA file

### Output(s)

- table (TSV) containing:
  - sequence ID
  - pTM score
  - associated PDB file w/ absolute paths
- results directory (`esm_results_<date>`)
  - files under results directory: (`<sequence name (NCBI?)>_<pTM score>.pdb`)

### Dependencies + Requirements

Note: As of now, it is required to run the script in kakawa-0

## Step 2: Add Contents to Output Table (optional?)

### Input(s)

- Output table from previous step
