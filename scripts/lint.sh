#!/usr/bin/env bash

set -e
set -x

black pycwatch tests --check
ruff pycwatch tests
mypy pycwatch tests
