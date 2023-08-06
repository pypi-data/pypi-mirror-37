from setuptools import setup, find_packages

from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="flake8-phabricator-formatter",
    license="MIT",
    version="0.1.1",
    description="flake8 formatter for Phabricator's Harbormaster",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Software Heritage developers',
    author_email='swh-devel@inria.fr',
    url="https://forge.softwareheritage.org/source/flake8-phabricator-formatter/",  # noqa
    packages=find_packages(),
    install_requires=[
        "flake8 > 3.0.0",
    ],
    entry_points={
        'flake8.report': [
            'phabricator = '
            'flake8_phabricator_formatter:PhabricatorFormatter',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
