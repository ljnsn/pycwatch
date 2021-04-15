
__version__ = '0.1.1'

import os
from pycwatch.rest import RestAPI


api_key = os.getenv('CRYPTO_WATCH_KEY') or None

rest = RestAPI(api_key)
