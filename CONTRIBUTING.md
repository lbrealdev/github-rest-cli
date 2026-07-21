# Contributing

Thanks for helping improve `github-rest-cli`. This guide covers local development, configuration, and quality tooling.

## Prerequisites

- Python 3.11.5+
- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just) (optional, wraps common tasks)
- [Ruff](https://docs.astral.sh/ruff/)
- [pre-commit](https://pre-commit.com/) (optional)

## Setup

Clone the repository, sync dependencies, and activate the virtualenv:

```shell
git clone https://github.com/lbrealdev/github-rest-cli.git
cd github-rest-cli
uv sync
source .venv/bin/activate
```

Install pre-commit hooks and Ruff (via just, if available):

```shell
just setup-pre-commit
just setup-ruff
```

Or install them yourself:

```shell
pre-commit install
uv tool install ruff
```

List installed packages:

```shell
uv pip list
```

## Authentication for local runs

Export a GitHub PAT the same way end users do:

```shell
export GITHUB_AUTH_TOKEN="<github-auth-token>"
```

Run the CLI entrypoint:

```shell
github-rest-cli --version
github-rest-cli --help
```

You can also profile a command:

```shell
just profile --help
# or with arguments, e.g.:
just profile repo list --format json
```

## Configuration

See [docs/configuration.md](docs/configuration.md) for environment variables, optional settings files, and Dynaconf tooling (`just dl` / `just dv`).

## Lint and format

```shell
just lint
just fmt
```

Equivalent:

```shell
ruff check .
ruff format .
```

## Tests

```shell
just test
# equivalent: pytest -v
```

## Build and publish (maintainers)

```shell
just build-local
just publish-local   # requires PYPI_TOKEN
```

Clean the uv cache:

```shell
just cache
```

## Pull requests

1. Create a branch from `main`
2. Keep changes focused
3. Run lint and tests before opening a PR
4. Link related issues (for example, `Fixes #72`)
