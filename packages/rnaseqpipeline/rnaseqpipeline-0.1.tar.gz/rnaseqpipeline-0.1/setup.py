from setuptools import setup, find_packages
from os import path

setup(
        name = "rnaseqpipeline",
        version = "0.1",
        author = "Joris van Steenbrugge",
        author_email = "joris.vansteenbrugge@wur.nl",
        packages = find_packages(),
        description = 'WUR nematology rnaseq pipeline',
#        packages = ['rnaseqpipeline'],
        scripts = ['scripts/rnaseqpipeline', 'scripts/fastaSplitter']
        )
