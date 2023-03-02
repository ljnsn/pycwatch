#!/usr/bin/env bash

set -e
set -x

#mypy pycwatch
ruff src tests
black pycwatch tests --check
