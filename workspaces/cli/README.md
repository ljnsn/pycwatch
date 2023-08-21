# pycwatch-cli

[![Coverage](https://img.shields.io/codecov/c/github/ljnsn/pycwatch?color=%2334D058)](https://codecov.io/gh/ljnsn/pycwatch)
[![Package version](https://img.shields.io/pypi/v/pycwatch?color=%2334D058&label=pypi%20package)](https://pypi.org/project/pycwatch)
[![Python versions](https://img.shields.io/pypi/pyversions/pycwatch.svg)](https://pypi.org/project/pycwatch)
[![Black style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
