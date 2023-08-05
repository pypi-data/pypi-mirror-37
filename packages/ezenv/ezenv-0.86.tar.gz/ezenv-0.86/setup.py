#!/usr/bin/env python
import setuptools
from distutils.core import setup

# grab metadata
version = '1.00'
with open('env.py') as f:
    for line in f:
        if line.startswith('__version__'):
            try:
                version = line.split("'")[1]
            except IndexError:
                pass
            break

# readme is needed at register time, not install time
try:
    with open('readme.rst') as f:
        long_description = f.read()
except IOError:
    long_description = ''


setup(
    name          = 'ezenv',
    version       = version,
    description   = 'A more convenient interface to environment variables.',
    author        = 'Mike Miller',
    author_email  = 'mixmastamyk@bitbucket.org',
    url           = 'https://github.com/mixmastamyk/env',
    license       = 'LGPL',
    py_modules    = ['env'],

    long_description = long_description,
    classifiers     = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
