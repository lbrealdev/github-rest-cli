# Authentication

`github-rest-cli` authenticates to the GitHub REST API with a personal access token (PAT).

## Create a token

Create a [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

### Classic PAT scopes

| Scope | Used for |
| --- | --- |
| `repo` | Private repos, create/delete, environments, Dependabot settings |
| `public_repo` | Public repositories only (subset of `repo`) |
| `delete_repo` | Deleting repositories (included in full `repo` on classic tokens) |

### Fine-grained tokens

Fine-grained tokens need repository access with permissions for Contents, Administration (create/delete), Environments, and Dependabot/security alerts as needed.

## Provide the token

### Environment variable (recommended)

```shell
export GITHUB_AUTH_TOKEN="<github-auth-token>"
```

### Settings file

You can also set `AUTH_TOKEN` in `.secrets.toml` (gitignored). See [Configuration](configuration.md) for `settings.toml` / `.secrets.toml` layout and Dynaconf environments.

```toml
# .secrets.toml
[default]
AUTH_TOKEN = "ghp_your_token_here"
```

Never commit tokens. Prefer `.secrets.toml` or the environment variable.

## Verify

```shell
github-rest-cli --version
github-rest-cli repo list
```

If the token is missing or invalid, API calls fail with an authorization error.

## See also

- [Configuration](configuration.md) — env vars, settings files, `API_URL`
- [CLI guide](cli.md) — commands and examples
