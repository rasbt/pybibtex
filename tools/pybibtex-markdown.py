# pybibtext -- Utility functions for
# parsing BibTeX files and creating citation reference
# lists.
#
# Author: Sebastian Raschka <mail@sebastianraschka.com>
# License: MIT
# Code Repository: https://github.com/rasbt/pybibtex

# pybibtex-mardkown.py is a script that
# formats a markdown document by inserting
# citekeys and appending a reference list.

import argparse
from pybibtex import build_citekey_dict
from pybibtex import replace_citekeys
from pybibtex import parse_bibfile_to_citedict
from pybibtex import bibentry_to_style
from pybibtex import __version__


def read_text_from_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text.split('\n')


def write_new_text(file_path, text):
    with open(file_path, 'w') as f:
        f.write(text)


def replace_citekeys_in_text(textlines, citekey_dict):
    new_text = '\n'.join(line for line in
                         replace_citekeys(textlines, citekey_dict))
    return new_text


def create_reference_section(citekey_dict, bib_dict):
    s = '\n\n# References\n\n'
    for idx, citekey in enumerate(citekey_dict):
        styled = bibentry_to_style(bib_dict[citekey], style='default')
        s += '%d. %s\n' % (idx+1, styled)
    return s


def main(file_path, out_path, bib_path):
    text_lines = read_text_from_file(file_path)
    citekey_dict = build_citekey_dict(text_lines)
    new_text = replace_citekeys_in_text(text_lines, citekey_dict)
    bib_dict = parse_bibfile_to_citedict(bib_path=bib_path)
    reference_section = create_reference_section(citekey_dict, bib_dict)
    write_new_text(out_path, text=new_text + reference_section)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=('Inserts citations into a markdown file'
                         ' and appends a reference list.'),
            epilog=('Example:\npython pybibtex-markown.py -i infile.md -o'
                    ' oubfile.md -b bibfile.bib\n'),
            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        help='Input markdown file with citekeys')
    parser.add_argument('-o', '--output',
                        type=str,
                        required=True,
                        help='Output path for the processed markdown file')
    parser.add_argument('-b', '--bibtex',
                        type=str,
                        required=True,
                        help='BibTeX file path (.bib file)')

    parser.add_argument('--version', action='version',
                        version='pybibtex v. %s' % __version__)

    args = parser.parse_args()

    main(file_path=args.input,
         out_path=args.output,
         bib_path=args.bibtex)
