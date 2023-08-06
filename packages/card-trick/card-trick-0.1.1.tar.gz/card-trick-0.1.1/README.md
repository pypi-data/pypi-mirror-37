# Card trick
A software package that extracts confers_resistance_to_drug relationships from 
The Comprehensive Antibiotic Resistance Database (CARD) https://card.mcmaster.ca/home

## Installation
This package requires Python3
```
pip3 install card-trick
```

## Usage
usage: card-trick [-h] [-v] {update,search} ...

positional arguments:
  {update,search}  The following commands are available. Type contig_tools
                   <COMMAND> -h for more help on a specific commands
    update         Get latest CARD ontology
    search         search CARD ontology

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    display the version number

### Update ontology database
The software comes preloaded with version 3.0.0 of the database (October 2018 release).
The update command `card-trick update` will download the latest version of the database and store it in your
home directory in the .card-trick directory

### Search ontology database
This will return matches to the STDOUT in either tsv (default) or json format. To write to a file just append `> OUTPUT_FILE` to the command

Specify a full or partial gene name with the -g argument to search for antibiotics resistance to which is conferred by the specified gene e.g
```
card-trick search -g ctx
```
This will return the following output
```
gene	antibiotics
CTX-M-3	cefalotin,ceftazidime,ceftriaxone
CTX-M-15	ceftazidime
CTX-M-27	cefalotin,ceftazidime
CTX-M-55	ceftazidime,ceftriaxone
```

Specify a full or partial antibiotic name with the -a argument to search for genes who confer resistance to the specified antibiotic
```
card-trick search -a tigecycline
```
This will return the following output
```
antibiotic	genes
tigecycline	AcrAB-TolC,AdeABC,mepA,oqxAB,tet(A),tetX
```

## Using in a python script or program
Examples
```
import card_trick
genes_conferring_resistance = card_trick.ontology_functions.search_antibiotics('tigecycline')
antibiotics = card_trick.ontology_functions.search_genes('ctx-m-15')
```
