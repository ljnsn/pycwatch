#!/usr/bin/env bash

package=workspaces/$1

# get the current version of the main package
version=$(grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

# replace version in pyproject.toml
sed -i "s/^version = \".*\"/version = \"$version\"/" "$package/pyproject.toml"

# replace all path dependencies
sed -i "s/^\(pycwatch-.*\) = { path = \".*\" }/\1 = \"$version\"/" "$package/pyproject.toml"

# poetry publish --build
cd "$package" && poetry build
