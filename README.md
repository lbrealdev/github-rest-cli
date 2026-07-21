# github-rest-cli

[![PyPI](https://img.shields.io/pypi/v/github-rest-cli.svg)](https://pypi.org/project/github-rest-cli/)
[![Python CI](https://github.com/lbrealdev/github-rest-cli/actions/workflows/python-ci.yml/badge.svg)](https://github.com/lbrealdev/github-rest-cli/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python CLI for common [GitHub REST API](https://docs.github.com/en/rest) operations—list and inspect repositories, create or delete them, manage Dependabot security settings, and create deployment environments.

## Installation

With `pip`:

```shell
pip install github-rest-cli
```

With `uv`:

```shell
uv pip install github-rest-cli
```

Requires Python 3.11.5 or newer.

## Authentication

Create a [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) and export it:

```shell
export GITHUB_AUTH_TOKEN="<github-auth-token>"
```

Suggested classic PAT scopes:

| Scope | Used for |
| --- | --- |
| `repo` | Private repos, create/delete, environments, Dependabot settings |
| `public_repo` | Public repositories only (subset of `repo`) |
| `delete_repo` | Deleting repositories (included in full `repo` on classic tokens) |

Fine-grained tokens need repository access with permissions for Contents, Administration (create/delete), Environments, and Dependabot/security alerts as needed.

For optional API URL overrides, settings files (including `settings.toml` / `.secrets.toml`), and environments, see [Configuration](docs/configuration.md).

## Quick start

```shell
github-rest-cli --version
github-rest-cli --help
```

```shell
github-rest-cli repo list
github-rest-cli repo get --name my-repo
github-rest-cli repo create --name my-new-repo --private
```

## Commands

Full command reference: [CLI guide](docs/cli.md).

```shell
github-rest-cli repo --help
github-rest-cli dependabot --help
github-rest-cli environment --help
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development, testing, linting, and Dynaconf tooling.

## Links

- [PyPI](https://pypi.org/project/github-rest-cli/)
- [Source](https://github.com/lbrealdev/github-rest-cli)
- [Issues](https://github.com/lbrealdev/github-rest-cli/issues)
- [License](LICENSE)
