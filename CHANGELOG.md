# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `repo list --all` fetches every page by following GitHub `Link` headers.
- `repo list --page` selects the page number (default `1`).

### Changed

- `repo list --page` no longer means page size. Use `--per-page` (default `20`) instead.
- `repo get` table output is a curated key/value detail view instead of the list summary columns.
- Split output formatting into projection helpers and generic renderers (`format_repo_get` / `format_repo_list`).

### Documentation

- Clarified `repo get` vs `repo list` table/JSON field behavior in the CLI guide.
- Documented `repo list` pagination flags (`--per-page`, `--page`, `--all`).

## [2.0.0] - 2026-07-21

### Changed

- Nested CLI groups: `repo`, `dependabot`, and `environment` with subcommands.
- `repo create` visibility via `--public` / `--private` / `--internal` (default public).
- Moved argparse construction and command handlers into `parser.py`; `main.py` is a thin entrypoint.
- Migrated uv development dependencies to PEP 735 `[dependency-groups]`.

### Documentation

- Added [CLI guide](docs/cli.md).
- Added [Authentication](docs/authentication.md) guide (PAT scopes and token setup).
- Expanded [configuration](docs/configuration.md) with `settings.toml` / `.secrets.toml` credential examples.
- Documented the release process in [CONTRIBUTING.md](CONTRIBUTING.md).

## [1.0.3] - 2025-08-22

Previous release on PyPI. See Git history and GitHub Releases for earlier notes.
