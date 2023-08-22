# Changelog

All notable changes to this project will be documented in this file.

## v2.1.0 (2023-08-22)

### ✨ Features

- **cli**: add different output format options

### 🐛🚑️ Fixes

- **cli**: fix adding key with multiple top level keys
- **lib**: use ujson converter

### ✅🤡🧪 Tests

- **cli**: test some more commands with different formats
- **cli**: add some tests for formatting

### 💚👷 CI & Build

- **main**: update lock file
- **dependabot**: monitor root folder too
- **publish**: use package specific tokens

### 📝💡 Documentation

- **readme**: update pypi badges

### 🔧🔨📦️ Configuration, Scripts, Packages

- **publish**: add set -e

### 🚨 Linting

- **cli**: remove noqas

### 🧑‍💻 Developer Experience

- **cli**: ignore FBT002 globally
- **cli**: ignore UP007 globally
- **cli**: ignore B008 globally

## v2.0.0 (2023-08-21)

### 💥 Boom

- move to monorepo setup

### ✨ Features

- **cli**: add exchanges commands
- **lib**: add markets cli
- **cli**: add pairs command
- **cli**: add info and assets commands and tests
- add cli

### 🐛🚑️ Fixes

- **cli**: return only result everywhere
- **lib**: pin cfgv
- **lib**: add identify for compat
- pin pre-commit below 2.20
- **lib**: key by is optional
- **lib**: pin black to below 23.7
- **lib**: coverage 7 dropped support for 3.7
- **cli**: typer doesn't support pipe union
- **cli**: always return result
- **lib**: pin mypy for 3.7
- **lib**: add unstructuring for decimals
- **lib**: add converter for MarketSummaryKey
- **main**: only install cli if python >= 3.10
- **cli**: require python >= 3.10
- **cli**: remove module running
- **cli**: fix entrypoint
- **main**: add cli dependencies
- **cli**: add script entrypoint
- **lib**: ignore correct file
- **lib**: add namespace level
- **lib**: fix version
- ignore reports and ruff cache
- move scripts back to top level
- **pyproject**: include namespace package

### ✅🤡🧪 Tests

- **cli**: add tests for market commands

### 🏷️ Types

- add py.typed to lib and cli

### 💚👷 CI & Build

- **dependabot**: monitor workspace dirs
- **publish**: publish both packages
- **package**: remove unnecessary quotes
- update lock file
- **package**: only lint on 310 and 311
- **pre-commit**: pass packages to mypy
- **package**: list excludes line by line
- **package**: only run cli tests for python >= 3.10
- **coverage**: enable parallel again and add combine
- **package**: upload all test run reports
- **package**: upload correct file
- **package**: don't poetry run
- **package**: fix upload file
- **package**: fix installs
- **package**: checkout repo
- **package**: checkout repo
- **package**: remove report step
- **package**: properly combine reports
- **package**: install coverage
- **package**: download all reports
- **package**: upload coverage only once
- **package**: remove mac from lint job too
- **package**: remove macos due to weird make behaviour
- **package**: run tests for both packages
- **package**: fix job name
- **package**: update pipeline
- change coverate report location

### 📌➕⬇️ ➖⬆️  Dependencies

- **lib**: remove requests-mock and pytest-mock
- bump mypy

### 📝💡 Documentation

- **cli**: update readme
- **readme**: better formatting
- **readme**: add usage info
- update readme

### 🔐🚧📈✏️ 💩👽️🍻💬🥚🌱🚩🥅🩺 Others

- cfgv

### 🔥⚰️  Clean up

- remove changelog from lib

### 🔧🔨📦️ Configuration, Scripts, Packages

- **publish**: fix publishing
- **cli**: set proper target versions
- **lint**: check packages with mypy instead of paths
- **mypy**: ignore missing imports for apiclient
- **main**: no need to combine without parallel
- **coverage**: reduce threshold
- **main**: include only src in coverage run
- **main**: replace version and path dependencies in publishs script
- **cli**: lower coverage fail threshold
- **main**: use test script in makefile
- **main**: update lint and test scripts
- **main**: exclude correct file
- **main**: add makefile
- **main**: use lib test extras
- **lib**: rename extras to test and remove commitizen
- **coverage**: add some config for coverage

### 🚨 Linting

- **lib**: add and remove ignores

## v1.1.4 (2023-08-20)

### 🐛🚑️ Fixes

- **conversion**: add and use new (un)structuring method
- use cattrs latest instead of master
- **config**: make settings attrs class

### ♻️  Refactorings

- **conversion**: move converter to separate module

### ✅🤡🧪 Tests

