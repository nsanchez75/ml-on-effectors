import requests
import sys
import os
import json

def get_pdb_url(sequence):
    """Fetch the PDB URL from the AlphaFold Protein Structure Database given any sequence.

    Args:
        sequence: The protein sequence to fetch the PDB URL for.

    Returns:
        The URL to the PDB file.
    """

    url = f"https://alphafold.ebi.ac.uk/api/prediction/{sequence}"
    headers = {
        "accept": "application/json",
        "key": "AIzaSyCeurAJz7ZGjPQUtEaerUkBZ3TaBkXrY94",  # There is no official API access. This is a working fake API key. If it stops working becuase you're rejected, let me know and I'll make another.
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            latest_model = data[-1]  # Some models have been rerun if there were problems originally -- this only takes the most recenty one
            return latest_model.get('pdbUrl')
    return None

def download_pdb(pdb_url, output_file):
    """Download the PDB file from the provided URL.

    Args:
        pdb_url: The URL to download the PDB file from.
        output_file: The path to the output file.
    """

    response = requests.get(pdb_url)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download PDB file from {pdb_url}.")

def main():
    """Downloads the PDBs for the protein sequences specified in the file given as the first argument. 
    Saves the downloaded PDBs in the directory specified as the second argument."""

    if len(sys.argv) != 3:
        print("Usage: python script.py sequences_file output_dir")
        return

    sequences_file = sys.argv[1]
    output_dir = sys.argv[2]

    with open(sequences_file, "r") as f:
        for line in f:
            try:
                sequence = line.strip().split(':')[1]
            except IndexError:
                sequence = line.strip()
            
            pdb_url = get_pdb_url(sequence)
            if pdb_url is not None:
                output_file = os.path.join(output_dir, sequence + ".pdb")
                download_pdb(pdb_url, output_file)
            else:
                print(f"Failed to get PDB URL for sequence {sequence}.")
            
            
if __name__ == "__main__":
    main()
