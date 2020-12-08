# pycwatch

The `pycwatch` library provides access to the [Cryptowatch API](https://docs.cryptowat.ch/rest-api/) and implements all resources of the REST API.

## Installation

Install from pypi:

`pip install pycwatch`

or clone this repository and install from there.

### Dependencies

-   `requests`

## Quick Start

You can set your API key as an environment variable before you use `pycwatch` like so:

```shell
export CRYPTO_WATCH_KEY="my-awesome-key"
```

If you do that, you can skip setting you key in the instructions below.

```python
import pycwatch

# create api
api = pycwatch.rest
# assign api key
api.api_key = 'my-awesome-key'

# get assets
assets = api.list_assets()
# get some price info
exchange, pair = 'binance', 'btceur'
price = api.get_market_price(exchange, pair)
```
