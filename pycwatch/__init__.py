import sys

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

from .client import CryptoWatchClient

__version__ = version("pycwatch")

__all__ = ("CryptoWatchClient",)
