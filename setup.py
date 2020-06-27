# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import sys
import re
from os import path
from setuptools import find_packages, setup

assert sys.version_info[0] == 3, "SpotDownloader requires Python 3."

VERSIONFILE = "spotdownloader/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError(
        "Unable to find version string in {}".format(VERSIONFILE))

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='SpotDownloader',
    version=version,
    description='This is a simple and easy to use app made in python that downloads all you music in .MP3 from a given spotify playlist, even your private ones!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    author='Bruno Moya',
    author_email='me@brunomoya.com',
    url='https://github.com/elblogbruno/SpotDownloader',
    download_url='https://github.com/elblogbruno/SpotDownloader/archive/1.0.1.tar.gz',
    keywords='songs lyrics spotify download youtube',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    data_files=[('./', ['requirements.txt'])],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'SpotDownloader = spotdownloader.__main__:main']
    },
    classifiers=[
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)