# Security Policy

## Reporting a vulnerability

Please report security problems in private, not in a public issue.

The preferred route is GitHub private vulnerability reporting for
[lbrealdev/github-rest-cli](https://github.com/lbrealdev/github-rest-cli):

1. Open the repository's **Security** tab.
2. Click **Report a vulnerability**.
3. Fill in the advisory form.

If you cannot use that form, email **lbrealdeveloper@gmail.com** instead.

Please do not open a public issue, discussion, or pull request for a vulnerability
that has not been disclosed yet. A public report can expose other users before a
fix is available.

## What to include

- The affected version (`github-rest-cli --version`).
- What you ran: the command, the options, and the kind of repository or account
  it was pointed at.
- What happened and what impact you think it has.
- Whether a GitHub token or any other credential was exposed, and if so, which
  one. Do not paste the token itself.

A short, precise report is more useful than a long one. If you are unsure whether
something is a security issue, report it privately and let the maintainer decide.

## Supported versions

The current release is **2.0.0**. Only the current release line is supported.
Older releases do not receive security fixes.

Security fixes are published in a new release when one is ready. Upgrading to the
latest version from [PyPI](https://pypi.org/project/github-rest-cli/) is the way to
pick them up.

## Scope

This policy covers the `github-rest-cli` package and the code in this repository.
The areas of most interest are:

- **Credential handling.** The GitHub token is read from the `GITHUB_AUTH_TOKEN`
  environment variable or from `AUTH_TOKEN` in the optional local secrets file,
  and is sent in the `Authorization` header of requests to the GitHub REST API
  origin configured by `API_URL`. The default origin is `https://api.github.com`.
  Problems with how the token is read, stored in memory, or sent to an origin
  other than the configured one are in scope.
- **Authenticated requests.** This includes request construction, header
  handling, and pagination, where `--all` follows the next-page links returned
  by the API.
- **Terminal rendering.** API text such as repository names, descriptions, and
  environment fields is printed to the terminal in tables or JSON. Problems
  where that text is rendered in a way that affects the terminal or the user's
  session are in scope.
- **The publish workflow.** The package is built and published to PyPI by the
  release workflow using Trusted Publishing when a GitHub Release is created.
  Problems in that build or publish path are in scope.

Out of scope:

- Vulnerabilities in GitHub itself, the GitHub REST API, or GitHub's own
  infrastructure. Report those to GitHub through its own security program.
- Vulnerabilities in the terminal emulator or shell the operator uses.
- Vulnerabilities in third-party packages that are not reached through this
  project's install or release path.

## What to expect

This is a small project maintained by one person. The maintainer will reply when
they can. There is no response-time commitment, no bug bounty, and no promised
patch date. When a fix is ready, it will land in a release.

Please give the maintainer a reasonable chance to release a fix before
disclosing the issue publicly.
