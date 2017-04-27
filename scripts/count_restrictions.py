#!/usr/bin/env python
"""
count_restrictions.py: count the number of restriction words for each item in a
corpus
"""
import platform
import argparse
import collections
import csv
import io
import logging
import re
import sys

import quantgov

from pathlib import Path

ENCODE_OUT = 'utf-8'

RESTRICTIONS = ('shall', 'must', 'may not', 'required', 'prohibited')
PATTERN = re.compile(r'\b(?P<match>{})\b'.format('|'.join(RESTRICTIONS)))

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


def count_restrictions(document):
    """
    For a single quantgov.corpora.Document object, return the number of
    regulatory restrictions in the text.
    """
    text = ' '.join(document.text.split()).lower()
    restrictions = collections.Counter(
        i.groupdict()['match'] for i in PATTERN.finditer(text)
    )
    return document.index, restrictions


def main():
    args = parse_args()
    logging.basicConfig(level=args.verbose)
    driver = quantgov.load_driver(args.driver)
    writer = csv.writer(args.outfile)
    worker_type = process_or_thread()
    writer.writerow(driver.index_labels + RESTRICTIONS + ('restrictions',))
    for docind, counts in quantgov.utils.lazy_parallel(
            count_restrictions, driver.stream(), worker=worker_type):
        writer.writerow(
            docind + tuple(counts[i] for i in RESTRICTIONS) +
            (sum(counts.values()),)
        )


if __name__ == "__main__":
    main()
