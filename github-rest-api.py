import requests
import argparse
import json
from config import settings
from rich.console import Console
from rich import print as rprint
from rich.text import Text


GITHUB_URL = f"{settings.API_URL}"
GITHUB_USER = f"{settings.USER}"
GITHUB_TOKEN = f"{settings.AUTH_TOKEN}"


console = Console()


headers = {
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"token {GITHUB_TOKEN}",
}


def rich_output(input: str, fmt: str):
    text = Text(input)
    text.stylize(fmt)
    console.print(text)


def get_repository(name: str, org: str):
    try:
        if org is None:
            req = requests.get(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}", headers=headers
            )
            req.raise_for_status()
            source_repo = json.loads(req.text)
            rprint(source_repo)
        elif org is not None:
            req = requests.get(
                f"{GITHUB_URL}/repos/{org}/{name}", headers=headers
            )
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
                f"Failed to get repository {name}\n" +
                f"Status code: {str(e.response.status_code)}",
                fmt="blink bold red"
            )


def create_repository(name: str, private: str, org: str):
    if private == 'true':
        is_private = True
    elif private == 'false':
        is_private = False
    else:
        is_private = False

    data = {
        "name": name,
        "auto_init": "true",
        "private": is_private,
    }

    try:
        if org is not None:
            req = requests.post(
                f"{GITHUB_URL}/orgs/{org}/repos", headers=headers, json=data
            )
            req.raise_for_status()
            rich_output(
                f"Repository sucessfully created in {org}/{name}",
                fmt="blink bold green",
            )
        else:
            req = requests.post(
                f"{GITHUB_URL}/user/repos", headers=headers, json=data
            )
            req.raise_for_status()
            rich_output(
                f"Repository sucessfully created in {GITHUB_USER}/{name}", 
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
                fmt="blink bold red"
            )
        else:
            rich_output(
                f"Failed to create repository {name}" +
                f"Status code: {e.response.status_code}",
                fmt="blink bold red",
            )


def delete_repository(name: str, org: str):
    try:
        if org is not None:
            req = requests.delete(
                f"{GITHUB_URL}/repos/{org}/{name}", headers=headers
            )
            req.raise_for_status()
            rich_output(
                f"Repository sucessfully deleted in {org}/{name}",
                fmt="blink bold green"
            )
        else:
            req = requests.delete(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}", headers=headers
            )
            req.raise_for_status()
            rich_output(
                f"Repository sucessfully deleted in {GITHUB_USER}/{name}", 
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
                "The requested repository was not found!", fmt="blink bold red",
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
        req = requests.get(
            f"{GITHUB_URL}/user/repos", headers=headers, params=params
        )
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
                f"Failed to list repositories for {GITHUB_USER}\n" +
                f"Status code: {e.response.status_code}",
                fmt="blink bold red",
            )


def dependabot_security(name: str, enabled: bool, org: str):
    if enabled == 'true':
        is_enabled = True
    elif enabled == 'false':
        is_enabled = False
    else:
        is_enabled = True

    try:
        if org is not None and is_enabled is True:
            for endpoint in ["vulnerability-alerts", "automated-security-fixes"]:
                req = requests.put(
                    f"{GITHUB_URL}/repos/{org}/{name}/{endpoint}",
                    headers=headers,
                )
                req.raise_for_status()
            rich_output(
                f"Dependabot has been activated on repository {org}/{name}",
                fmt="blink bold green",
            )
        elif org is not None:
            req = requests.delete(
                f"{GITHUB_URL}/repos/{org}/{name}/vulnerability-alerts",
                headers=headers,
            )
            req.raise_for_status()
            rich_output(
                f"Disable dependabot on repository: {org}/{name}",
                fmt="blink bold green"
            )
        else:
            if org is None and is_enabled is True:
                for endpoint in ["vulnerability-alerts", "automated-security-fixes"]:
                    req = requests.put(
                        f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/{endpoint}",
                        headers=headers,
                    )
                    req.raise_for_status()
                rich_output(
                    f"Dependabot has been activated on repository {GITHUB_USER}/{name}",
                    fmt="blink bold green",
                )
            elif org is None:
                req = requests.delete(
                    f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/vulnerability-alerts",
                    headers=headers,
                )
                req.raise_for_status()
                rich_output(
                    f"Disable dependabot on repository: {GITHUB_USER}/{name}",
                    fmt="blink bold green" 
                )
    except requests.exceptions.RequestException as e:
        rprint(f"Error: {e}")


