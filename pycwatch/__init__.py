
import os

from pycwatch.rest import RestAPI

__version__ = '0.0.1'


api_key = os.getenv('CRYPTO_WATCH_KEY') or None

rest = RestAPI(api_key)
