"""
ont_fastq_deconcatenate fastq_fix.py
Created on: 9th October, 2018
Proprietary and confidential information of Oxford Nanopore Technologies, Limited
All rights reserved; (c)2018: Oxford Nanopore Technologies, Limited

"""
import logging
import os
import shutil

from Bio import SeqIO

logger = logging.getLogger(__name__)

bad_filename_suffix = '.invalid'


def correct_concatenation_errors(filename):
    """ Check and see if filename is a valid fastq file. If it's not, try and
    identify and correct the specific issue where two fastq records have been
    concatentated.

    The original file will be renamed to "filename.bad" if any corrections are
    applied. This won't necessarily guarantee that all the errors are fixed.

    :param filename: filename to attempt to fix
    :returns: True if the filename was changed, False otherwise
    :rtype: boolean

    """
    try:
        SeqIO.index(filename, 'fastq')
    except ValueError:
        # There are a bunch of different ways that the ValueError we're trying
        # to fix could manifest, so we'll just try and fix the file regardless
        # of what kind of ValueError it is.
        logger.warning('Found invalid fastq file: %s, attempting a fix.',
                       filename)
        return _fix_concatenation_errors(filename)


def _fix_concatenation_errors(filename):
    bad_filename = filename + bad_filename_suffix
    temp_filename = filename + '.tmp'
    fix_failed = False
    bad_file = False
    with open(temp_filename, 'w') as output_file, \
         open(filename, 'r') as input_file:
        next_header = input_file.readline()
        while not next_header.startswith('@'):
            next_header = input_file.readline()
        while next_header:
            if not next_header.startswith('@'):
                # Something's gone wrong -- abort and let the file get
                # quarantined.
                fix_failed = True
                bad_file = True
                break
            header = next_header
            seq = input_file.readline()
            plus = input_file.readline()
            qstring = input_file.readline()
            # There could be a half-complete record at the end of the file
            if not seq or not qstring:
                break
            if len(seq) < len(qstring):
                bad_file = True
                # We'll assume we've got the next header concatenated with the
                # qstring.
                # seq has a newline at the end, hence the -1
                next_header = qstring[len(seq) - 1:]
                qstring = qstring[:len(seq) - 1] + '\n'
            else:
                next_header = input_file.readline()
            for item in [header, seq, plus, qstring]:
                output_file.write(item)

    if fix_failed:
        logger.error('Error while fixing fastq file {}'.format(filename))
        # Clean up
        os.remove(temp_filename)
    else:
        # Replace our original file with the corrected one
        shutil.move(filename, bad_filename)
        shutil.move(temp_filename, filename)

    return bad_file


def quarantine_if_required(filename, quarantine_dir):
    """ Check and see if filename is a valid fastq file.

    :param filename: fastq file to check
    :param quarantine_dir: directory to move the file to if it fails the check

    :returns: True if the file was quarantined, False otherwise
    :rtype: boolean

    """
    needs_quarantine = False
    try:
        SeqIO.index(filename, 'fastq')
    except ValueError as e:
        needs_quarantine = True
        logger.error('Found invalid fastq file: %s -- moving it to quarantine.',
                     filename)
        logger.error(e)
        try:
            os.makedirs(quarantine_dir, exist_ok=True)
        except TypeError:  # Python2 :(
            if not os.path.exists(quarantine_dir):
                os.makedirs(quarantine_dir)
        try:
            shutil.move(filename, quarantine_dir)
            # Quarantine the original (bad) fastq file if possible
            bad_filename = filename + bad_filename_suffix
            if os.path.exists(bad_filename):
                shutil.move(bad_filename, quarantine_dir)
        except shutil.Error:
            logger.error('Failed to move file %s to quarantine', filename)

    return needs_quarantine
