#!/usr/bin/env bash

set -e
set -x

pytest tests --cov --cov-report xml pycwatch

