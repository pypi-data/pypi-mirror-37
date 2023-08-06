# Release procedure
#
# Prepare the release:
#
#  - run tests: tox
#  - fill the changelog in README.rst
#  - check that "python3 setup.py sdist" contains all files tracked by
#    the SCM (Mercurial): update MANIFEST.in if needed
#  - update version in setup.py
#  - set release date in the changelog in README.rst
#  - check README.rst: tox
#  - git commit -a
#  - git push
#
# Release the new version:
#
#  - git tag VERSION
#  - git push --tags
#  - python3 setup.py sdist bdist_wheel
#  - twine upload dist/*
#
# After the release:
#
#  - increment version in setup.py
#  - git commit && git push
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.rst") as fp:
    long_description = fp.read()

install_options = {
    "name": "sixer",
    "version": "1.6.1",
    "license": "Apache License 2.0",
    "author": 'Victor Stinner',
    "author_email": 'victor.stinner@gmail.com',

    "description": "Add Python 3 support to Python 2 applications using the six module.",
    "long_description": long_description,
    "url": "https://github.com/vstinner/sixer",

    "classifiers": [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    "py_modules": ["sixer"],
    "entry_points": {'console_scripts': ['sixer=sixer:main']},
}

setup(**install_options)
