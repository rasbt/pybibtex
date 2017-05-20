# pybibtext -- Utility functions for
# parsing BibTex files and creating citation reference
# lists.
#
# Author: Sebastian Raschka <mail@sebastianraschka.com>
# License: MIT
# Code Repository: https://github.com/rasbt/pybibtex


def parse_bibfile(bib_path):
    """Read a bibtex file into a dictionary."""
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

            yield line[orig_start: end+1]


def build_citekey_dict(text_lines):
    """Create a citekey dictionary from text lines"""
    dct = {}
    idx_cnt = 1
    for cite in get_cites(text_lines):
        if cite not in dct:
            dct[cite] = '[%d]' % (idx_cnt)
            idx_cnt += 1
    return dct


def replace_citekeys(text_lines, citekey_dict):
    """Substitute citekeys by reference IDs"""
    for line in text_lines:
        for k in citekey_dict:
            line = line.replace(k, citekey_dict[k])
        yield line
