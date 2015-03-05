#!/usr/bin/env python

from setuptools import setup, find_packages  
from codecs import open 
from os import path

# package meta info
NAME = "gblog"
VERSION = "0.1.0"
DESCRIPTION = "A simple blog system based on tornado and mysql"
AUTHOR = "GONG YU SONG"
AUTHOR_EMAIL = "yusong.gong@gmail.com"
LICENSE = "BSD"
URL = "https://github.com/waterdrinker/gblog"
KEYWORDS = "blog tornado mysql"
classifiers=[
    'Programming Language :: Python :: 3.4',
]

# package contents
PACKAGES = find_packages(exclude=['test', 'data'])
#['gblog']
#find_packages(exclude=['test'])

# If there are data files included in your packages that need to be
# installed, specify them here.  If using Python 2.6 or less, then these
# have to be included in MANIFEST.in as well.
package_data={
    '': ['*.html', '*.xml', '*.css', '*png'],
    #'sample': ['package_data.dat'],
}

# place data files outside of your packages.
# see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
# Each (directory, files) pair in the sequence specifies the installation directory and the files to install there.
data_files=[('share/gblog/gblog_sql', ['data/schema.sql']),
            ('share/gblog', ['data/gblog.conf'])]

ENTRY_POINTS = {
    'console_scripts': [
        'gblog=gblog.server:main',
    ],
}

# dependencies
INSTALL_REQUIRES = ["Markdown", "Pygments", "Unidecode", "tornado", "MySQL-python"]

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=classifiers,
    url=URL,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_data=package_data,
    data_files=data_files,
    install_package_data=True,
    #zip_safe=False,
    entry_points=ENTRY_POINTS,
    install_requires=INSTALL_REQUIRES,
)


