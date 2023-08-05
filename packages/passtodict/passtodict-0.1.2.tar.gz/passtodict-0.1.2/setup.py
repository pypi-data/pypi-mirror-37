#!/usr/bin/python3

# Copyright (C) 2018  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

from setuptools import setup
import fastentrypoints      # noqa: F401


setup(
    name='passtodict',
    version='0.1.2',

    description="Password-Store client library",
    url='https://gitlab.com/pacholik1/Pass2Dict',
    license='LGPL-3.0',

    author="Vojtěch Pachol",
    author_email="pacholick@gmail.com",

    classifiers=[
        # 'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        'Programming Language :: Python :: 3',
    ],
    keywords='pass',

    packages=['passtodict'],
    setup_requies=['fastentrypoints'],
    install_requires=['python-gnupg'],

    entry_points={
        'console_scripts': [
            'passget=passtodict:main',
        ],
    },
)
