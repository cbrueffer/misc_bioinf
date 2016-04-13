misc_bioinf
===========

Repository for miscellaneous bioinformatics scripts that may be useful to others.


maf2annovar.py
--------------

Converts a file in MAF format (e.g., from TCGA mutation calling) into the [Annovar](http://annovar.openbioinformatics.org) input format.

Compatible with Python 2 and 3; no external dependencies.


liftover_annovar.py
-------------------

Converts the genomic coordinates in an Annovar input file over to a new reference genome using the [UCSC liftOver](https://genome.ucsc.edu/cgi-bin/hgLiftOver) commandline tool.

Compatible with Python 2 and 3; depends on the [pandas](http://pandas.pydata.org/) library.


fix_tophat_unmapped_reads.py
----------------------------

This script has been renamed to ```tophat-recondition ``` and moved to its own repository here: [https://github.com/cbrueffer/tophat-recondition](https://github.com/cbrueffer/tophat-recondition)
