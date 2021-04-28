# pycwatch

The `pycwatch` library provides access to the [Cryptowatch API](https://docs.cryptowat.ch/rest-api/) and implements all resources of the REST API.

## Installation

Either install from pypi or clone this repository and install locally.

```fish
pip install pycwatch
```

### Dependencies

- `requests`

## Quick Start

```python
import pycwatch

# create api client
api = pycwatch.rest

# get list of available assets
assets = api.list_assets()
# get some price info
exchange, pair = 'binance', 'btceur'
price = api.get_market_price(exchange, pair)
```

If you have an account at [cryptowat.ch](https://cryptowat.ch), you can either set your key as an environment variable or in the code.

```bash
export CRYPTO_WATCH_KEY="my-awesome-key"
```

or

```python
import pycwatch

api = pycwatch.rest
api.api_key = 'my-awesome-key'
```
