# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Breaking

- Replaced flat commands with nested groups:
  - `get-repo` → `repo get`
  - `list-repo` → `repo list`
  - `create-repo` → `repo create`
  - `delete-repo` → `repo delete`
  - `dependabot --enable` / `--disable` → `dependabot enable` / `dependabot disable`
  - `environment` → `environment create`
- Replaced `repo create --visibility` with mutually exclusive `--public` / `--private` / `--internal` (default public).

### Changed

- Moved argparse construction and command handlers into `parser.py`; `main.py` is a thin entrypoint.
- Migrated uv development dependencies to PEP 735 `[dependency-groups]`.

### Documentation

- Added [CLI guide](docs/cli.md).
- Added [Authentication](docs/authentication.md) guide (PAT scopes and token setup).
- Expanded [configuration](docs/configuration.md) with `settings.toml` / `.secrets.toml` credential examples.
- Documented the release process in [CONTRIBUTING.md](CONTRIBUTING.md).

## [1.0.3] - 2025-08-22

Previous release on PyPI. See Git history and GitHub Releases for earlier notes.
