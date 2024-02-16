import sys
import os
import torch
import esm

from argparse import ArgumentParser, FileType

def parse_fasta(fasta_contents:list[str])->list[tuple[str, str]]:
  proteins = list()
  while (line := next(fasta_contents, False)):
    if line[0] != '>':
      continue

    header = line[1:].split()[0]
    sequence = next(fasta_contents)
    proteins.append((header, sequence))
  
  return proteins


def main():
  parser = ArgumentParser(prog="A Python script to run ESMFold on ORFs.")
  parser.add_argument("--input_fasta", '-i', type=FileType('r'), help="Input FASTA file containing ORF sequences", required=True)
  fasta_contents = parser.parse_args().input_fasta.read().splitlines()


if __name__ == "__main__":
  main()
