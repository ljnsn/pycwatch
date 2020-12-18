# pycwatch

The `pycwatch` library provides access to the [Cryptowatch API](https://docs.cryptowat.ch/rest-api/) and implements all resources of the REST API.

## Installation

Install from pypi (soon):

`pip install pycwatch`

or clone this repository and install from there.

### Dependencies

-   `requests`

## Quick Start

```python
import pycwatch

# create api
api = pycwatch.rest

# get assets
assets = api.list_assets()
# get some price info
exchange, pair = 'binance', 'btceur'
price = api.get_market_price(exchange, pair)
```

If you have an account at [cryptowat.ch](https://cryptowat.ch), you can either set your key as an environment variable or in the code.

```shell
export CRYPTO_WATCH_KEY="my-awesome-key"
```

or

```python
import pycwatch

api = pycwatch.rest
api.api_key = 'my-awesome-key'
```
