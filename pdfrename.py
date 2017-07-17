#!/usr/bin/python3
"""
Rename a PDF with information taken from its metadata.
"""

import argparse
import datetime
import chardet
import os
import re
import sys
import time

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument


def makesafe(s):
    """
    Make a safe filename by replacing spaces with a separator, and removing non-word characters.
    >>> makesafe('Foo bar?')
    'Foo_bar'
    """
    s = re.sub('\s+', '_', s)
    s = re.sub('\W', '', s)
    s = re.sub('_{2,}', '_', s)
    return s

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--surname', action='store_true')
    parser.add_argument('--date', action='store_true')
    parser.add_argument('--getdate')
    parser.add_argument('--truncate', action='store_true')
    parser.add_argument('--prepend')
    parser.add_argument('--append')
    args = parser.parse_args()
    if os.path.splitext(args.target)[1].lower() == '.pdf':
        target = args.target
    elif os.path.splitext(args.target)[1] == '':
        target = args.target + '.pdf'
    elif os.path.splitext(args.target)[1] == '.':
        target = args.target + 'pdf'
    else:
        print('You can only use pdfrename with PDFs.')
        sys.exit()
    try:
        with open(target, 'rb') as pdf:
            parser = PDFParser(pdf)
            doc = PDFDocument(parser)
    except FileNotFoundError:
        print('The file {} for could not be found.'.format(target))
        sys.exit()
    try:
        author = doc.info[0]['Author'].decode(chardet.detect(doc.info[0]['Author'])['encoding'])
    except TypeError:
        author = ''
    try:
        title = doc.info[0]['Title'].decode(chardet.detect(doc.info[0]['Title'])['encoding'])
    except TypeError:
        title = ''
    parts = []
    if args.prepend:
        parts.append(makesafe(args.prepend))
    if author:
        if args.surname:
            parts.append(makesafe(author.split()[-1]))
        else:
            parts.append(makesafe(author))
    if title:
        parts.append(makesafe(title))
    if args.date:
        try:
            date = doc.info[0]['CreationDate'].decode(chardet.detect(doc.info[0]['CreationDate'])['encoding'])[2:10]
        except TypeError:
            date = ''
        if date:
            parts.append(date)
    if args.getdate:
        with open(args.getdate) as f:
            for line in f.readlines():
                if line.startswith('date:'):
                    date = datetime.datetime.strptime(line.lstrip('date:').rstrip('\n').strip(), '%d %B %Y').strftime('%Y%m%d')
            parts.append(date)	
    if args.append:
        parts.append(makesafe(args.append))
    if parts:
        new_name = '_'.join(parts)
        os.rename(target, '{}.pdf'.format(new_name))
        if args.verbose:
            print(
                '{} has been renamed to {}.pdf'.format(
                    target,
                    new_name
                )
            )
