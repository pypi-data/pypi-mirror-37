#!/usr/bin/env python3

from setuptools import setup

setup(
    name="whtools",
    version="0.0.7",
    url="https://github.com/WHGhost/whtools",
    description='My python tools all in one package',
    long_description="""A random collection of python tools I make for various purpose packed together in a library""",
    author='WHGhost',
    author_email='wghosth@gmail.com',
    license='GPL-3.0',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
    ],
    keywords='library',
    packages=["whtools"],
    install_requires=[''],
    python_requires='>=3',
    package_data={},
    data_files=[],
)
