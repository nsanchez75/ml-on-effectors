import os
import sys
import re
from Bio.SeqIO import parse

USAGE = "python3 find_rxlr.py <FASTA file>"

# RXLR strings
RXLR_R1 = "R.LR"
RXLR_R2 = "[RKHGQ].[LMYFIV][RNK]"
## Kyle's string searches
RXLR_R3 = "[GHQ].LR"
RXLR_R4 = "R.L[GKQ]"
## combining Kyle's string search ideas
RXLR_R5 = "[RGHQ].L[RGKQ]"

RXLR_REGEXES = [RXLR_R1, RXLR_R2, RXLR_R3, RXLR_R4, RXLR_R5]

# EER strings
EER_R1 = "[ED][ED][KR]"

EER_REGEXES = [EER_R1]

def index_all_matches(sequence, regex):
  return [match.start() for match in re.compile(regex).finditer(sequence)]

def main():
  FASTA = sys.argv[1]
  if not os.path.exists(FASTA) or not FASTA[FASTA.rfind('.')+1:] in {"faa", "fasta"}:
    print(USAGE)
    exit(1)

  has_rxlr = dict()
  has_eer = dict()
  has_rxlr_and_eer = [] # note: first possible RXLR has to be before last possible EER
  for sequence in parse(FASTA, "fasta"):
    # TODO add user specifications for this
    POST_SP_START = 19
    POST_SP_END = min(POST_SP_START + 60, len(sequence))
  
    post_sp_seq = str(sequence.seq[POST_SP_START:POST_SP_END])
    
    # determine if sequence has RXLR (and which match did it achieve)
    lowest_rxlr = None
    for i, regex in enumerate(RXLR_REGEXES):
      rxlr_match = index_all_matches(post_sp_seq, regex)
      if rxlr_match:
        try:
          has_rxlr[sequence.id].append(i)
        except KeyError:
          has_rxlr[sequence.id] = [i]
        if not lowest_rxlr or lowest_rxlr[0] > rxlr_match[0]: lowest_rxlr = (rxlr_match[0], i)
    
    # determine if sequence has EER (and which did it achieve)
    highest_eer = None
    for i, regex in enumerate(EER_REGEXES):
      eer_match = index_all_matches(post_sp_seq, regex)
      if eer_match:
        try:
          has_rxlr[sequence.id].append(i)
        except KeyError:
          has_rxlr[sequence.id] = [i]
        if not highest_eer or highest_eer[0] > eer_match[-1]: highest_eer = (eer_match[-1], i)
  
    # determine if RXLR-EER is found in sequence
    if (lowest_rxlr and highest_eer) and lowest_rxlr[0] < highest_eer[0]:
      has_rxlr_and_eer.append((sequence.id, lowest_rxlr[1], highest_eer[1]))

  with open("has_rxlr.txt", 'w') as frxlr:
    frxlr.write(f"")
    for seq_id, regex_matches in has_rxlr.items():
      list_of_regex_booleans = [0] * len(RXLR_REGEXES)
      for index in regex_matches:
        list_of_regex_booleans[index] = 1
      frxlr.write(f"{seq_id}\t{'\t'.join(list_of_regex_booleans)}\n")

    for _ in has_rxlr:
      frxlr.write(f"{_[0]}\t{_[1]}\n")

  with open("has_eer.txt", 'w') as feer:
    for _ in has_eer:
      feer.write(f"{_[0]}\t{_[1]}\n")

  with open("has_rxlr_and_eer.txt", 'w') as frxlreer:
    for _ in has_rxlr_and_eer:
      frxlreer.write(f"{_[0]}\t{_[1]}\t{_[2]}\n")


if __name__ == "__main__":
  main()
