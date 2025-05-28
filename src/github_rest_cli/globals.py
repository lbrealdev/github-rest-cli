from github_rest_cli.config import settings
from github_rest_cli.utils import validate_github_token

GITHUB_URL = "https://api.github.com"


def get_headers():
    validate_github_token()
    return {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {settings.AUTH_TOKEN}",
    }
