# -*- coding: utf-8 -*-
from collections import namedtuple

version_info = namedtuple("version_info", ["major", "minor", "patch"])
version = version_info(1, 2, 0)
__version__ = "{0.major}.{0.minor}.{0.patch}".format(version)
