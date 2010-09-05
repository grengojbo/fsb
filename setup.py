# -*- mode: python; coding: utf-8; -*-
from setuptools import setup, find_packages
import os, os.path
import sys

DIRNAME = os.path.dirname(__file__)

# Dynamically calculate the version based on django.VERSION.
version = __import__('fsb').__version__

setup(name='fsb',
    version=version,
    description="Freeswitch Billing",
    long_description="Billing System from FreeSWITCH",
    keywords='freeswitch',
    author='Oleg Dolya',
    author_email='oleg.dolya@gmail.com',
    url='http://bitbucket.org/jbo/fsa/',
    license='GPL',
    include_package_data=True,
    #package_dir = {
    #    '' : 'satchmo/apps',
    #    'static' : 'satchmo/static'
    #},
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    #packages = packages,
    #data_files = data_files,
    zip_safe = False,
    #install_requires=[
    #    'Django>=1.1',
    #    'django-extensions',
    #    #'django-batchadmin',
    #    'BeautifulSoup',
    #    'userprofile',
    #    #'pycrypto',
    #    #'django-registration',
    #    #'django-threaded-multihost',
    #    #'PyYAML',
    #    #'Reportlab',
    #    #'trml2pdf',
    #    'elementtree',
    #    'docutils',
    #    'fsadmin'
    #],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
    ],
    scripts=['scripts/fsb'],
)
