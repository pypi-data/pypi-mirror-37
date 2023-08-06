"""
Packaging metadata for the decode-acc library.
"""

# Copyright (c) 2018  Peter Pentchev
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import re
import setuptools


RE_VERSION = r'''^
    \s* VERSION \s* = \s* '
    (?P<version>
           (?: 0 | [1-9][0-9]* )    # major
        \. (?: 0 | [1-9][0-9]* )    # minor
        \. (?: 0 | [1-9][0-9]* )    # patchlevel
    (?: \. [a-zA-Z0-9]+ )?          # optional addendum (dev1, beta3, etc.)
    )
    ' \s*
    $'''


def get_version():
    """ Get the module version from its __init__.py file. """
    found = None
    re_semver = re.compile(RE_VERSION, re.X)
    with open('decode_acc/__init__.py') as verfile:
        for line in verfile.readlines():
            match = re_semver.match(line)
            if not match:
                continue
            assert found is None
            found = match.group('version')

    assert found is not None
    return found


def get_long_description():
    """ Read the long description from the README.md file. """
    with open('README.md') as descfile:
        return descfile.read()


setuptools.setup(
    name='decode-acc',
    version=get_version(),

    description='Incrementally decode bytes into strings and lines',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',

    author='Peter Pentchev',
    author_email='roam@ringlet.net',
    url='https://gitlab.com/ppentchev/decode-acc/',

    packages=('decode_acc',),
    package_data={
        'decode_acc': [
            # The PEP 484 typed Python module marker
            'py.typed',
        ],
    },

    license='BSD-2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: DFSG approved',
        'License :: Freely Distributable',
        'License :: OSI Approved :: BSD License',

        'Operating System :: OS Independent',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    zip_safe=True,
)
