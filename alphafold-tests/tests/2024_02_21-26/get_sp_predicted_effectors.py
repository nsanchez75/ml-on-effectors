import os
from shutil import rmtree
from time import sleep
import pandas as pd

# used to extract predicted SP-positive effectors from a specific file

df = "ORF_ID_table_creation_results/blastp_output_db_B_lac-SF5_q_blac-uniprot_on_predicted-effectors-ov-85_RXLR-EER_WY-domain_CRN-motif_SP.tsv"
df = pd.read_csv(df, sep='\t')

# only get SPs
df = df[df["SP"].astype(int) == 1]

# get only predicted effectors
wy_df = df[(df["WY-domain"].astype(int) == 1) & (df["RXLR-EER"].astype(int) == 0) & (df["predicted-effectors-ov-85"].astype(int) == 0)]
wy__efo_ov_85__df = df[(df["WY-domain"].astype(int) == 1) & (df["RXLR-EER"].astype(int) == 0) & (df["predicted-effectors-ov-85"].astype(int) == 1)]
wy__rxlr_eer__df = df[(df["WY-domain"].astype(int) == 1) & (df["RXLR-EER"].astype(int) == 1) & (df["predicted-effectors-ov-85"].astype(int) == 0)]
wy__rxlr_eer__efo_ov_85__df = df[(df["WY-domain"].astype(int) == 1) & (df["RXLR-EER"].astype(int) == 1) & (df["predicted-effectors-ov-85"].astype(int) == 1)]
rxlr_eer_df = df[(df["RXLR-EER"].astype(int) == 1) & (df["WY-domain"].astype(int) == 0) & (df["predicted-effectors-ov-85"].astype(int) == 0)]
rxlr_eer__efo_ov_85__df = df[(df["RXLR-EER"].astype(int) == 1) & (df["WY-domain"].astype(int) == 0) & (df["predicted-effectors-ov-85"].astype(int) == 1)]
crn_df = df[(df["CRN-motif"].astype(int) == 1) & (df["predicted-effectors-ov-85"].astype(int) == 0)]
crn__efo_ov_85__df = df[(df["CRN-motif"].astype(int) == 1) & (df["predicted-effectors-ov-85"].astype(int) == 1)]
efo_ov_85_df = df[(df["WY-domain"].astype(int) == 0) & (df["RXLR-EER"].astype(int) == 0) & (df["CRN-motif"].astype(int) == 0) & (df["predicted-effectors-ov-85"].astype(int) == 1)]

DIR = "AF_seqs_to_analyze_in_ESMFold"
if os.path.exists(DIR):
  print(f"Warning: Directory {DIR} detected. Replacing its contents in 3 seconds...")
  sleep(3)
  rmtree(DIR)
os.mkdir(DIR)
  
OUTFILE = "AF_seqs_to_test.fasta"
with open("af-uniprot-id_uniprot-seq.fasta", 'r') as fin, open(f"{DIR}/{OUTFILE}", 'w') as fout:
  infasta = fin.readlines()
  infasta = {infasta[i].strip().split()[0][1:]: infasta[i+1].strip() for i in range(0, len(infasta), 2)}

  def df_to_fasta(df:pd.DataFrame, marker:str)->None:
    headers = df["best_blast_hit_AF_ID"].tolist()
    for header in headers:
      if header in infasta:
        if header in infasta:
          fout.write(f">{header}_{marker}\n" +
                     f"{infasta[header]}\n")

  df_to_fasta(wy_df, "WY")
  df_to_fasta(wy__efo_ov_85__df, "WY-efo-ov-85")
  df_to_fasta(wy__rxlr_eer__df, "RXLR-EER-WY")
  df_to_fasta(wy__rxlr_eer__efo_ov_85__df, "RXLR-EER-WY-efo-ov-85")
  df_to_fasta(rxlr_eer_df, "RXLR-EER")
  df_to_fasta(rxlr_eer__efo_ov_85__df, "RXLR-EER-efo-ov-85")
  df_to_fasta(crn_df, "CRN")
  df_to_fasta(crn__efo_ov_85__df, "CRN-efo-ov-85")
  df_to_fasta(efo_ov_85_df, "efo-ov-85")
