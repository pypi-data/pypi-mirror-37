#!/usr/bin/env python3
"""
ont_fastq_deconcatenate fix_concatenated_fastqs.py
Created on: 9th October, 2018
Proprietary and confidential information of Oxford Nanopore Technologies, Limited
All rights reserved; (c)2018: Oxford Nanopore Technologies, Limited

Provides a simple script to attempt to fix errors in fastq files where two
records have been concatenated together.

e.g.

@id1
AAA
+
\\\@id2
CCC
+
\\\

"""

import argparse
import fnmatch
import glob
import logging
import os

from progressbar import ProgressBar, Bar, SimpleProgress, ETA, Percentage, RotatingMarker

from ont_fastq_deconcatenate import fastq_fix
from ont_fastq_deconcatenate import __version__ as version


def set_up_logger(log_file):
    handler = logging.FileHandler(log_file, 'a')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('ont_fastq_deconcatenate')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def find_and_fix_fastqs(directory, recursive=True):
    logger = set_up_logger(os.path.join(directory,
                                        'ont_fastq_deconcatenate.log'))

    logger.info('ONT fastq deconcatenate version {}'.format(version))
    logger.info('Checking directory {}'.format(directory))
    if recursive:
        logger.info('Also recursively checking sub-directories.')

    files = []
    if recursive:
        for root, dirnames, filenames in os.walk(directory):
            dirnames.sort()
            filenames.sort()
            for filename in fnmatch.filter(filenames, '*.fastq'):
                files.append(os.path.abspath(os.path.join(root, filename)))
    else:
        files = [os.path.abspath(x) 
                 for x in glob.glob(os.path.join(directory, '*.fast5'))]
    bad_fastqs = 0
    quarantined_fastqs = 0
    logger.info('Found {} fastq files'.format(len(files)))

    bar_format = [RotatingMarker(), " ", SimpleProgress(), Bar(), Percentage(),
                  " ", ETA()]
    pbar = ProgressBar(maxval=len(files), widgets=bar_format).start()

    for index, filename in enumerate(files):
        if fastq_fix.correct_concatenation_errors(filename):
            bad_fastqs += 1
        # We might have quarantined the file if something went wrong during fixing
        if (os.path.exists(filename) and
                fastq_fix.quarantine_if_required(filename)):
            quarantined_fastqs +=1
        pbar.update(index)
    pbar.finish()
    logger.info('Attempted to fix {} fastq files.'.format(bad_fastqs))
    logger.info('Quarantined {} fastq files '
                'afterwards.'.format(quarantined_fastqs))


def main():
    argparser = argparse.ArgumentParser(description='ONT fastq deconcatenation '
                                        'tool')
    argparser.add_argument('-i', '--input', required=True, help='Input folder')
    argparser.add_argument('-r', '--recursive', default=True,
                           action='store_true', help='Input folder')
    
    args = argparser.parse_args()
    find_and_fix_fastqs(args.input, args.recursive)

if __name__ == '__main__':
    main()
