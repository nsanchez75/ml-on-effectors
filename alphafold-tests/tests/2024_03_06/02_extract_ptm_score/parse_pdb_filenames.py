import os

os.makedirs("extract_ptm_score_results", exist_ok=True)
with open("esm_pdb_results_2024_02_26.txt", 'r') as fpdbs, open("extract_ptm_score_results/esm_pdb_results_2024_02_26.parsed.txt", 'w') as fout:
  lines = fpdbs.readlines()
  for i, line in enumerate(lines):
    line = line.strip().split('_')
    l1 = line[0]
    l2 = float(line[2].removesuffix(".pdb"))
    l2 = round(l2, 4)
    line = f"{l1}\t{l2}\n"
    lines[i] = line
  fout.writelines(lines)