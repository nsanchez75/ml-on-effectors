#!/usr/bin/python3
import sys
import re
import os
from Bio import SeqIO

def main():

    if len(sys.argv) < 2:
        print("run with: \npython regex_searcher.py <input_fasta_path>")
        exit(0) 

    try: fh = sys.argv[1]
    except: 
        print("run with: \npython regex_searcher.py <input_fasta_path>")
        print("trouble accessing file: ", fh)
        exit(0)

    if not os.path.isfile(fh):
        print("run with: \npython regex_searcher.py <input_fasta_path>")
        print("trouble accessing file: ", fh)
        exit(0) 

    full_path = os.path.abspath(fh)
    #print("\n using this file: ", full_path)

    #print("\n~ input your regex to search, in REGEX format ~")
          
    #print("\n examples:") 
   # print("\n    R\\\wLR                    = strict RXLR")
   # print("\n    ^\\w{1,56}R\\\wLR          = strict RXLR from position 1 to 60")
   # print("\n    [E|D][E|D][R|K]            = lenient EER")
   # print("\n    ^\\\w{1,97}[E|D][E|D][R|K] = lenient EER, from position 1 to 100")

    #regex_inp = input("\n\n >input: ").strip("\n")

    #print("\n~using this REGEX pattern: " , regex_inp , " ~\n")

    #print("sequence_name", "sequence", "rxlr position", "rxlr motif", "eer position," 
      #      "eer motif", sep=',')

    for record in SeqIO.parse(full_path, "fasta"):
        rxlr_results = []
        eer_results = []

        rxlr_results.append(re.search("[R|Q|G|H].LR", str(record.seq)))

        eer_results.append(re.search("[D|E][D|E][K|R]", str(record.seq)))

        rxlr_res = None
        eer_res = None

        for res in rxlr_results:
            if res == None or res.start() > 96:
                pass

            else:
                rxlr_res = True

        for res in eer_results:
            if res == None or res.start() > 97:
                pass

            else:
                eer_res = True 

        if rxlr_res == True and eer_res == True: 
            print(record.id)

        
if __name__ == "__main__":
    main()
