#!/usr/bin/env bash

set -e
set -x

coverage run --source "workspaces/$1" --module pytest "workspaces/$1"
coverage combine -a
coverage report
coverage xml
