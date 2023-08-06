#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coldfront',
    version='0.0.2',
    description='HPC Resource Allocation System ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='high-performance-computing resource-allocation',
    url='http://coldfront.io',
    project_urls={
        'Bug Tracker': 'https://github.com/ubccr/coldfront/issues',
        'Documentation': 'https://ubccr.github.io/coldfront-docs/',
        'Source Code': 'https://github.com/ubccr/coldfront',
    },
    author='Andrew E. Bruno, Dori Sajdak, Mohammad Zia',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(),
    install_requires=[
        'arrow==0.12.1',
        'bibtexparser==1.0.1',
        'blessed==1.15.0',
        'certifi==2018.10.15',
        'chardet==3.0.4',
        'Django==2.1.2',
        'django-crispy-forms==1.7.2',
        'django-model-utils==3.1.2',
        'django-picklefield==1.1.0',
        'django-q==1.0.1',
        'django-simple-history==2.5.1',
        'django-sslserver==0.20',
        'django-su==0.8.0',
        'doi2bib==0.3.0',
        'future==0.16.0',
        'humanize==0.5.1',
        'idna==2.7',
        'pyparsing==2.2.2',
        'python-dateutil==2.7.3',
        'python-memcached==1.59',
        'pytz==2018.5',
        'redis==2.10.6',
        'requests==2.20.0',
        'six==1.11.0',
        'urllib3==1.24',
        'wcwidth==0.1.7',
    ],
    entry_points={
        'console_scripts': [
            'coldfront = coldfront:manage',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 2.1',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Systems Administration',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ]
)
