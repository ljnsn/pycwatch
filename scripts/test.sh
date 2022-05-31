#!/usr/bin/env bash

set -e
set -x

pytest tests --cov pycwatch --cov-report xml

