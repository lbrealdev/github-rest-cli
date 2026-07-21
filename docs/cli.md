# CLI guide

Command reference for `github-rest-cli`. The CLI uses nested groups:

```text
github-rest-cli <command> <subcommand> [options]
```

For tokens and PAT scopes, see [Authentication](authentication.md). For settings files and API URL, see [Configuration](configuration.md).

## Global options

```shell
github-rest-cli --help
github-rest-cli --version
```

| Option | Description |
| --- | --- |
| `-h` / `--help` | Show help |
| `-v` / `--version` | Show package version |

## Command groups

| Group | Purpose |
| --- | --- |
| `repo` | Get, list, create, and delete repositories |
| `dependabot` | Enable or disable Dependabot security updates |
| `environment` | Create deployment environments |

```shell
github-rest-cli repo --help
github-rest-cli dependabot --help
github-rest-cli environment --help
```

## `repo`

### `repo get`

Fetch details for one repository.

```shell
github-rest-cli repo get --name my-repo
github-rest-cli repo get --name my-repo --org my-org
github-rest-cli repo get --name my-repo --format json
```

| Flag | Required | Default | Description |
| --- | --- | --- | --- |
| `-n` / `--name` | Yes | — | Repository name |
| `-o` / `--org` | No | authenticated user | Organization owner |
| `-f` / `--format` | No | `table` | Output format: `table` or `json` |

### `repo list`

List repositories for the authenticated user.

```shell
github-rest-cli repo list
github-rest-cli repo list --page 50 --sort pushed
github-rest-cli repo list --role owner --format json
```

| Flag | Required | Default | Description |
| --- | --- | --- | --- |
| `-p` / `--page` | No | `20` | Number of results (`per_page`) |
| `-s` / `--sort` | No | `pushed` | Sort field (e.g. `pushed`, `updated`, `created`) |
| `-r` / `--role` | No | unset | Filter by affiliation/role |
| `-f` / `--format` | No | `table` | Output format: `table` or `json` |

`--format` only changes presentation. Table and JSON use the same repository set and the same fields: `name`, `owner`, `url`, `visibility`.

### `repo create`

Create a repository. Visibility defaults to **public** when none of the visibility flags is passed.

```shell
github-rest-cli repo create --name my-new-repo
github-rest-cli repo create --name my-new-repo --private
github-rest-cli repo create --name my-new-repo --public
github-rest-cli repo create --name my-new-repo --internal
github-rest-cli repo create --name my-new-repo --org my-org
github-rest-cli repo create --name my-new-repo --empty
```

| Flag | Required | Default | Description |
| --- | --- | --- | --- |
| `-n` / `--name` | Yes | — | Repository name |
| `-o` / `--org` | No | authenticated user | Create under an organization |
| `--public` | No | default when omitted | Public repository |
| `--private` | No | — | Private repository |
| `--internal` | No | — | Internal repository (org) |
| `-e` / `--empty` | No | off | Create without an initial commit / README |

`--public`, `--private`, and `--internal` are mutually exclusive.

### `repo delete`

Delete a repository. Prompts for confirmation unless `--yes` is passed.

```shell
github-rest-cli repo delete --name my-repo
github-rest-cli repo delete --name my-repo --org my-org
github-rest-cli repo delete --name my-repo --yes
```

| Flag | Required | Default | Description |
| --- | --- | --- | --- |
| `-n` / `--name` | Yes | — | Repository name |
| `-o` / `--org` | No | authenticated user | Organization owner |
| `-y` / `--yes` | No | off | Skip confirmation prompt |

## `dependabot`

### `dependabot enable` / `dependabot disable`

Enable or disable Dependabot security updates for a repository.

```shell
github-rest-cli dependabot enable --name my-repo
github-rest-cli dependabot disable --name my-repo
github-rest-cli dependabot enable --name my-repo --org my-org
```

| Flag | Required | Default | Description |
| --- | --- | --- | --- |
| `-n` / `--name` | Yes | — | Repository name |
| `-o` / `--org` | No | authenticated user | Organization owner |

## `environment`

### `environment create`

Create a deployment environment on a repository.

```shell
github-rest-cli environment create --name my-repo --env production
github-rest-cli environment create --name my-repo --env staging --org my-org
```

| Flag | Required | Default | Description |
| --- | --- | --- | --- |
| `-n` / `--name` | Yes | — | Repository name |
| `-e` / `--env` | Yes | — | Environment name |
| `-o` / `--org` | No | authenticated user | Organization owner |

## Output format

`repo get` and `repo list` support:

- `table` (default) — PrettyTable display
- `json` — JSON string suitable for piping or scripting

```shell
github-rest-cli repo list --format json
github-rest-cli repo get --name my-repo --format table
```

## Breaking changes (nested CLI)

Older flat commands were removed:

| Old | New |
| --- | --- |
| `get-repo` | `repo get` |
| `list-repo` | `repo list` |
| `create-repo` | `repo create` |
| `delete-repo` | `repo delete` |
| `dependabot --enable` / `--disable` | `dependabot enable` / `dependabot disable` |
| `environment ...` | `environment create ...` |
| `create-repo --visibility private` | `repo create --private` |
