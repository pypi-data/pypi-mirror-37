#!/usr/bin/python
#  -*- coding=utf-8 -*-
from setuptools import setup, find_packages


with open("README", "r") as fh:
    long_description = fh.read()

with open("ChangeLog", "r") as fh:
    long_description += fh.read()

setup(
        name = "pynav",
        version = "1.0",
        packages=find_packages(),
        # metadata for upload to PyPI
        author = "sloft",
        author_email = "nomail@example.com",
        description = "Python programmatic web browser to fetch data and test web sites",
        license = "GNU Lesser General Public License (LGPL)",
        keywords = ["programmatic", "web", "browser"],
        url = "http://bitbucket.org/sloft/pynav/",
        download_url = "http://bitbucket.org/sloft/pynav/downloads/",
        python_requires='>=3.5',
        classifiers = [
	"Programming Language :: Python",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
	"Operating System :: OS Independent",
	"License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
	"Development Status :: 4 - Beta",
	"Environment :: Console",
	"Topic :: Internet",
	"Intended Audience :: Developers",
	"Topic :: Internet :: WWW/HTTP",
	"Topic :: Internet :: WWW/HTTP :: Browsers",
	"Topic :: Internet :: WWW/HTTP :: Indexing/Search",
	"Topic :: Internet :: WWW/HTTP :: Site Management",
	"Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
	"Topic :: Software Development :: Libraries",
	"Topic :: Software Development :: Libraries :: Python Modules",
	],
        long_description = long_description
)
