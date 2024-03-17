import os
import pandas as pd
import matplotlib.pyplot as plt

ptm_df = pd.read_csv("../02_extract_ptm_score/extract_ptm_score_results/esm_pdb_results_2024_02_26.parsed.txt",
                     sep='\t', names=["AF_ID", "ptm_score"])

scores = ptm_df["ptm_score"].astype(float).tolist()

plt.hist(scores)
OUTDIR = "ptm_statistics_results"
os.makedirs(OUTDIR, exist_ok=True)
plt.savefig(f"{OUTDIR}/ptm_score_distribution.jpg")
