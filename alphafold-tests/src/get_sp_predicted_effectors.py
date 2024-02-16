import pandas as pd

# used to extract predicted SP-positive effectors from a specific file

f = "blastp_output_db_B_lac-SF5_q_blac-uniprot_on_WY-Domain_SP_CRN-motif_predicted-effectors-ov-85_RXLR-EER.tsv"
f = pd.read_csv(f, sep='\t')

# only get SPs
f = f[f["SP"].astype(int) == 1]

# get only predicted effectors
condition = (f["WY-Domain"] == 1) | (f["CRN-motif"] == 1) | (f["predicted-effectors-ov-85"] == 1) | (f["RXLR-EER"] == 1)
f = f[condition]

f.to_csv("blac_sp-predicted-effectors.tsv", sep='\t', index=False)