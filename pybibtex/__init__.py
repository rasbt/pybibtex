# pybibtext -- Utility functions for
# parsing BibTex files and creating citation reference
# lists.
#
# Author: Sebastian Raschka <mail@sebastianraschka.com>
# License: MIT
# Code Repository: https://github.com/rasbt/pybibtex

from .pybibtex import parse_bibfile, bibentry_to_style
from .pybibtex import get_cites, build_citekey_dict, replace_citekeys

__all__ = [parse_bibfile, bibentry_to_style,
           get_cites, build_citekey_dict, replace_citekeys]

__version__ = '0.2.0'
__author__ = "Sebastian Raschka <mail@sebastianraschka.com>"
