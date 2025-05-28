from github_rest_cli.config import settings
from rich import print as rprint


GITHUB_URL = "https://api.github.com"


def get_headers():
    token = settings.get("AUTH_TOKEN")
    if not token:
        rprint(
            "[bold red]Error: Environment variable GITHUB_AUTH_TOKEN is not set. Please set it and try again.[/bold red]"
        )
        raise SystemError(1)

    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {token}",
    }
