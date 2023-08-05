#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Santiago Dueñas <sduenas@bitergia.com>
#     Luis Cañas-Díaz <lcanas@bitergia.com>
#

import codecs
import os
import re

# Always prefer setuptools over distutils
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme_md = os.path.join(here, 'README.md')
version_py = os.path.join(here, 'indexwarrior', '_version.py')

# Pypi wants the description to be in reStrcuturedText, but
# we have it in Markdown. So, let's convert formats.
# Set up things so that if pypandoc is not installed, it
# just issues a warning.
try:
    import pypandoc
    long_description = pypandoc.convert(readme_md, 'rst')
except (IOError, ImportError):
    print("Warning: pypandoc module not found, or pandoc not installed. " \
            + "Using md instead of rst")
    with codecs.open(readme_md, encoding='utf-8') as f:
        long_description = f.read()

with codecs.open(version_py, 'r', encoding='utf-8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(name="indexwarrior",
      description="Tool to operate GrimoireLab ES indexes",
      long_description=long_description,
      url="https://gitlab.com/devops/indexwarrior",
      version=version,
      author="Bitergia",
      author_email="lcanas@bitergia.com",
      license="GPLv3",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.4'],
      keywords="development repositories analytics",
      packages=['indexwarrior'],
      scripts=[
        "bin/indexwarrior"
      ],
      install_requires=[
        'certifi==2018.04.16',
        'colorama==0.3.9',
        'elasticsearch==6.0.0',
        'elasticsearch-dsl==6.0.0',
        'prettytable==0.7.2',
        'httpretty==0.8.14'
      ],
      zip_safe=False
    )
