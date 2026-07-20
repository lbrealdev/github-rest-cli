# Configuration

`github-rest-cli` uses Dynaconf for settings. Prefer environment variables; optional files are supported for local development.

## Environment variables (recommended)

| Variable | Setting | Required | Description |
| --- | --- | --- | --- |
| `GITHUB_AUTH_TOKEN` | `AUTH_TOKEN` | Yes | GitHub personal access token |
| `GITHUB_API_URL` | `API_URL` | No | GitHub REST API base URL (default: `https://api.github.com`) |
| `SET_ENV` | environment switcher | No | Active Dynaconf environment (`development`, `testing`, `production`, …) |

Example:

```shell
export GITHUB_AUTH_TOKEN="<github-auth-token>"
# optional:
export GITHUB_API_URL="https://api.github.com"
```

## Optional settings files

When present in the **current working directory**, Dynaconf loads:

1. `settings.toml`
2. `.secrets.toml` (gitignored; for local secrets)

File defaults for local clones live in the repository `settings.toml` (including `API_URL`). An installed package does not ship these files; env vars are enough.

## Contributor tooling

List defined parameters:

```shell
just dl
# equivalent: just dynaconf-list
```

Validate parameters:

```shell
just dv
# equivalent: just dynaconf-validate
```

Validation expects `dynaconf_validators.toml` at the project root.

Implementation lives in `src/github_rest_cli/config.py`.

## References

- [dynaconf/dynaconf](https://github.com/dynaconf/dynaconf)
- [Dynaconf documentation](https://www.dynaconf.com/)
- [Dynaconf API](https://www.dynaconf.com/api/)
