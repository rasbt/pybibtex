# pybibtext -- Utility functions for
# parsing BibTeX files and creating citation reference
# lists.
#
# Author: Sebastian Raschka <mail@sebastianraschka.com>
# License: MIT
# Code Repository: https://github.com/rasbt/pybibtex

from setuptools import setup, find_packages


def calculate_version():
    initpy = open('pybibtex/__init__.py').read().split('\n')
    version = list(filter(lambda x:
                          '__version__' in x, initpy))[0].split('\'')[1]
    return version


package_version = calculate_version()

setup(name='pybibtex',
      version=package_version,
      description="Utility functions for creating citation references",
      author='Sebastian Raschka',
      author_email='mail@sebastianraschka.com',
      url='https://github.com/rasbt/pybibtex',
      license='MIT',
      zip_safe=True,
      packages=find_packages(),
      platforms='any',
      keywords=['bibtex'],
      classifiers=[
             'License :: OSI Approved :: MIT License',
             'Development Status :: 5 - Production/Stable',
             'Operating System :: Microsoft :: Windows',
             'Operating System :: POSIX',
             'Operating System :: Unix',
             'Operating System :: MacOS',
             'Programming Language :: Python :: 3.6',
      ],
      long_description="""
pybibtext is a package that provides utility functions for
parsing BibTeX files and creating citation reference lists

Contact
=============

If you have any questions or comments about mputil, please feel
free to contact me via
eMail: mail@sebastianraschka.com
or Twitter: https://twitter.com/rasbt

This project is hosted at https://github.com/rasbt/pybibtex

""")
