import os
import pandas as pd

sp_df = pd.read_csv("../01_append_ncbi/ncbi_appending_results/blac_SF5_sp_seqs.tsv", sep='\t')
# print(sp_df)
ptm_df = pd.read_csv("../02_extract_ptm_score/extract_ptm_score_results/esm_pdb_results_2024_02_26.parsed.txt", sep='\t', names=["AF_ID", "ptm_score"])
# print(ptm_df)

results_df = pd.merge(sp_df, ptm_df, on="AF_ID", how="right")

OUTDIR = "appended_ptm_score_results"
os.makedirs(OUTDIR, exist_ok=True)
results_df.to_csv(f"{OUTDIR}/blac_SF5_sp_seqs_with_ptm.tsv", sep='\t', index=False)