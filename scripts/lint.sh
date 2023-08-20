#!/usr/bin/env bash

set -e
set -x

black workspaces --check
ruff workspaces
mypy workspaces --explicit-package-bases
