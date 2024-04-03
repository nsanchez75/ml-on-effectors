import sys
from matplotlib import pyplot as plt
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python3 create_histogram_of_pdbs.py [input_table_with_pdbs.tsv]") 

df = pd.read_csv(sys.argv[1], sep='\t', names=["AF_ID", "classification", "pdb_score"])

classifications = set(df["classification"].unique())

for classification in classifications:
    class_df = df[df["classification"].astype(str) == classification]
    class_pdbs = class_df["pdb_score"]
    plt.hist(class_pdbs, bins=20)
    plt.xlabel("PDB score")
    plt.ylabel("Frequency")
    plt.title(f"Histogram for {classification}")

    plt.savefig(f"histogram_for_{classification}.png")
    plt.clf()

