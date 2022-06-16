#!/usr/bin/env bash

set -e
set -x

pytest --doctest-modules --cov pycwatch --cov-report xml tests
