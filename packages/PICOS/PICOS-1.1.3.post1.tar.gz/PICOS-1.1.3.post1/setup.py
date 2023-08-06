#!/usr/bin/python

#-------------------------------------------------------------------------------
# Copyright (C) 2012-2017 Guillaume Sagnol
# Copyright (C)      2018 Maximilian Stahlberg

#
# This file is part of PICOS Release Scripts.
#
# PICOS Release Scripts are free software: you can redistribute it and/or modify
# them under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PICOS Release Scripts are distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from version import get_version, get_base_version
except ModuleNotFoundError:
    # PyPI strips version.py from the source package as it's not part of the installation.
    import os

    LOCATION = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    VERSION_FILE = os.path.join(LOCATION, "picos", ".version")

    def get_base_version():
        with open(VERSION_FILE, "r") as versionFile:
            return versionFile.read().strip()

    get_version = get_base_version

setup(
    name = 'PICOS',
    version = get_version(),
    author = 'Guillaume Sagnol',
    author_email = 'sagnol@math.tu-berlin.de',
    packages = ['picos'],
    package_data = {'picos': ['.version']},
    license = 'LICENSE.txt',
    description = 'A Python interface to conic optimization solvers.',
    long_description = open('README.md', 'rb').read().decode('utf8'),
    long_description_content_type = 'text/markdown',
    install_requires = [
        "CVXOPT >=  1.1.4",
        "numpy  >=  1.6.2",
        "six >=  1.8.0"
    ],
    keywords = [
        'conic optimization',
        'convex optimization'
        'linear programming',
        'quadratic programming',
        'semidefinite programming',
        'exponential cone programming',
        'lp',
        'socp',
        'sdp'
    ],
    classifiers = [
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python'
    ],
    url = 'https://gitlab.com/picos-api/picos',
    download_url = 'https://gitlab.com/picos-api/picos/tags/v{}'.format(get_base_version())
)
