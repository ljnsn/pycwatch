#!/usr/bin/env bash

set -e
set -x

coverage run --source "workspaces/$1/src" --module pytest "workspaces/$1"
coverage report
coverage xml
