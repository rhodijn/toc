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
* Create a .env file with the following content:
```
ÀPI_URL=""
API_KEY=""

EMAIL_PASS=""

FTP_URL=""
FTP_USER=""
FTP_PASS=""
```
* Create a subfolder ```data``` with two files, ```config.json```:
```
{
    "api": {
        "get": "?view=full&expand=p_avail",
        "put": "?validate=true&override_warning=true&override_lock=true&stale_version_check=false&cataloger_level=20&check_match=false",
        "j": "json",
        "x": "xml",
        "header": {
            "Accept": "application/xml",
            "Content-Type": "application/xml"
        }
    },
    "email": {
        "from": "",
        "to": ""
    },
    "ftp": {
        "port":
    },
    "path": {
        "d": "",
        "h": "",
        "l": "",
        "r": "",
        "t": ""
    },
    "library": {
        "wae": "",
        "win": ""
    }
}
```
and ```log.json``` which is the template for the log file:
```
{
    "mms-id": {
        "iz": null,
        "nz": null
    },
    "dt": null,
    "url": null,
    "filename": {
        "local": null,
        "remote": null
    },
    "valid": {
        "file": false,
        "lib": false
    },
    "file_uploaded": false,
    "link_tested": false,
    "file_deleted": false,
    "added_856": false,
    "messages": [],
    "requests": []
}
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
If this doesn't help, feel free to contact me.

## Authors

This script was created by Rhodijn (zolo) for ZHAW HSB inside the CAS Data Management and Information Technologies at the University of Zurich.

## Version History

* 1.0
    * Initial Release (2025-06-10)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](https://github.com/rhodijn/toc/blob/main/LICENSE.md) file for details
