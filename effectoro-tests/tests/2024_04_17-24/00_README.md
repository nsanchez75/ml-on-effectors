# 4/17/2024

I am going to try to construct a new method for determining if a sequence contains a motif. I discovered MEME Suite, which is a module already installed in the lab server. The command to get the commands is `meme -h`. Here is the [MEME Suite webpage](https://meme-suite.org/meme/index.html).

From the MEME Suite homepage I learned about FIMO (Find Individual Motif Occurrences) and MAST (Motif Alignment & Search Tool). For the purposes of this project, I will be using MAST as it will allow me to simply determine whether or not a motif can be found in a protein sequence. The command to run MAST, assuming that MEME Suite is loaded, is `mast ...`).

Instead of working with MEME for now, I have downloaded and tried Dr. Fletcher's script that I found through the GitHub repository search function when trying to find RXLR search scripts. The script is called `RXLR-EERfromSigP.py`.

```bash
python3 RXLR-EERfromSigP.py -f B_lac-SF5.protein.fasta
```

To get rid of all asterisks at the end of sequences, I am using this command:

```bash
sed -i 's/\*$//' B_lac-SF5.protein.fasta
```
