import pandas as pd
from sys import argv

def get_dataframe(filename: str)->pd.DataFrame:
  match filename[-3:]:
    case "csv": return pd.read_csv(filename)
    case "tsv": return pd.read_table(filename, sep='\t')
    case _: exit("Error: file does not appear to be a valid type (.tsv or .csv).")

if not len(argv) == 4:
  exit("Usage: python3 combine_tables.py <table 1> <table 2> <linker table>")

df1 = get_dataframe(argv[1])
df2 = get_dataframe(argv[2])
dflink = get_dataframe(argv[3])

if dflink.columns.size != 2:
  exit("Error: Linker table must have only two columns.")

DFLINK_COLS = dflink.columns.to_list()

df_comb = df1.merge(right=dflink, how="left", on=DFLINK_COLS[0], validate="1:1")
df_comb = df_comb.merge(right=df2, how="left", on=DFLINK_COLS[1], validate="1:1")

df_comb.to_csv(f"{argv[1][-3:]}__with-NCBI.tsv", sep='\t', index=False)
