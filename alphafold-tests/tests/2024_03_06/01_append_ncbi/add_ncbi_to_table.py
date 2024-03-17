import os
import pandas as pd

orf_df = pd.read_csv("blastp_output_db_B_lac-SF5_q_blac-uniprot_on_predicted-effectors-ov-85_RXLR-EER_WY-domain_CRN-motif_SP.tsv", sep='\t')
orf_df = orf_df.rename(columns={"best_blast_hit_AF_ID": "AF_ID"})
ncbi_to_af_df = pd.read_csv("blastp_output_AF-ID_ncbi-proteins.filtered_best_hits.txt", sep='\t')
ncbi_to_af_df = ncbi_to_af_df.rename(columns={"qseqid": "AF_ID",
                                              "sseqid": "NCBI_ID"})
# print(ncbi_to_af_df)

for df in [orf_df, ncbi_to_af_df]:
  df.drop(columns=["pident",
                  "length",
                  "mismatch",
                  "gapopen",
                  "qstart",
                  "qend",
                  "sstart",
                  "send",
                  "evalue",
                  "bitscore",
                  "qcovs"],
          inplace=True)

resulting_df = pd.merge(ncbi_to_af_df, orf_df, on="AF_ID", how="right")
sp_df = resulting_df[resulting_df["SP"].astype(int) == 1]
# print(sp_df)
non_sp_df = resulting_df[resulting_df["SP"].astype(int) == 0]
# print(non_sp_df)

OUTDIR = "ncbi_appending_results"
os.makedirs(OUTDIR, exist_ok=True)
sp_df.to_csv(f"{OUTDIR}/blac_SF5_sp_seqs.tsv", sep='\t', index=False)
non_sp_df.to_csv(f"{OUTDIR}/blac_SF5_non_sp_seqs.tsv", sep='\t', index=False)
