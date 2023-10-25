# ESMFold Tests

## Using ESMFold API

Created a Python program that tried to use the ESMFold API (https://esmatlas.com/about)

Code Example from website:

```bash
curl -X POST --data "GENGEIPLEIRATTGAEVDTRAVTAVEMTEGTLGIFRLPEEDYTALENFRYNRVAGENWKPASTVIYVGGTYARLCAYAPYNSVEFKNSSLKTEAGLTMQTYAAEKDMRFAVSGGDEVWKKTPTANFELKRAYARLVLSVVRDATYPNTCKITKAKIEAFTGNIITANTVDISTGTEGSGTQTPQYIHTVTTGLKDGFAIGLPQQTFSGGVVLTLTVDGMEYSVTIPANKLSTFVRGTKYIVSLAVKGGKLTLMSDKILIDKDWAEVQTGTGGSGDDYDTSFN" https://api.esmatlas.com/foldSequence/v1/pdb/
```

This doesn't work because ESMFold API has a limited amount of usage at a time. We have to use Google Colab or ESMFold repository.

Update 10/25/2023: There's a curl issue so the code definitely doesn't work on my own computer for some reason. Maybe test on lab servers?

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

## Experiments: Data & Results

### 10/25/2023

- used `api_create_esmfolds.py` on a small FASTA file (also edited the script to warn the user that the FASTA file must be small or else the API won't work)
- encountered a curl issue that is preventing the script to work (error pasted below). I guess I'll be using Colab instead.

```text
Running ESMFold fold prediction on RXLR3...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
Successfully ran ESMFold fold prediction on RXLR3.
Running ESMFold fold prediction on RXLR3B...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
Successfully ran ESMFold fold prediction on RXLR3B.
```

- copied ESMFold Colab onto my school Google Drive (Michelmore Lab / ML Colabs Folder) and ran the sequences on it
  - made sure to omit the '*' at the end of the sequences
  - didn't run ESMFold with optional code blocks (things about the color of the plots and the plot confidence). Maybe use them next time?
- results found in 10/25/2023 (obviously)
