# GitHub REST API

### Use

This python cli app uses dynaconf to manage secrets and environment variables.

So that you can use your secrets and environment variables declared in `settings.toml` or `.settings.toml`, use the `GITHUB` prefix value of `envvar_prefix` declared in config.py.

Set up python package dependencies in `pyproject.toml`:
```shell
uv sync
```

Activate `virtualenv`:
```shell
source .venv/bin/activate
```

Export required environment variables:
```shell
export GITHUB_USER="<github-username>"
export GITHUB_AUTH_TOKEN="<github-auth-token>"
```

Run the `github-rest-api` cli:
```shell
github-rest-api -h
```

### Dynaconfg

List all defined parameters: 
```shell
dynaconf -i github_rest_api.config.settings list
```

Validate all defined parameters:
```shell
dynaconf -i github_rest_api.config.settings validate
```

**NOTE:** `dynaconf_validators.toml` must exist.

### Ruff

Install ruff via uv:
```shell
uv tool install ruff
```

Run check:
```shell
ruff check .
```

Run format:
```shell
ruff format .
```
