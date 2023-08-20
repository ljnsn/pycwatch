#!/usr/bin/env bash

set -e

mypy_params=()
for directory in workspaces/*; do
  # Check if the current item is a directory
  if [[ -d "$directory" ]]; then
    dir_name=$(basename "$directory")
    mypy_params+=("-p" "pycwatch.$dir_name")
  fi
done

set -x

black workspaces --check
ruff workspaces
mypy "${mypy_params[@]}"
