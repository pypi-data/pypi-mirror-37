#!/usr/bin/env python
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


setup(
    name="alhambra",
    version="1.0.0",
    packages=['alhambra'],
    install_requires=[
        'numpy', 'stickydesign >= 0.8.1', 'svgwrite', 'lxml', 'shutilwhich',
        'peppercompiler >= 0.1.2', 'ruamel.yaml', 'cssutils'
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['alhambra = alhambra.scripts:alhambra']},
    author="Constantine Evans",
    author_email="cevans@dna.caltech.edu",
    description="DX Tile Set Designer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://dna.caltech.edu/alhambra')
