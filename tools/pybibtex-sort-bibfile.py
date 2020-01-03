# pybibtext -- Utility functions for
# parsing BibTeX files and creating citation reference
# lists.
#
# Author: Sebastian Raschka <mail@sebastianraschka.com>
# License: MIT
# Code Repository: https://github.com/rasbt/pybibtex

# pybibtex-sort-bibfile.py is a script that
# sorts bib file entries alphabetically

import argparse
from pybibtex import parse_bibfile_to_dict
from pybibtex import __version__


def write_new_text(file_path, text):
    with open(file_path, 'w') as f:
        f.write(text)


def main(file_path, out_path):
    d = parse_bibfile_to_dict(file_path)
    items_sorted = [(k, v) for k, v in d.items()]
    items_sorted.sort()
    sorted_file_contents = [i[1] for i in items_sorted]
    sorted_file_contents = '\n\n'.join(['\n'.join(entry)
                                        for entry in sorted_file_contents])
    write_new_text(out_path, sorted_file_contents)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=('Script that sorts bib file entries alphabetically'),
            epilog=('Example:\npython pybibtex-sort-bibfile.py'
                    ' -i infile.bib -o oubfile.bib\n'),
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input bibfiles file with bibtex entries')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output path for the bibtex file '
                             'with sorted entries')

    parser.add_argument('--version', action='version',
                        version='pybibtex v. %s' % __version__)

    args = parser.parse_args()

    main(file_path=args.input,
         out_path=args.output)
