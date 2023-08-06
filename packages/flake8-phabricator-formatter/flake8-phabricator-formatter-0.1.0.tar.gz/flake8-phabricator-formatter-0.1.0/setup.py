import setuptools

requires = [
    "flake8 > 3.0.0",
]

setuptools.setup(
    name="flake8-phabricator-formatter",
    license="MIT",
    version="0.1.0",
    description="flake8 formatter for Phabricator's Harbormaster",
    author='Software Heritage developers',
    author_email='swh-devel@inria.fr',
    url="https://forge.softwareheritage.org/source/flake8-phabricator-formatter/",
    packages=[
        "flake8_phabricator_formatter",
    ],
    install_requires=requires,
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
