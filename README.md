# Enriching Bibliographic Records in Alma with Tables of Content

When a table of content should added to enrich a bibliographic record, this script automates the process. It uploads the file to a public server and adds a 856 field to the bibliographic record in Alma, generating a link in the discovery system.

## Description

As soon as the scanned pdf-file (named ```barcode.pdf```, where ```barcode``` is the actual barcode ot the bibliographic item) is placed in a folder on a computer or on Sharepoint, the script will upload it to a public server, rename it to ```mms-id.pdf``` (where ```mms-id``` is the NZ MMS-ID of the record) and add a field 856 to the MARC21 record in Alma.

## Getting Started

### Dependencies

The following python modules are required for the script to run:
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

* Download all files
* Create a .env file with the following parameters:
```
ÀPI_URL=""
API_KEY=""

EMAIL_PASS=""

FTP_URL=""
FTP_USER=""
FTP_PASS=""
```

### Executing program

* This is how to run the script from the command line on MacOS:
```
python3 enrich.py -f toc/BM2064150.pdf -l win
```
* This is how to run the script from the command line on Windows:
```
python enrich.py -f toc/BM2064150.pdf -l win
```
* The relative path to the pdf-file including its name must be suplied in the -f parameter.
* The code for the library for the pdf-file must be suplied in the -l parameter.

## Help

* This is how to show the help message on MacOS:
```
python3 enrich.py -h
```
* This is how to show the help message on Windows:
```
python enrich.py -h
```

## Authors

This script was created by Rhodijn (zolo) for ZHAW HSB inside the CAS Data Management and Information Technologies at the University of Zurich.

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](https://github.com/rhodijn/toc/blob/main/LICENSE.md) file for details
