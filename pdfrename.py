#!/usr/bin/python
"""
Rename a PDF with information taken from its metadata.
"""

import argparse
import datetime
import os
import re
import time

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

sep = '_'


def truncate(s):
    """
    str -> str
    Take a string and return a string consisting of the initial capitals
    >>> truncate('Philosophy of Language and Mind')
    'PLM'
    >>> truncate('Semantics and Philosophy in Europe 8')
    'SPE8'
    """
    parts = s.split()
    initials = []
    for part in parts:
        if part[0].isupper() or part[0].isdigit():
            initials.append(part[0])
    return ''.join(initials)


def makesafe(s):
    """
    Make a safe filename by replacing spaces with a separator, and removing nin-word characters.
    >>> makesafe('Foo bar?')
    'Foo_bar'
    """
    no_spaces = re.sub('\s+', sep, s)
    safe = re.sub('\W', '', no_spaces)
    return safe

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
    target = args.target
    with open(target, 'rb') as pdf:
        parser = PDFParser(pdf)
        doc = PDFDocument(parser)
    try:
        author = doc.info[0]['Author']
    except KeyError:
        author = ''
    try:
        if '-' in doc.info[0]['Title']:
            title = doc.info[0]['Title'].split('-')[0].strip()
            subtitle = doc.info[0]['Title'].split('-')[1].strip()
        else:
            title = doc.info[0]['Title']
            subtitle = ''
    except KeyError:
        title = ''
        subtitle = ''
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
    if subtitle:
        if args.truncate:
            parts.append(truncate(makesafe(subtitle)))
        else:
            parts.append(makesafe(subtitle))
    if args.date:
        parts.append(time.strftime('%Y%m%d'))
    if args.getdate:
        with open(args.getdate) as f:
            for line in f.readlines():
                if line.startswith('date:'):
                    date = datetime.datetime.strptime(line.lstrip('date:').rstrip('\n').strip(), '%d %B %Y').strftime('%Y%m%d')
            parts.append(date)	
    if args.append:
        parts.append(makesafe(args.append))
    if parts:
        new_name = sep.join(parts)
        os.rename(target, '{}.pdf'.format(new_name))
        if args.verbose:
            print(
                '{} has been renamed to {}.pdf'.format(
                    target,
                    new_name
                )
            )
