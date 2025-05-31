# Enriching Bibliographic Records in Alma with Tables of Content

When a table of content should added to enrich a bibliographic record, this script automates the process. It uploads the file to a public server and adds a 856 field to the bibliographic record in Alma, generating a link in the discovery system.

## Description

As soon as the scanned pdf-file (named ```barcode.pdf```, where ```barcode``` is the actual barcode ot the bibliographic item) is placed in a folder on a computer or on Sharepoint, the script will upload it to a public server and add a 856 field to the MARC21 record in Alma.

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

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

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

This script was created by Rhodijn (zolo) for ZHAW HSB inside the CAS Data Management and Information Technologies at University of Zurich

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](https://github.com/rhodijn/toc/blob/main/LICENSE.md) file for details
