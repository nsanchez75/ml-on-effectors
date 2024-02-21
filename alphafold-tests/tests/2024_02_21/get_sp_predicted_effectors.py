import pandas as pd

# used to extract predicted SP-positive effectors from a specific file

df = "blastp_output_db_B_lac-SF5_q_blac-uniprot_on_WY-Domain_SP_CRN-motif_predicted-effectors-ov-85_RXLR-EER.tsv"
df = pd.read_csv(df, sep='\t')

# only get SPs
df = df[df["SP"].astype(int) == 1]

# get only predicted effectors
wy_df = df[df["WY-Domain"].astype(int) == 1 & df["RXLR-EER"].astype(int) == 0]
wy__rxlr_eer__df = df[df["WY-Domain"].astype(int) == 1 & df["RXLR-EER"].astype(int) == 1]
rxlr_eer_df = df[df["RXLR-EER"].astype(int) == 1 & df["WY-Domain"].astype(int) == 0]
crn_df = df[df["CRN-motif"].astype(int) == 1]
