import requests
import argparse
import json
from github_rest_api.config import settings
from rich.console import Console
from rich import print as rprint
from rich.text import Text


GITHUB_URL = f"{settings.API_URL}"
GITHUB_USER = f"{settings.USER}"
GITHUB_TOKEN = f"{settings.AUTH_TOKEN}"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"token {GITHUB_TOKEN}",
}


def rich_output(input: str, fmt: str):
    console = Console()
    text = Text(input)
    text.stylize(fmt)
    console.print(text)


def get_repository(name: str, org: str):
    try:
        if org is None:
            req = requests.get(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}", headers=HEADERS
            )
            req.raise_for_status()
            source_repo = json.loads(req.text)
            rprint(source_repo)
        elif org is not None:
            req = requests.get(f"{GITHUB_URL}/repos/{org}/{name}", headers=HEADERS)
            req.raise_for_status()
            source_repo = json.loads(req.text)
            rprint(source_repo)
        else:
            rprint("Failed!")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            rich_output(
                "Unauthorized access. Please check your token or credentials.",
                fmt="blink bold red",
            )
        elif e.response.status_code == 404:
            rich_output(
                "The requested repository does not exist!", fmt="blink bold red"
            )
        else:
            rich_output(
                f"Failed to get repository {name}\n"
                + f"Status code: {str(e.response.status_code)}",
                fmt="blink bold red",
            )


