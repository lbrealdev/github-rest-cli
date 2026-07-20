# github-rest-cli

[![PyPI](https://img.shields.io/pypi/v/github-rest-cli.svg)](https://pypi.org/project/github-rest-cli/)
[![Python CI](https://github.com/lbrealdev/github-rest-cli/actions/workflows/python-ci.yml/badge.svg)](https://github.com/lbrealdev/github-rest-cli/actions/workflows/python-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Python CLI for common [GitHub REST API](https://docs.github.com/en/rest) operations—list and inspect repositories, create or delete them, manage Dependabot security settings, and create deployment environments.

## Features

- Get repository details (`repo get`)
- List repositories for the authenticated user (`repo list`)
- Create and delete repositories (`repo create`, `repo delete`)
- Enable or disable Dependabot security updates (`dependabot enable|disable`)
- Create deployment environments (`environment create`)
- Table or JSON output for repository listings (`--format`)

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

For optional API URL overrides, settings files, and environments, see [Configuration](docs/configuration.md).

## Quick start

```shell
github-rest-cli --version
github-rest-cli --help
```

## Commands

Top-level groups:

```shell
github-rest-cli repo --help
github-rest-cli dependabot --help
github-rest-cli environment --help
```

### Get a repository

```shell
github-rest-cli repo get --name my-repo
github-rest-cli repo get --name my-repo --org my-org
github-rest-cli repo get --name my-repo --format json
```

### List repositories

```shell
github-rest-cli repo list
github-rest-cli repo list --page 50 --sort pushed
github-rest-cli repo list --role owner --format json
```

| Flag | Description | Default |
| --- | --- | --- |
| `-p` / `--page` | Number of results (`per_page`) | `20` |
| `-s` / `--sort` | Sort field (e.g. `pushed`, `updated`, `created`) | `pushed` |
| `-r` / `--role` | Filter by affiliation/role | unset |
| `-f` / `--format` | Output format: `table` or `json` | `table` |

### Create a repository

```shell
github-rest-cli repo create --name my-new-repo
github-rest-cli repo create --name my-new-repo --private
github-rest-cli repo create --name my-new-repo --org my-org
github-rest-cli repo create --name my-new-repo --empty
```

### Delete a repository

Prompts for confirmation unless `--yes` / `-y` is passed:

```shell
github-rest-cli repo delete --name my-repo
github-rest-cli repo delete --name my-repo --org my-org
github-rest-cli repo delete --name my-repo --yes
```

### Dependabot security updates

```shell
github-rest-cli dependabot enable --name my-repo
github-rest-cli dependabot disable --name my-repo
github-rest-cli dependabot enable --name my-repo --org my-org
```

### Deployment environments

```shell
github-rest-cli environment create --name my-repo --env production
github-rest-cli environment create --name my-repo --env staging --org my-org
```

## Output format

`repo get` and `repo list` support:

- `table` (default) — PrettyTable display
- `json` — JSON string suitable for piping or scripting

```shell
github-rest-cli repo list --format json
github-rest-cli repo get --name my-repo --format table
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local development, testing, linting, and Dynaconf tooling.

## Links

- [PyPI](https://pypi.org/project/github-rest-cli/)
- [Source](https://github.com/lbrealdev/github-rest-cli)
- [Issues](https://github.com/lbrealdev/github-rest-cli/issues)
- [License](LICENSE)
