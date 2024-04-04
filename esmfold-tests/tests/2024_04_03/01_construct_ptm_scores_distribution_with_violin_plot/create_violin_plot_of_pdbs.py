import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("esm_results.tsv", sep='\t', names=["seq_id", "class", "ptm_score"])

# print(df[["class", "ptm_score"]])
sns.violinplot(df[["class", "ptm_score"]], x="class", y="ptm_score")
plt.show()