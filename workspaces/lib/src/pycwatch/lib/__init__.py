"""Main package."""
import sys

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

from pycwatch.lib.client import CryptoWatchClient

__version__ = version("pycwatch-lib")
__all__ = ("CryptoWatchClient",)