def deployment_environment(name: str, env: str, org: str):
    try:
        if org is not None and env != "":
            req = requests.put(
                f"{GITHUB_URL}/repos/{org}/{name}/environments/{env}",
                headers=headers,
            )
            req.raise_for_status()
            rich_output(
                f"Create deployment environment {env.upper()}\n" +
                f"Repository: {org}/{name}",
                fmt="blink bold green"
            )
        elif env != "":
            req = requests.put(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/environments/{env}",
                headers=headers,
            )
            req.raise_for_status()
            rich_output(
                f"Create deployment environment {env.upper()}\n" +
                f"Repository: {GITHUB_USER}/{name}",
                fmt="blink bold green"
            )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            rich_output(
                f"Failed to create environment {env.upper()}",
                fmt="blink bold red"
            )    
        else:
            rprint(f"Error: {e}")


def main():
    # top-level parser
    parser = argparse.ArgumentParser(
        prog="Python Github REST API",
        description="Python CLI to Github REST API",
    )
    subparsers = parser.add_subparsers(
        help="Python Github REST API commands", dest="command"
    )

    # get-repository function parser
    parser_get_repository = subparsers.add_parser(
        "get-repository", help="Get repository information"
    )
    parser_get_repository.add_argument(
        "-n",
        "--name",
        help="The name of the repository.",
        required=True,
        dest="name",
    )
    parser_get_repository.add_argument(
        "-o",
        "--org",
        help="The organization name.",
        required=False,
        dest="org"
    )

    # list-repository function parser
    parser_list_repository = subparsers.add_parser(
        "list-repository", help="List repositories for authenticated user"
    )
    parser_list_repository.add_argument(
        "-r",
        "--role",
        required=False,
        dest="role",
        help="Type role for list repositories.",
    )
    parser_list_repository.add_argument(
        "-p",
        "--page",
        required=False,
        default=50,
        dest="page",
        help="The number of results per page.",
    )
    parser_list_repository.add_argument(
        "-s",
        "--sort",
        required=False,
        default="pushed",
        dest="sort",
        help="The property to sort the results by.",
    )

    # create-repository function parser
    parser_create_repository = subparsers.add_parser(
        "create-repository", help="Create new repository"
    )
    parser_create_repository.add_argument(
        "-n", 
        "--name", 
        required=True, 
        dest="name",
        help="The name of the repository.", 
    )
    parser_create_repository.add_argument(
        "-p",
        "--private",
        required=False,
        default=None,
        dest="private",
        help="Whether the repository is private.",
    )
    parser_create_repository.add_argument(
        "-o",
        "--org",
        required=False,
        dest="org",
        help="The organization name.",
    )

    # delete-repository function parser
    parser_delete_repository = subparsers.add_parser(
        "delete-repository", help="Delete repository"
    )
    parser_delete_repository.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The name of the repository.",
    )
    parser_delete_repository.add_argument(
        "-o",
        "--org",
        required=False,
        dest="org",
        help="The organization name.",
    )

    # dependabot function parser
    parser_dependabot = subparsers.add_parser(
        "dependabot", help="Github dependabot security"
    )
    parser_dependabot.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The name of the repository.",
    )
    parser_dependabot.add_argument(
        "-e",
        "--enabled",
        required=True,
        dest="enabled",
        help="Enable or disable dependabot.",
    )
    parser_dependabot.add_argument(
        "-o",
        "--org",
        dest="org",
        help="The organization name.",
    )

    # deployment environments function parses
    parser_environments = subparsers.add_parser(
        "environment", help="Github deployment environments"
    )
    parser_environments.add_argument(
        "-n",
        "--name",
        required=True,
        dest="name",
        help="The name of the repository.",
    )
    parser_environments.add_argument(
        "-e",
        "--env",
        required=True,
        dest="env",
        help="The name of the environment.",
    )
    parser_environments.add_argument(
        "-o",
        "--org",
        required=False,
        dest="org",
        help="The organization name.",
    )

    # guard clause pattern
    args = parser.parse_args()
    command = args.command

    if command == "get-repository":
        return get_repository(args.name, args.org)
    if command == "list-repository":
        return list_repositories(args.page, args.sort, args.role)
    if command == "create-repository":
        return create_repository(args.name, args.private, args.org)
    if command == "delete-repository":
        return delete_repository(args.name, args.org)
    if command == "dependabot":
        return dependabot_security(args.name, args.enabled, args.org)
    if command == "environment":
        return deployment_environment(args.name, args.env, args.org)
    return False


if __name__ == "__main__":
    main()
