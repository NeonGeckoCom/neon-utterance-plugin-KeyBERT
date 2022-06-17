#!/usr/bin/env python3
import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


with open("README.md", "r") as f:
    long_description = f.read()


with open("./version.py", "r", encoding="utf-8") as v:
    for line in v.readlines():
        if line.startswith("__version__"):
            if '"' in line:
                version = line.split('"')[1]
            else:
                version = line.split("'")[1]


PLUGIN_ENTRY_POINT = 'neon-keyword-plugin-KeyBERT=neon_keyword_plugin_KeyBERT:KeyBERTExtractor'
setup(
    name='neon-keyword-plugin-KeyBERT',
    version=version,
    description='A keyword extractor for ovos/neon/mycroft',
    url='https://github.com/NeonGeckoCom/neon-keyword-plugin-KeyBERT',
    author='Neongecko',
    author_email='developers@neon.ai',
    license='BSD3',
    packages=['neon_keyword_plugin_KeyBERT'],
    zip_safe=True,
    keywords='mycroft plugin keyword extractor',
    entry_points={'intentbox.keywords': PLUGIN_ENTRY_POINT},
    install_requires=required("requirements.txt"),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
