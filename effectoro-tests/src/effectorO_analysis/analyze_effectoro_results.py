from argparse import ArgumentParser, FileType

def main():
  parser = ArgumentParser(prog='A Python script to analyze the output of EffectorO.')
  parser.add_argument("--fasta_input", "-i", type=FileType('r'), help="Input FASTA file (should be an EffectorO result)", required=True)
  parser.add_argument("--filter_list", "-f", type=FileType('r'), help="Input file that lists names of sequences to be focused on", required=False)
  parser.add_argument("--min_cutoff", "-m", type=float, help="Minimum effector probability cutoff", required=False)
  parser.add_argument("--max_cutoff", "-M", type=float, help="Maximum effector probability cutoff", required=False)
  args = parser.parse_args()

  # declare input variables
  input_fasta_filename = args.fasta_input.name
  effectoro_result = args.fasta_input.read().splitlines()
  filter_list = (set(args.filter_list.read().splitlines())) if (args.filter_list) else (None)
  min_cutoff = (args.min_cutoff) if (args.min_cutoff) else (None)
  max_cutoff = (args.max_cutoff) if (args.max_cutoff) else (None)

  # filter effectoro result
  indices_to_delete = list()
  for i, element in enumerate(effectoro_result):
    # only deal with headers for information
    if element[0] != '>':
      continue

    header = element[1:].split()
    if filter_list is not None and header not in filter_list:
      indices_to_delete += [i, i+1]
    


if __name__ == "__main__":
  main()