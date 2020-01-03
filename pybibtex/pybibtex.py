# pybibtext -- Utility functions for
# parsing BibTeX files and creating citation reference
# lists.
#
# Author: Sebastian Raschka <mail@sebastianraschka.com>
# License: MIT
# Code Repository: https://github.com/rasbt/pybibtex

from operator import itemgetter
from itertools import groupby


def parse_bibfile_to_cite_dict(bib_path):
    """Read a bibtex file into a dictionary.
    Returned dictionary has the form:

    {'\\cite{citekey-of-article}': {},
     '\\cite{citekey-of-article}': {},
     '\\cite{citekey-of-article}': {},
     ...
    }

    """
    dct = {}
    with open(bib_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                if line.startswith('@'):
                    entries = {}
                    start = line.find('{')
                    end = line.find(',')
                    citekey = '\cite{%s}' % line[start+1:end]
                    while not line.startswith('}'):
                        line = next(f)
                        if ' = ' not in line:
                            continue
                        key, value = line.split(' = ')
                        key = key.strip()
                        value = value.strip()[1:-1].strip('{}')
                        entries[key] = value
                    dct[citekey] = entries
    return dct


def parse_bibfile_to_dict(bib_path):
    """Read a bibtex file into a dictionary.
    Returned dictionary has the form:

    {'alberga2018prediction': ['title={Prediction of ... }'],
     'hawkins2007comparison': ['title={Comparison of ... }'],\
     ...

    }

    """
    dct = {}
    with open(bib_path, 'r') as f:
        txt = f.readlines()
        citekey = None
        entries = []
        for line in txt:
            line = line.strip()
            if line:
                if line.startswith('@'):
                    if citekey is not None:
                        dct[citekey] = entries
                    entries = []
                    start = line.find('{')
                    end = line.find(',')
                    citekey = '%s' % line[start+1:end].lower()
                entries.append(line)
    if citekey is not None:
        dct[citekey] = entries

    return dct


def split_multiciteky(citekey):
    """Splits a multi-citekey into individual citekeys"""
    splt = citekey.split('\cite{')[-1].rstrip('}')
    splt = [c.strip() for c in splt.split(',')]
    return ['\cite{%s}' % c for c in splt]


def ids_to_string(ids_list):
    """Converts lists of integer IDs to text"""
    sorted_ids = sorted(ids_list)
    ranges = []
    for key, group in groupby(enumerate(sorted_ids), lambda x: x[0] - x[1]):
        group = list(map(itemgetter(1), group))
        if len(group) > 1:
            ranges.append([group[0], group[-1]])
        else:
            ranges.append(group[0])

    parsed = []
    for r in ranges:
        if isinstance(r, list):
            parsed.append('%d-%d' % (r[0], r[1]))
        else:
            parsed.append(str(r))

    return '[%s]' % ','.join(parsed)


def bibentry_to_style(bibentry, style='default'):
    """Format a bibtext dictionary entry as a string."""
    s = ''
    if style == 'default':
        s += '%s ' % bibentry['author']
        s += '(%s). ' % bibentry['year']
        s += '*%s*' % bibentry['title']

        if 'journal' in bibentry:
            s += '. %s, ' % bibentry['journal']

        if 'volume' in bibentry:
            s += '%s' % bibentry['volume']

            if 'number' in bibentry:
                s += '(%s)' % bibentry['number']

                if 'pages' in bibentry:
                    s += ', %s' % bibentry['pages'].replace('--', '-')

        s += '.'
    return s


def get_cites(text_lines):
    """Yield citekeys from text lines."""
    cite_start = '\cite{'
    cite_end = '}'
    for idx, line in enumerate(text_lines):

        start = 0
        while True:
            start = line.find(cite_start, start)
            if start < 0:
                break

            orig_start = start
            start += len(cite_start) + 1
            end = line.find(cite_end, start)
            if end < 0:
                raise ValueError('No closing braces found in line %d: %s' %
                                 (idx+1, line))

            citekey = line[orig_start: end+1]
            yield citekey


def build_citekey_dict(text_lines):
    """Create a citekey dictionary from text lines"""
    dct = {}
    idx_cnt = 1
    for citekey in get_cites(text_lines):
        if ',' in citekey:
            citekeys = split_multiciteky(citekey)
        else:
            citekeys = [citekey]
        for key in citekeys:
            if key not in dct:
                dct[key] = '[%d]' % (idx_cnt)
                idx_cnt += 1
    return dct


def replace_citekeys(text_lines, citekey_dict):
    """Substitute citekeys by reference IDs"""
    for line in text_lines:
        citekeys = get_cites(text_lines=[line])
        for key in citekeys:
            if ',' in key:
                keys = split_multiciteky(key)
                id_key = ''.join(citekey_dict[k] for k in keys)
                id_key = id_key.replace('][', ',')
                ids_list = [int(i) for i in id_key[1:-1].split(',')]
                id_key = ids_to_string(ids_list)

            else:
                id_key = citekey_dict[key]

            line = line.replace(key, id_key)
        yield line
