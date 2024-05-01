# note: retrieved from Dr. Fletcher's repo: https://github.com/kfletcher88/SignalP-Combiner

import re
import sys
from pysam import FastaFile
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
import argparse

def main():
  parser = argparse.ArgumentParser(prog='RXLR-EERfromSigP.py', description='A script to identify RXLR and EER motifs from ORFs predicted to be secreted.')
  optional = parser._action_groups.pop()
  required = parser.add_argument_group('Required Arguments')
  oneof = parser.add_argument_group('Provide a SignalP output')
  required.add_argument('-f', '--fasta', help='Fasta file of protein sequences', required=True)
  optional.add_argument('-R', '--RXLRdist', default=80, help='Residues after cleaveage to search for RXLR. Default=80')
  optional.add_argument('-E', '--EERdist',  default=40, help='Residues after RXLR to search for EER. Default=40')
  oneof.add_argument('-6', '--SignalP6', help='SignalP6 output')
  oneof.add_argument('-5', '--SignalP5', help='SignalP5 output')
  oneof.add_argument('-4', '--SignalP4', help='SignalP4 output')
  oneof.add_argument('-3', '--SignalP3', help='SignalP3 output')
  parser._action_groups.append(optional)
  args = parser.parse_args()

  fasta = args.fasta
  sequences_object = FastaFile(fasta)
  RXLRdist = int(args.RXLRdist)
  EERdist = int(args.EERdist)
  dict = {}

  def RXLRsearch():
              found_match = False
              match = re.search(r'R.LR', seq[SPind:SPind+RXLRdist])
              if match and not found_match:
                found_match = True
                first_motif_position = match.start()+SPind
                Ematch = re.search(r'EER', seq[first_motif_position:first_motif_position+EERdist])
                if Ematch:
                  print(header + " RXLR at " + str(match.start()+SPind) + "; EER at " + str(first_motif_position+Ematch.start()))
                  print(seq)
                else:
                  print(header + " RXLR at " + str(match.start()+SPind))
                  print(seq)
              match = re.search(r'(Q|H|G).LR', seq[SPind:SPind+RXLRdist])
              if match and not found_match:
                found_match = True
                first_motif_position = match.start()+SPind
                Ematch = re.search(r'(D|E)(D|E)(R|K)', seq[first_motif_position:first_motif_position+EERdist])
                if Ematch:
                  print(header + " " + match.group(1) + "XLR at " + str(match.start()+SPind) + "; " + Ematch.group() + " at " + str(first_motif_position+Ematch.start()))
                  print(seq)
                else:
                  print(header + " " + match.group(1) + "XLR at " + str(match.start()+SPind))
                  print(seq)
              match = re.search(r'R.L(Q|H|G)', seq[SPind:SPind+RXLRdist])
              if match and not found_match:
                found_match = True
                first_motif_position = match.start()+SPind
                Ematch = re.search(r'(D|E)(D|E)(R|K)', seq[first_motif_position:first_motif_position+EERdist])
                if Ematch:
                  print(header + " RXL" + match.group(1) + " at " + str(match.start()+SPind) + "; " + Ematch.group() + " at " + str(first_motif_position+Ematch.start()))
                  print(seq)
                else:
                  print(header + " RXL" + match.group(1) + " at " + str(match.start()+SPind))
                  print(seq)
              Ematch = re.search(r'(D|E)(D|E)(R|K)', seq[SPind:SPind+RXLRdist+EERdist])
              if Ematch and not found_match:
                  print(header + " no RXLR found; " + Ematch.group() + " at " + str(SPind+Ematch.start()))
                  print(seq)


  if args.SignalP6 is not None:
    ORFID=[]
    SP=[]
    with open(args.SignalP6, 'r') as SP6:
      for line in SP6:
        col = line.strip().split()
        if col[2] == "SP":
          ORFID = col[0]
          SP = col[7][0:3].replace("-","")
          SPind = int(SP)
          seq = sequences_object.fetch(ORFID)
          header = ">" + ORFID + " Cleaved at " + SP +";"
          dict[ORFID] = ORFID
          RXLRsearch()
  if args.SignalP5 is not None:
    ORFID=[]
    SP=[]
    with open(args.SignalP5, 'r') as SP5:
      for line in SP5:
        col = line.strip().split()
        if col[1] == "SP(Sec/SPI)":
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[6][0:3].replace("-","")
            SPind = int(SP)
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()
  if args.SignalP4 is not None:
    ORFID=[]
    SP=[]
    with open(args.SignalP4, 'r') as SP4:
      for line in SP4:
        Csite=False
        col = line.strip().split()
        if col[9] == "Y" and col[1] > col[3]:
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[2]
            SPind = int(SP)
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()
        if col[9] == "Y" and col[1] < col[3]:
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[4]
            SPind = int(SP)
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()
  if args.SignalP3 is not None:
    ORFID=[]
    SP=[]
    with open(args.SignalP3, 'r') as SP3:
      for line in SP3:
        Csite = False
        col = line.strip().split()
        if col[15] == "S":
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[17]
            SPind = int(SP)
            Csite = True
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()
        if col[13] == "Y" and not Csite:
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[2]
            SPind = int(SP)
            Csite = True
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()
        if col[6] == "Y" and not Csite:
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[5]
            SPind = int(SP)
            Csite = True
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()
        if col[9] == "Y" and not Csite:
          ORFID = col[0]
          if ORFID not in dict:
            SP=col[5]
            SPind = int(SP)
            Csite = True
            seq = sequences_object.fetch(ORFID)
            header = ">" + ORFID + " Cleaved at " + SP +";"
            dict[ORFID]=ORFID
            RXLRsearch()

if __name__ == '__main__':
        main()

