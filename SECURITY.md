# Security

`github-rest-cli` is a local CLI. It calls the GitHub REST API with a personal access token and prints repository and environment data to the terminal. It is not a network service.

## Scope

Reports are about `github-rest-cli` itself: how it reads the token, which API origin it sends that token to, and how it prints or follows data the API returns. A report has to name something the tool does with the token, the working directory it is run from, or the API data it renders.

Vulnerabilities in GitHub, in the terminal emulator, or in the packages `github-rest-cli` depends on are out of scope. Report those to the projects that own them.

## Reporting a vulnerability

Report through a GitHub private vulnerability advisory on this repository. Do not open a public issue for a vulnerability that has not been disclosed yet.

In the advisory, share the version you used, the command you ran, and what you observed. Do not paste the token, a `.secrets.toml`, or command output that contains a credential.

Treat a report as confidential until a fixed release is out.

## Supported versions

Only the latest release receives fixes; older releases are not patched.

## Trust boundary

The person running the CLI is trusted. The environment that person set is inside the boundary:

- `GITHUB_AUTH_TOKEN` — the token sent on API requests.
- `GITHUB_API_URL` — the API origin. When it is unset, the origin is `https://api.github.com`.

`settings.toml` and `.secrets.toml` in the working directory are also loaded. They can set `API_URL` and `AUTH_TOKEN`. Those files are not a directory the tool created for itself. Anything that can write the working directory can choose the origin the token is sent to, or can supply the token the tool will use. Do not run the CLI from a directory you do not control.

These inputs are outside the boundary:

- API response bodies, including `Link` headers
- repository and environment fields that are printed
- command arguments that become parts of the request URL

The CLI does not invoke a shell. JSON output is encoded with `json.dumps`. Table output prints API strings as they were returned. `repo list --all` and `environment list --all` follow the next-page URL from the `Link` header. The next-page URL is requested with the same token and is not checked against the API origin.

## What to treat as secret

The token can read and change repositories the account can access. Treat it as secret:

- `GITHUB_AUTH_TOKEN` and `AUTH_TOKEN`
- `.secrets.toml`
- shell history or logs that captured the token
- API output from private repositories

Do not commit `.secrets.toml`.
