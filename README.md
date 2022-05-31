# pycwatch

<p>
<a href="https://codecov.io/gh/ljnsn/pycwatch" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/ljnsn/pycwatch?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/pycwatch" target="_blank">
    <img src="https://img.shields.io/pypi/v/pycwatch?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black style">
</a>
</p>

</br>

The `pycwatch` library provides access to the [Cryptowatch API](https://docs.cryptowat.ch/rest-api/) and implements all resources of the REST API.

## Installation

Either install from pypi or clone this repository and install locally.

```fish
pip install pycwatch
```

## Quick Start

See the [cryptowat.ch docs](https://docs.cryptowat.ch/rest-api) for available endpoints.

```python
from pycwatch import CryptoWatchClient

# create api client
client = CryptoWatchClient()

# get list of available assets
assets = client.list_assets()
# get some price info
exchange, pair = "binance", "btceur"
price = client.get_market_price(exchange, pair)
```

If you have an account at [cryptowat.ch](https://cryptowat.ch), you can either set your key as an environment variable or in the code.

```bash
export CRYPTO_WATCH_KEY="my-awesome-key"
```

or

```python
from pycwatch import CryptoWatchClient

api_key = "my-awesome-key"
client = CryptoWatchClient(api_key)
```
