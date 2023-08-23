#!/usr/bin/env bash

error_exit() {
  msg=$1
  echo -e "$msg"
  exit 1
}

package=workspaces/$1

# get the current version of the main package
version=$(grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)

# replace version in pyproject.toml
sed -i "s/^version = \".*\"/version = \"$version\"/" "$package/pyproject.toml"

# replace all path dependencies
sed -i "s/^\(pycwatch-.*\) = { path = \".*\" }/\1 = \"$version\"/" "$package/pyproject.toml"

rootdir=$(pwd)

cd "$package" || error_exit "Could not find package $package"

poetry publish --build || error_exit "Failed to publish package $package"

cd "$rootdir" || error_exit "Failed to change back to directory $rootdir"
