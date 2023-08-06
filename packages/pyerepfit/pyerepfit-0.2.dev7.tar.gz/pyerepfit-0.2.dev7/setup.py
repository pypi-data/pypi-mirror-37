#!/usr/bin/env python3

from setuptools import setup, find_packages
import pyerepfit

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(name='pyerepfit',
    version=pyerepfit.__version__,
    description='The python verion of the DFTB repulsive potential fitting tool, erepfit.',
    url='https://bitbucket.org/solccp/pyerepfit.git',
    author='Chien-Pin Chou',
    author_email='sol.chou@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Chemistry",

    ],
    scripts=['bin/erepfit'],
    package_data={'pyerepfit': '*.json'},
    install_requires=install_requires,
    zip_safe=False)
