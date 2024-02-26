import sys
import os
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
    if len(sys.argv) < 3:
        print("Usage: python script.py <fasta_file_path> <output_directory>")
        sys.exit(1)

    fasta_file_path = sys.argv[1]
    output_directory = sys.argv[2]
    
    model = esm.pretrained.esmfold_v1()
    model = model.eval().cuda()
    proteins = parse_fasta(fasta_file_path)

    # Create output directory if it does not exist
    os.makedirs(output_directory, exist_ok=True)

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
            with open(os.path.join(output_directory, "{}_{}.pdb".format(name, ptm)), "w") as f:
                f.write(model.output_to_pdb(output)[0])
