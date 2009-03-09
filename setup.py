from setuptools import setup, find_packages
import os, os.path
import sys

DIRNAME = os.path.dirname(__file__)
#APPDIR = os.path.join(DIRNAME, 'satchmo')
APPDIR = os.path.join(DIRNAME, 'web/apps')
STATICDIR = os.path.join(DIRNAME, 'web/static')
if not APPDIR in sys.path:
    sys.path.append(APPDIR)

# Dynamically calculate the version based on django.VERSION.
#version = __import__('satchmo_store').__version__
version = '0.0.1'

packages = find_packages('web/apps')
packages.append('web/static')
data_files = []
for dirpath, dirnames, filenames in os.walk(STATICDIR):
    #Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup(name='fsadmin',
    version=version,
    description="Freeswitch Administrator",
    long_description="Web interface from FreeSWITCH"
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='freeswitch',
    author='Oleg Dolya',
    author_email='oleg.dolya@gmail.com',
    url='http://dev.uaseo.info/fsadmin/',
    license='GPL',
    include_package_data=True,
    package_dir = {
        '' : 'satchmo/apps',
        'static' : 'satchmo/static'
    },
    #packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    packages = packages,
    data_files = data_files,
    zip_safe = False,
    install_requires=[
        
        'Django>=1.1',
        'django-extensions',
        'BeautifulSoup',
        # TODO: add setuptools 
        'gdate',
        #'pycrypto',
        #'django-registration',
        #'django-threaded-multihost',
        #'PyYAML',
        #'Reportlab',
        #'trml2pdf',
        #'elementtree',
        #'docutils'
        #'jbo-lib-collection'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent', 
        'Topic :: Office/Business',
    ]
    zip_safe=False,
    #scripts=['scripts/server-admin','scripts/fapws2'],
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
        # -*- Entry points: -*-
        """,
        #test_suite="nose.collector",
)
