#!/usr/bin/env bash

set -e
set -x

coverage run
coverage combine
coverage report
coverage xml
