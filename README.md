# Enriching Bibliographic Records in Alma with Tables of Content
```
###################
##                 ##
##               ##
  ######       ##
    ##       ######
  ##               ##
##                 ##
  ###################
```
When a table of content should be added to enrich a bibliographic record, this script automates the process. It uploads the pdf-file to a public server and adds a 856 field to the bibliographic record in Alma, generating a link in the discovery system.

## Description

As soon as the scanned pdf-file (named `barcode.pdf`, where `barcode` is the actual barcode ot the bibliographic item) is placed in a folder on a computer or on Sharepoint, the script will upload it to a public server, rename it to `mms-id.pdf` (where `mms-id` is the NZ MMS-ID of the record) and add a field 856 to the MARC21 record in Alma.

## Getting Started

### Dependencies

The following python modules are required for the script to run (a `requirements.txt` is included):
* argparse
* datetime
* dotenv
* json
* lxml
* paramiko
* os
* re
* smtplib
* ssl
* sys

### Installing

* Download all files.
* Create empty folders named `log`, `temp` and `xml` in the root directory.
* Rename the file `.env.example` to `.env` and submit your credentials inside the quotes:
```
API_URL=""
API_KEY=""

EMAIL_PASS=""

FTP_URL=""
FTP_USER=""
FTP_PASS=""
```
* You need to adjust some values in `data/config.json`:
  * update `{"email": {"from": ""}}` wich the sender address of the enrichment report
  * update `{"email": {"to": ""}}` with the address which should receive the enrichment report
  * update `{"path": {"r": ""}}` witch the remote path on your ftp server
  * update `{"library": {}}` with keys which are the parameters you will use als -l parameter and values which are the corresponding subfolders on the remote server

### Execute the script

* This is how to run the script from the command line on MacOS (replace `toc/BM2064150.pdf` and `win`with your values):
```
python3 enrich.py -f toc/BM2064150.pdf -l win
```
* This is how to run the script from the command line on Windows (replace `toc/BM2064150.pdf` and `win`with your values):
```
python enrich.py -f toc/BM2064150.pdf -l win
```
* The relative path to the pdf-file including its name must be suplied by passing a parameter `-f` or `--file`.
* The code for the library for the pdf-file must be suplied by passing a parameter `-l` or `--lib`.

## Help

* To show the help message on MacOS enter:
```
python3 enrich.py -h
```
* To show the help message on Windows enter:
```
python enrich.py -h
```
If this doesn't help, feel free to contact me.

## Author

This script was created by Rhodijn (zolo) for ZHAW HSB inside the 2025 CAS Data Management and Information Technologies at the University of Zurich.

## Version History

* 1.0
    * Initial Release (2025-06-17)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](https://github.com/rhodijn/toc/blob/main/LICENSE.md) file for details.
