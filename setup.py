# -*- mode: python; coding: utf-8; -*-
from setuptools import setup, find_packages
import os, os.path
import sys

DIRNAME = os.path.dirname(__file__)
##APPDIR = os.path.join(DIRNAME, 'satchmo')
#APPDIR = os.path.join(DIRNAME, 'web/apps')
#STATICDIR = os.path.join(DIRNAME, 'web/static')
#if not APPDIR in sys.path:
#    sys.path.append(APPDIR)

# Dynamically calculate the version based on django.VERSION.
##version = __import__('satchmo_store').__version__
version = '0.0.2'

#packages = find_packages('web/apps')
#packages.append('web/static')
#data_files = []
#for dirpath, dirnames, filenames in os.walk(STATICDIR):
#    #Ignore dirnames that start with '.'
#    for i, dirname in enumerate(dirnames):
#        if dirname.startswith('.'): del dirnames[i]
#    if filenames:
#        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup(name='fsbilling',
    version=version,
    description="Freeswitch Billing",
    long_description="Billing System from FreeSWITCH",
    keywords='freeswitch',
    author='Oleg Dolya',
    author_email='oleg.dolya@gmail.com',
    url='http://linktel.com.ua/project/fsbilling/',
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
    install_requires=[
        'Django>=1.1',
        'django-extensions',
        'django-batchadmin',
        'BeautifulSoup',
        'userprofile',
        #'pycrypto',
        #'django-registration',
        #'django-threaded-multihost',
        #'PyYAML',
        #'Reportlab',
        #'trml2pdf',
        'elementtree',
        'docutils',
        'fsadmin'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent', 
        'Topic :: Office/Business',
    ],
    #scripts=['scripts/server-admin','scripts/fapws2'],
)