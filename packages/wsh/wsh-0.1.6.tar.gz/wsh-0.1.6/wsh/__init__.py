"""
:copyright: (c) 2018 Pinn Technologies, Inc.
:license: All rights reserved
"""
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .wsh import WSH  # NOQA
