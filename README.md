# pycwatch

[![Coverage](https://img.shields.io/codecov/c/github/ljnsn/pycwatch?color=%2334D058)](https://codecov.io/gh/ljnsn/pycwatch)
![PyPI CLI - Version](https://img.shields.io/pypi/v/pycwatch-cli?logo=pypi&label=pycwatch-cli&color=limegreen)
![PyPI LIB - Version](https://img.shields.io/pypi/v/pycwatch-lib?logo=pypi&label=pycwatch-lib&color=limegreen)
[![Python versions](https://img.shields.io/pypi/pyversions/pycwatch.svg)](https://pypi.org/project/pycwatch)
[![Black style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Archived, because [Cryptowat.ch is dead](https://cryptowat.ch/products/cryptocurrency-market-data-api) 😞

This repository contains two packages, `pycwatch-lib` and `pycwatch-cli`.

## `pycwatch-lib`

The `pycwatch-lib` library provides access to the [Cryptowatch API](https://docs.cryptowat.ch/rest-api/) and implements all resources of the REST API. Use it in Python applications or scripts that you're writing to retrieve cryptocurrency market data.

### Library Installation

Either install from pypi or clone this repository and install locally.

```bash
pip install pycwatch-lib
```

### Library Quick Start

See the [cryptowat.ch docs](https://docs.cryptowat.ch/rest-api) for available endpoints.

```python
from pycwatch.lib import CryptoWatchClient

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
from pycwatch.lib import CryptoWatchClient

api_key = "my-awesome-key"
client = CryptoWatchClient(api_key)
```

Note that anonymous users are limited to 10 Cryptowatch Credits worth of API calls per 24-hour period.
See <https://docs.cryptowat.ch/rest-api/rate-limit#api-request-pricing-structure> for more information.

## `pycwatch-cli`

The `pycwatch-cli` is a command line application that makes the power of CryptoWatch
available to you on the command line.

### CLI Installation

The easiest way to install is with [`pipx`](https://pypa.github.io/pipx/).

```bash
pipx install pycwatch-cli
```

This will make the command `pycw` available.

### CLI Quick Start

Run `pycw --help` to get usage info.

```
❯ pycw --help
                                                                                                            
 Usage: pycw [OPTIONS] COMMAND [ARGS]...                                                                    
                                                                                                            
 PyCwatch CLI.                                                                                              
                                                                                                           
╭─ Commands ───────────────────────────────────────────────────────────────╮
│ assets                           Get or list assets.                     │
│ exchanges                        Get or list exchanges.                  │
│ info                             Get API info.                           │
│ markets                          Get or list markets.                    │
│ pairs                            Get or list pairs.                      │
╰──────────────────────────────────────────────────────────────────────────╯
```

All the endpoints implemented by `pycwatch-lib` are available via the `pycw` command.
For example:

```bash
# list available assets
pycw assets list
# get some price info
pycw markets price binance btceur
```