def create_repository(name: str, visibility: str, org: str):
    data = {
        "name": name,
        "auto_init": "true",
        "visibility": visibility,
    }

    if visibility == "private":
        data["private"] = True

    try:
        url = f"{GITHUB_URL}/orgs/{org}/repos" if org else f"{GITHUB_URL}/user/repos"
        req = requests.post(url, headers=HEADERS, json=data)
        req.raise_for_status()
        rich_output(
            f"Repository successfully created in {org or GITHUB_USER}/{name}",
            fmt="blink bold green",
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            rich_output(
                "Unauthorized access. Please check your token or credentials.",
                fmt="blink bold red",
            )
        elif e.response.status_code == 422:
            rich_output(
                "Repository name already exists on this account or organization!",
                fmt="blink bold red",
            )
        else:
            rich_output(
                f"Failed to create repository {name}\
                    Status code: {e.response.status_code}",
                fmt="blink bold red",
            )


def delete_repository(name: str, org: str):
    try:
        url = (
            f"{GITHUB_URL}/repos/{org}/{name}"
            if org
            else f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}"
        )
        req = requests.delete(url, headers=HEADERS)
        req.raise_for_status()
        rich_output(
            f"Repository sucessfully deleted in {org or GITHUB_USER}/{name}",
            fmt="blink bold green",
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            rich_output(
                "You are not an admin of this repository!",
                fmt="blink bold red",
            )
        elif e.response.status_code == 404:
            rich_output(
                "The requested repository was not found!",
                fmt="blink bold red",
            )
        else:
            rich_output(
                f"Failed to delete repository {name}\
                    with status code {e.response.status_code}",
                fmt="blink bold red",
            )


def list_repositories(page: int, property: str, role: str):
    try:
        params = {"per_page": page, "sort": property, "type": role}
        req = requests.get(f"{GITHUB_URL}/user/repos", headers=HEADERS, params=params)
        req.raise_for_status()
        repositories = json.loads(req.text)
        repository_full_name = [repo["full_name"] for repo in repositories]
        for repos in repository_full_name:
            rich_output(f"- {repos}", fmt="blink bold green")
        rich_output(
            f"\nTotal repositories: {len(repository_full_name)}",
            fmt="blink bold green",
        )

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            rich_output(
                "Unauthorized access. Please check your token or credentials.",
                fmt="blink bold red",
            )
        else:
            rich_output(
                f"Failed to list repositories for {GITHUB_USER} Status code: {e.response.status_code}",
                fmt="blink bold red",
            )


def dependabot_security(name: str, org: str, enabled: bool):
    is_enabled = bool(enabled)

    try:
        if org is not None and is_enabled is True:
            for endpoint in ["vulnerability-alerts", "automated-security-fixes"]:
                req = requests.put(
                    f"{GITHUB_URL}/repos/{org}/{name}/{endpoint}", headers=HEADERS
                )
                req.raise_for_status()
            rich_output(
                f"Dependabot has been activated on repository {org}/{name}",
                fmt="blink bold green",
            )
        elif org is not None:
            req = requests.delete(
                f"{GITHUB_URL}/repos/{org}/{name}/vulnerability-alerts",
                headers=HEADERS,
            )
            req.raise_for_status()
            rich_output(
                f"Disable dependabot on repository: {org}/{name}",
                fmt="blink bold green",
            )
        else:
            if org is None and is_enabled is True:
                for endpoint in ["vulnerability-alerts", "automated-security-fixes"]:
                    req = requests.put(
                        f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/{endpoint}",
                        headers=HEADERS,
                    )
                    req.raise_for_status()
                rich_output(
                    f"Dependabot has been activated on repository {GITHUB_USER}/{name}",
                    fmt="blink bold green",
                )
            elif org is None:
                req = requests.delete(
                    f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/vulnerability-alerts",
                    headers=HEADERS,
                )
                req.raise_for_status()
                rich_output(
                    f"Disable dependabot on repository: {GITHUB_USER}/{name}",
                    fmt="blink bold green",
                )
    except requests.exceptions.RequestException as e:
        rprint(f"Error: {e}")


def deployment_environment(name: str, env: str, org: str):
    try:
        if org is not None and env != "":
            req = requests.put(
                f"{GITHUB_URL}/repos/{org}/{name}/environments/{env}",
                headers=HEADERS,
            )
            req.raise_for_status()
            rich_output(
                f"New deployment environment created - {env.upper()}\n"
                + f"Repository: {org}/{name}",
                fmt="blink bold green",
            )
        elif env != "":
            req = requests.put(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/environments/{env}",
                headers=HEADERS,
            )
            req.raise_for_status()
            rich_output(
                f"New deployment environment created - {env.upper()}\n"
                + f"Repository: {GITHUB_USER}/{name}",
                fmt="blink bold green",
            )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            rich_output(
                f"Failed to create environment {env.upper()}", fmt="blink bold red"
            )
        else:
            rprint(f"Error: {e}")


def cli():
    """
    Create parsers and subparsers for CLI arguments
    """
    global_parser = argparse.ArgumentParser(
        description="Python CLI to GitHub REST API",
    )
    subparsers = global_parser.add_subparsers(
        help="Python GitHub REST API commands", dest="command"
    )

    # Subparser for "get-repository" function
    get_repo_parser = subparsers.add_parser(
        "get-repo", help="Get repository information"
    )
    get_repo_parser.add_argument(
        "-n",
        "--name",
        help="The repository name",
        required=True,
        dest="name",
    )
    get_repo_parser.add_argument(
        "-o", "--org", help="The organization name", required=False, dest="org"
    )

    # Subparser for "list-repository" function
    list_repo_parser = subparsers.add_parser(
        "list-repo",
        help="List repositories for authenticated user",
    )
    list_repo_parser.add_argument(
        "-r",
        "--role",
        required=False,
        dest="role",
        help="List repositories by role",
    )
    list_repo_parser.add_argument(
        "-p",
        "--page",
        required=False,
        default=50,
        type=int,
        dest="page",
        help="The number of results",
    )
    list_repo_parser.add_argument(
        "-s",
        "--sort",
        required=False,
        default="pushed",
        dest="sort",
        help="List repositories sorted by",
    )

    # Subparser for "create-repository" function
    create_repo_parser = subparsers.add_parser(
        "create-repo",
        help="Create a new repository",
    )
    create_repo_parser.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The repository name",
    )
    create_repo_parser.add_argument(
        "-v",
        "--visibility",
        required=False,
        default="public",
        dest="visibility",
        help="Whether the repository is private",
    )
    create_repo_parser.add_argument(
        "-o",
        "--org",
        required=False,
        dest="org",
        help="The organization name",
    )

    # Subparser for "delete-repository" function
    delete_repo_parser = subparsers.add_parser(
        "delete-repo",
        help="Delete a repository",
    )
    delete_repo_parser.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The repository name",
    )
    delete_repo_parser.add_argument(
        "-o",
        "--org",
        required=False,
        dest="org",
        help="The organization name",
    )

    # Subparser for "delete-repository" function
    dependabot_parser = subparsers.add_parser(
        "dependabot",
        help="Github Dependabot security updates",
    )
    dependabot_parser.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The repository name",
    )
    dependabot_parser.add_argument(
        "-o",
        "--org",
        dest="org",
        help="The organization name",
    )
    dependabot_parser.add_argument(
        "--enable",
        required=False,
        action="store_true",
        dest="control",
        help="Enable dependabot security updates",
    )
    dependabot_parser.add_argument(
        "--disable",
        required=False,
        action="store_false",
        dest="control",
        help="Disable dependabot security updates",
    )

    # Subparser for "deployment-environments" function
    deploy_env_parser = subparsers.add_parser(
        "environment",
        help="Github Deployment environments",
    )
    deploy_env_parser.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The repository name",
    )
    deploy_env_parser.add_argument(
        "-e",
        "--env",
        required=True,
        dest="env",
        help="Deployment environment name",
    )
    deploy_env_parser.add_argument(
        "-o",
        "--org",
        required=False,
        dest="org",
        help="The organization name",
    )

    # guard clause pattern
    args = global_parser.parse_args()
    command = args.command

    if command == "get-repo":
        return get_repository(args.name, args.org)
    if command == "list-repo":
        return list_repositories(args.page, args.sort, args.role)
    if command == "create-repo":
        return create_repository(args.name, args.visibility, args.org)
    if command == "delete-repo":
        return delete_repository(args.name, args.org)
    if command == "dependabot":
        return dependabot_security(args.name, args.org, args.control)
    if command == "environment":
        return deployment_environment(args.name, args.env, args.org)
    return False


if __name__ == "__main__":
    cli()
