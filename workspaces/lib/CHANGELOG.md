# Changelog

All notable changes to this project will be documented in this file.

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
