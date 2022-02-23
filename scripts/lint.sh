#!/usr/bin/env bash

set -e
set -x

mypy pycwatch
flake8 pycwatch tests
black pycwatch tests --check
isort pycwatch tests --check-only
