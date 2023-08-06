
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# import * : only appropriate because ponder is our only module
# This namespace contains everything (for those who want it)
# but public API is defined by __all__
from .ponder import *
__all__ = ['use_dataframes','encode','one_hot']
