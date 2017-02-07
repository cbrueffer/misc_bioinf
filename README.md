misc_bioinf
===========

Repository for miscellaneous bioinformatics scripts that may be useful to others.


maf2annovar.py
--------------

Converts a file in MAF format (e.g., from TCGA mutation calling) into the [Annovar](http://annovar.openbioinformatics.org) input format.

Compatible with Python 2 and 3; no external dependencies.

```
usage: maf2annovar.py [-h] [-d] -m MAF_FILE [-v]

Convert a MAF file to Annovar input format.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug output
  -m MAF_FILE, --maf_file MAF_FILE
                        File in MAF format
  -v, --version         show program's version number and exit
```

liftover_annovar.py
-------------------

Converts the genomic coordinates in an Annovar input file over to a new reference genome using the [UCSC liftOver](https://genome.ucsc.edu/cgi-bin/hgLiftOver) commandline tool.

Compatible with Python 2 and 3; depends on the [pandas](http://pandas.pydata.org/) library.

This script requires a liftOver file in [chain format](https://genome.ucsc.edu/goldenpath/help/chain.html) that maps coordinates between the old and new reference genome.  Chain files for many genomes are available from [UCSC](http://hgdownload.cse.ucsc.edu/downloads.html).

```
usage: liftover_annovar.py [-h] [-d] [-v] -c CHAINFILE -i INFILE [-l LIFTOVER]
                           [-w WORKDIR]

Lift over a file in Annovar format to a new reference genome. Extra columns are
preserved.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable debug mode
  -v, --version         show program's version number and exit
  -c CHAINFILE, --chainfile CHAINFILE
                        liftOver chain file (available from UCSC)
  -i INFILE, --infile INFILE
                        file in Annovar input format (chromosome, start, end,
                        ref_allele, var_allele, ...)
  -l LIFTOVER, --liftover LIFTOVER
                        path to the liftOver binary (default: system PATH)
  -w WORKDIR, --workdir WORKDIR
                        work directory (default: directory containing INFILE)
```


fix_tophat_unmapped_reads.py
----------------------------

This script has been renamed to ```tophat-recondition ``` and moved to its own repository here: [https://github.com/cbrueffer/tophat-recondition](https://github.com/cbrueffer/tophat-recondition)
