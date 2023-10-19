# ESMFold Tests

## Using ESMFold API

Created a Python program that tried to use the ESMFold API (https://esmatlas.com/about)

Code Example from website:

```bash
curl -X POST --data "GENGEIPLEIRATTGAEVDTRAVTAVEMTEGTLGIFRLPEEDYTALENFRYNRVAGENWKPASTVIYVGGTYARLCAYAPYNSVEFKNSSLKTEAGLTMQTYAAEKDMRFAVSGGDEVWKKTPTANFELKRAYARLVLSVVRDATYPNTCKITKAKIEAFTGNIITANTVDISTGTEGSGTQTPQYIHTVTTGLKDGFAIGLPQQTFSGGVVLTLTVDGMEYSVTIPANKLSTFVRGTKYIVSLAVKGGKLTLMSDKILIDKDWAEVQTGTGGSGDDYDTSFN" https://api.esmatlas.com/foldSequence/v1/pdb/
```

This doesn't work because ESMFold API has a limited amount of usage at a time. We havve to use Google Colab or ESMFold repository.

## Using ESMFold Colab

Tried to run ESMFold Colab through Google Colab browser. Had issues with inputting the FASTA file:

- would download FASTA file to Google Colab
- couldn't resolve it so kinda just gave up on it

## Using ESMFold Github Repo

Tried to download repo, create Conda environment, etc.

Ran into an issue with "OpenFold" module not being able to be downloaded.

## Using Ian Anderson's Code

### Before 10/19/2023

Tried running Anderson's code. However, "OpenFold" module issue is happening again.

Found an email from Kelsey about working ssh into Kakawa so I'll try to run the code on Kakawa instead

**TODO: SSH into Kakawa**
