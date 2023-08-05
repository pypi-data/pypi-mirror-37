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

import os
import sys
import gnupg
import pathlib


PASS_PATH = pathlib.Path(os.path.expanduser('~/.password-store/'))
gpg = gnupg.GPG()


class DecryptError(Exception):
    pass


class Fields(dict):
    """Dict with password fields. Password itself is in `fields.PWD`"""
    def __init__(self, string: str):
        lines = string.splitlines()
        self.PWD = lines.pop(0)
        self.extra = []

        for line in lines:
            key, sep, value = line.partition(':')
            if sep:
                self[key] = value.lstrip()
            else:
                self.extra.append(line)

        for i in ['login', 'user', 'email']:
            login = self.get(i)
            if login:
                self.LOGIN = login
                break


class _Pass2Dict:
    exclude = ['.git']

    def __call__(self, passname):
        with open(PASS_PATH / (passname + '.gpg'), 'rb') as f:
            crypt = gpg.decrypt_file(f)

        if not crypt:
            raise DecryptError(crypt.status)

        info = str(crypt)
        return Fields(info)

    def get(self, passname, field):
        return self(passname)[field]

    def main(self):
        print(self.get(*sys.argv[1:]))

    def ls(self, subfolder='.'):
        if not os.path.isabs(subfolder):
            subfolder = PASS_PATH / subfolder

        for i in os.scandir(subfolder):
            i = i   # type: os.DirEntry
            if i.name in self.exclude:
                continue
            if i.is_dir():
                yield from self.ls(i)
            if i.is_file() and i.name.endswith('.gpg'):
                root, ext = os.path.splitext(
                    pathlib.Path(i).relative_to(PASS_PATH)
                )
                yield root


sys.modules[__name__] = _Pass2Dict()


if __name__ == '__main__':
    passtodict = _Pass2Dict()
    for i in sorted(passtodict.ls('test')):
        print(i)
