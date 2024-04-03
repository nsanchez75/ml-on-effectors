from argparse import ArgumentParser
from time import sleep
import os
from shutil import rmtree
import torch
import esm

def parse_fasta(file_path):
    with open(file_path, "r") as f:
        entries = f.read().split(">")[1:]
        proteins = [(entry.split("\n", 1)[0], entry.split("\n", 1)[1].replace("\n", "")) for entry in entries]
    return proteins

def set_chunk_size_based_on_length(length):
    if length < 700:
        return 128
    elif 700 <= length <= 1100:
        return 128
    else:
        return 64


if __name__ == "__main__":
    parser = ArgumentParser(prog="Python script that runs ESM on kakawa")
    parser.add_argument("-i", "--input_fasta", type=str, required=True, help="Input FASTA file")
    parser.add_argument("-o", "--output_directory", type=str, default="ESM_kakawa_results", help="Output directory")
    args = parser.parse_args()
    INFILE:str = args.input_fasta
    if not os.path.exists(INFILE):
        print(f"Error: Input file {INFILE} does not exist.")
        exit(1)
    OUTDIR:str = args.output_directory
    if os.path.exists(OUTDIR):
        print(f"Warning: Output directory {OUTDIR} detected. Replacing its contents in 3 seconds...")
        sleep(3)
        rmtree(OUTDIR)
    os.mkdir(OUTDIR)

    model = esm.pretrained.esmfold_v1()
    model = model.eval().cuda()
    proteins = parse_fasta(INFILE)

    with torch.no_grad():
        for name, sequence in proteins:
            chunk_size = set_chunk_size_based_on_length(len(sequence))
            if chunk_size is not None:
                model.set_chunk_size(chunk_size)
            output = model.infer(sequence,
                                 num_recycles=3, # hard=coded
                                 chain_linker="X"*25, # hard-coded
                                 residue_index_offset=512)
            ptm = output["ptm"][0]
            with open(os.path.join(OUTDIR, f"{name}_{ptm}.pdb"), "w") as f:
                f.write(model.output_to_pdb(output)[0])