- **conversion**: add tests for (un)structuring
- **config**: add test for settings

### 💚👷 CI & Build

- **pre-commit**: add local hooks

### 📌➕⬇️ ➖⬆️  Dependencies

- pydantic
- api-client-pydantic

### 📝💡 Documentation

- **readme**: add note about anonymous usage
- fix links in changelog

### 🔥⚰️  Clean up

- **client**: remove no key message
- remove flake8 config

### 🔧🔨📦️ Configuration, Scripts, Packages

- **ruff**: remove ignore for EM101

## [v1.1.3][1.1.3] (2023-08-20)

### ♻️  Refactorings

- switch to attrs and add typing

### 💚👷 CI & Build

- remove run on separate pull request
- add python 3.11 to matrix
- add bump commit message
- **pre-commit**: add more hooks
- rename job deploy -> publish

## [v1.1.2][1.1.2] (2022-12-27)

### 🐛🚑️ Fixes

- use importlib.metadata to get version

### 💚👷 CI & Build

- **publish**: add publish workflow
- **package**: add bump-version job
- **package**: fix python package workflow
- add commitizen and cz-conventional-gitmoji, remove bumpversion

### 📌➕⬇️ ➖⬆️  Dependencies

- add importlib-metadata for python<3.8

### 📝💡 Documentation

- **changelog**: fix date in changelog
- **changelog**: fix changelog format so that commitizen recognizes tags

### 🔥⚰️  Clean up

- remove bumpversion config

### 🔧🔨📦️ Configuration, Scripts, Packages

- add publish script and make all scripts executable
- remove python restriction from black dependency
- **commitizen**: add bump message template
- **commitizen**: add tag format
- **coverage**: fix source to not include tests

## [v1.1.1][1.1.1] (2022-06-22)

### Fixed

- Remove poetry-version-plugin until supported again.
- New property on pairs -> add AssetMember.sid

## [v1.1.0][1.1.0] (2022-06-16)

### Fixed

- Fixed an issue with the allowance when an API key was provided.

### Added

- Add `get_info` method that queries the root endpoint to get status information.
- Add back ability to pass periods as mixed list of `int` and `str` that was removed in 1.0.0.

## [v1.0.1][1.0.1] (2022-06-16)

### Changed

- Minor update mostly to improve coverage and bump dependencies.

## [v1.0.0][1.0.0] (2022-03-04)

### Changed

- All API calls now return data as `pydantic` models.

### Added

- Live tests.

## [v0.2.1][0.2.1] (2021-04-29)

### Added

- First version published to pypi. Mostly done some polishing. It is now possible to specify you periods as a mixed list of `str` and `int` in the `get_market_ohlc` method, if you so wish.

## [v0.2.0][0.2.0] (2021-04-16)

### Added

- Typing information on both resources and REST client.

### Changed

- Made `pycwatch.rest.RestAPI.update_allowance` and `pycwatch.rest.RestAPI.perform_request` private methods.

## [v0.1.1][0.1.1] (2020-12-19)

### Added

- Remaining tests for the main API client.
- Better README with quick start instructions.
- This changelog.

### Changed

- `rest.perform_request` does not raise an `APIError` anymore when no key is set, but puts a debug message into log.

## [v0.1.0][0.1.0] (2020-09-24)

### Added

- Tests for the HTTP client, resources, and basic ones for API client.

## [v0.0.1][0.0.1] (2020-09-15)

### Added

- Initial version with support for all resources defined by the Cryptowat.ch REST API.

The format of this file is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[unreleased]: https://github.com/iuvbio/pycwatch/compare/v1.1.3...HEAD
[1.1.3]: https://github.com/iuvbio/pycwatch/compare/v1.1.2...1.1.3
[1.1.2]: https://github.com/iuvbio/pycwatch/compare/v1.1.1...1.1.2
[1.1.1]: https://github.com/iuvbio/pycwatch/compare/v1.1.0...1.1.1
[1.1.0]: https://github.com/iuvbio/pycwatch/compare/v1.0.1...1.1.0
[1.0.1]: https://github.com/iuvbio/pycwatch/compare/v0.2.1...1.0.1
[1.0.0]: https://github.com/iuvbio/pycwatch/compare/v0.2.1...1.0.0
[0.2.1]: https://github.com/iuvbio/pycwatch/compare/v0.2.0...0.2.1
[0.2.0]: https://github.com/iuvbio/pycwatch/compare/v0.1.1...0.2.0
[0.1.1]: https://github.com/iuvbio/pycwatch/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/iuvbio/pycwatch/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/iuvbio/pycwatch/releases/tag/v0.0.1
