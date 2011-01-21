# -*- mode: python; coding: utf-8; -*- 
VERSION = (0, 3, 0)

# Dynamically calculate the version based on VERSION tuple
if len(VERSION)>2 and VERSION[2] is not None:
    str_version = "%d.%d.%d" % VERSION[:3]
else:
    str_version = "%d.%d" % VERSION[:2]

__author__ = '$Author:$'
__revision__ = '$Revision:$'
__version__ = str_version