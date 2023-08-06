# -*- coding: utf-8 -*-

import warnings

import pkg_resources
from ruamel import yaml

__author__ = "Uwe Schmitt"
__email__ = "uwe.schmitt@id.ethz.ch"
__version__ = pkg_resources.require("datapool")[0].version


warnings.simplefilter("ignore", yaml.error.UnsafeLoaderWarning)
