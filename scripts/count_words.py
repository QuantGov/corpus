#!/usr/bin/env python
"""
count_words.py: count the number of words for each item in a corpus
"""
import platform
import argparse
import csv
import io
import logging
import re
import sys

import quantgov

from pathlib import Path

ENCODE_IN = 'utf-8'
ENCODE_OUT = 'utf-8'

WORD_REGEX = re.compile(r'\b\w+\b')

log = logging.getLogger(Path(__file__).stem)

def process_or_thread():
    worker_os = platform.system()
    if worker_os in ['Darwin', 'Linux']:
        worker_type = 'thread'
        return worker_type
    if worker_os in ['Windows']:
        worker_type = 'process'
        return worker_type

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('driver', type=Path)
    parser.add_argument('-o', '--outfile',
                        type=lambda x: open(
                            x, 'w', encoding=ENCODE_OUT, newline=''),
                        default=io.TextIOWrapper(
                            sys.stdout.buffer, encoding=ENCODE_OUT)
                        )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_const',
                           const=logging.DEBUG, default=logging.INFO)
    verbosity.add_argument('-q', '--quiet', dest='verbose',
                           action='store_const', const=logging.WARNING)
    return parser.parse_args()


def count_words(doc):
    return doc.index, len(WORD_REGEX.findall(doc.text))


def main():
    args = parse_args()
    logging.basicConfig(level=args.verbose)
    driver = quantgov.load_driver(args.driver)
    writer = csv.writer(args.outfile)
    worker_type = process_or_thread()
    writer.writerow(driver.index_labels + ('words',))
    for docindex, count in quantgov.utils.lazy_parallel(
            count_words, driver.stream(), worker=worker_type):
        writer.writerow(docindex + (count,))


if __name__ == "__main__":
    main()
