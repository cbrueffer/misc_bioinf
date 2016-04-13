#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script rebases a file in Annovar format to a new reference genome using
UCSC liftOver.

@author: Christian Brueffer (ORCID: 0000-0002-3826-0989)

Home:    https://github.com/cbrueffer/misc_bioinf/
License: https://github.com/cbrueffer/misc_bioinf/LICENSE.md
"""

from __future__ import print_function

import pandas as pd

COL_CHROM = 0
COL_START = 1
COL_END = 2
COL_REF_ALLELE = 3
COL_VAR_ALLELE = 4


def exec_cmd(command, log=True):
    """Executes a given commandline and prints the command output to stdout."""
    import subprocess

    try:
        s = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        while True:
            line = s.stdout.readline()
            if not line:
                break
            if log:
                print(line, end='')
    except:
        raise


def liftover_annovar(annovarfile, chainfile, workdir=None, liftover='liftOver',
                     sep='\t'):
    """Convert the genomic coordinates in an Annovar-compatible file to
    a new reference genome using UCSC liftOver.
    """
    if not workdir:
        workdir = os.path.dirname(annovarfile)

    print("Using workdir:", workdir)

    liftover_infile = os.path.join(workdir, 'liftover_input.txt')
    liftover_lifted_file = os.path.join(workdir, 'liftover_lift_ok.txt')
    liftover_failed_file = os.path.join(workdir, 'liftover_lift_failed.txt')
    outfile_lifted = annovarfile + ".liftok"
    outfile_failed = annovarfile + ".liftfail"

    df_in = pd.read_csv(annovarfile, header=None, sep=sep)

    col_position = len(df_in.columns)

    # add a new column with genome positions
    df_in[col_position] = df_in.apply(lambda row: "chr%s:%i-%i" %
        (row[COL_CHROM], row[COL_START], row[COL_END]), axis=1)

    # write the liftOver input file containing only genome positions
    df_in[col_position].to_csv(liftover_infile, index=False, header=False)

    # build liftOver command line and execute
    liftover_cmd = [liftover, "-positions", liftover_infile, chainfile,
                    liftover_lifted_file, liftover_failed_file]

    try:
        exec_cmd(liftover_cmd)

        # read the successfully lifted locations
        with open(liftover_lifted_file) as infile:
            liftover_ok = infile.read().splitlines()
        # read the locations failed to lift over
        with open(liftover_failed_file) as infile:
            liftover_failed = infile.read().splitlines()
            # remove comments
            liftover_failed = [s for s in liftover_failed if s.startswith("#")]
    except:
        raise

    # Throw out input locations that failed to lift.  For the rest we update
    # coordinates to the lifted ones.
    df_out_lifted = df_in[~df_in[col_position].isin(liftover_failed)]

    # Drop the position column, as the filtering it was needed for is done.
    df_out_lifted = df_out_lifted.drop(df_out_lifted.columns[[col_position]],
                                       axis=1)

    # remove chr prefix
    liftover_ok = [s.replace("chr", "") for s in liftover_ok]
    # split into a data frame with three columns (chr, start, end)
    liftover_ok_df = pd.DataFrame([s.replace("-", ":").split(":") for s in liftover_ok])

    # update genomic location in the output frame and write it
    df_out_lifted[[COL_CHROM, COL_START, COL_END]] = liftover_ok_df
    df_out_lifted.to_csv(outfile_lifted, sep="\t", index=False, header=False)

    # write the input lines that failed to lift over
    df_out_failed = df_in[df_in[col_position].isin(liftover_failed)]
    df_out_failed.to_csv(outfile_failed, sep="\t", index=False, header=False)

    print()
    print('Locations in input file:  ', len(df_in.index))
    print('Locations lifted:         ', len(liftover_ok))
    print('Locations failed to lift: ', len(liftover_failed))
    print()
    print("Lifted annovar file (new coordinates):             ", outfile_lifted)
    print("File with failed to lift entries (old coordinates):", outfile_failed)


if __name__ == "__main__":
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(description='Lift over a file in Annovar'
                                     'format to a new reference genome.  Extra columns are preserved.')
    parser.add_argument("-d", "--debug", action='store_true',
                        help="enable debug mode")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")
    parser.add_argument("-c", "--chainfile", required=True,
                        help="liftOver chain file (available from UCSC)")
    parser.add_argument("-i", "--infile", required=True,
                        help="File in Annovar input format (chromosome, start,"
                        "end, ref_allele, var_allele, ...)")
    parser.add_argument("-l", "--liftover", default="liftOver",
                        help="path to the liftOver binary (default: system PATH)")
    parser.add_argument("-w", "--workdir", default=None,
                        help="Work directory (default: directory containing INFILE)")
    args = parser.parse_args()
    #args = parser.parse_args('-d --chainfile hg19ToHg38.over.chain --infile test_liftover.txt'.split())

    for f in [args.infile, args.chainfile]:
        if not os.path.exists(f) or not os.path.isfile(f):
            print("Input file cannot be read: %s" % f, file=sys.stderr)
            sys.exit(1)

    # check whether the liftOver binary is available
    try:
        exec_cmd([args.liftover], log=False)
    except OSError as e:
        print("liftOver binary cannot be executed:", str(e), file=sys.stderr)
        sys.exit(1)

    try:
        liftover_annovar(args.infile, args.chainfile, workdir=args.workdir,
                         liftover=args.liftover)
    except KeyboardInterrupt:
        print("Program interrupted by user, exiting.")
    except Exception as e:
        if args.debug:
            import traceback
            print(traceback.format_exc())

        print('Error: %s' % str(e), file=sys.stderr)
