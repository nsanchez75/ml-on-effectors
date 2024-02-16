from argparse import ArgumentParser, FileType

def main():
  parser = ArgumentParser(prog="List of IDs to FASTA", description="Converts a list of IDs into a FASTA sequence")
  parser.add_argument("-l", "--input_list", type=FileType('r'), help="Input list file", required=True)
  parser.add_argument("-f", "--input_fasta", type=str, help="Input FASTA filename", required=True)
  parser.add_argument("-o", "--output_filename", type=str, help="Output FASTA filename", required=True)
  args = parser.parse_args()

  id_set = set(args.input_list.read().splitlines())

  with open(args.input_fasta, 'r') as fin, open(args.output_filename, 'w') as fout:
    lines = fin.readlines()
    for i, line in enumerate(lines):
      if not line[0] == '>': continue

      header = line[1:].split()[0]
      if header in id_set:
        fout.write(f"{line}" +
                   f"{lines[i+1]}")


if __name__ == "__main__":
  main()