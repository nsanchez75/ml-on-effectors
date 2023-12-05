# EffectorO Tests

## Running EffectorO

Created a conda environment `effectoro.yml` that can be used to run EffectorO

- Code to create conda environment: `conda env create -f [path/to/]effectoro.yml`

Ran EffectorO on `B_lac-SF5.protein.fasta` to test it and it works

## Running EffectorO Before SignalP

Created programs that would run EffectorO first and then SignalP and vice versa

## Extracting Stuff from Munir

- CRN prediction (BlacSF5_CRN.hmm + get_CRN_seqs.sh)
- WY-Domain prediction (WY_fold.hmm + get_WY_seqs.sh)
- RXLR-EER prediction (whisson_et_al_rxlr_eer_cropped.hmm)
- regex searcher for RXLR and EER (regex_searcher.py)
  - **TODO:** change the name to RXLR-EER_regex_searcher.py
