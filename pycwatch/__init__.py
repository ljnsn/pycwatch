__version__ = "0.2.1"

import os
from pycwatch.rest import RestAPI


api_key = os.getenv("CRYPTO_WATCH_KEY")

rest = RestAPI(api_key)
