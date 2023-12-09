import pandas as pd
from argparse import ArgumentParser


def get_dataframe(filename: str)->pd.DataFrame:
  match filename[-3:]:
    case "csv": return pd.read_csv(filename)
    case "tsv": return pd.read_table(filename, sep='\t')
    case _: exit("Error: File does not appear to be a valid type (.tsv or .csv).")

if __name__ == "__main__":
  # get arguments
  parser = ArgumentParser(prog="Table Merger with Linker", description="Python script to merge two tables together using a linker table.")
  parser.add_argument('-l', "--left_table",   type=str, required=True, help="File name for table that will be on the left side of the resulting table.")
  parser.add_argument('-r', "--right_table",  type=str, required=True, help="File name for table that will be on the right of the resulting table.")
  parser.add_argument('-L', "--linker_table", type=str, required=True, help="File name for table that contains the 2-column linker table.")
  parser.add_argument('-o', "--output_table", type=str, required=True, help="File name for resulting table.")

  args = parser.parse_args()

  df1 = get_dataframe(args.left_table)
  df2 = get_dataframe(args.right_table)
  dflink = get_dataframe(args.linker_table)

  if dflink.columns.size != 2:
    exit("Error: Linker table must have only two columns.")

  DFLINK_COLS = dflink.columns.to_list()

  df_comb = df1.merge(right=dflink, how="left", on=DFLINK_COLS[0], validate="1:1")
  df_comb = df_comb.merge(right=df2, how="left", on=DFLINK_COLS[1], validate="1:1")

  # produce resulting table
  match args.output_table[-3:]:
    case "csv": df_comb.to_csv(args.output_table, index=False)
    case "tsv": df_comb.to_csv(args.output_table, sep='\t', index=False)
    case _: exit("Error: Output table does not appear to be a valid type (.tsv or .csv).")
