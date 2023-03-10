import requests
import argparse
from config import settings
from rich.console import Console
from rich import print
from rich.text import Text
import json


console = Console()


headers = {
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"token {settings.AUTH_TOKEN}",
}


def rich_output(input: str, fmt: str) -> None:
    text = Text(input)
    text.stylize(fmt)
    console.print(text)


def get_repository(name: str) -> None:
    resp = requests.get(
        f"{settings.API_URL}/repos/{settings.USER}/{name}", headers=headers
    )
    if resp.status_code == 200:
        source_repo = json.loads(resp.text)
        print(source_repo)
    elif resp.status_code == 404:
        rich_output("The requested repository does not exist!", fmt="blink bold red")
    else:
        rich_output(
            f"Failed to get repository {name} with status code {resp.status_code}",
            fmt="blink bold red",
        )


def create_repository(name: str, public: str, org: str) -> None:
    data = {
        "name": name,
        "auto_init": "true",
        "private": public.lower() != "true",
    }
    if org is not None:
        resp_org = requests.post(
            f"{settings.API_URL}/orgs/{org}/repos", headers=headers, json=data
        )
        if resp_org.status_code == 201:
            rich_output(
                f"Repository sucessfully created in {org} organization",
                fmt="blink bold green"
            )
        else:
            rich_output(
                f"Failed to create repository {name} with status code\
                    {resp_org.status_code}",
                fmt="blink bold red",
            )
    else:
        resp = requests.post(
            f"{settings.API_URL}/user/repos", headers=headers, json=data
        )
        if resp.status_code == 201:
            rich_output("Repository created sucessfully!", fmt="blink bold green")
        elif resp.status_code == 422:
            rich_output(
                "Repository name already exists on this account!",
                fmt="blink bold red"
            )
        else:
            rich_output(
                f"Failed to create repository {name}\
                    with status code {resp.status_code}",
                fmt="blink bold red",
            )


def delete_repository(name: str, org: str) -> None:
    if org is not None:
        resp_org = requests.delete(
            f"{settings.API_URL}/repos/{org}/{name}", headers=headers
        )
        if resp_org.status_code == 204:
            rich_output(
                f"Repository sucessfully deleted in {org} organization",
                fmt="blink bold green"
            )
        elif resp_org.status_code == 403:
            rich_output(
                "You are not an admin of this repository", fmt="blink bold red"
            )
        elif resp_org.status_code == 404:
            rich_output(
                f"This repository was not found in the organization {org}",
                fmt="blink bold red"
            )
    else:
        resp = requests.delete(
            f"{settings.API_URL}/repos/{settings.USER}/{name}", headers=headers
        )
        if resp.status_code == 204:
            rich_output("Repository deleted sucessfully!", fmt="blink bold green")
        elif resp.status_code == 404:
            rich_output("Repository not found!", fmt="blink bold red")
        else:
            rich_output(
                f"Failed to delete repository {name}\
                    with status code {resp.status_code}",
                fmt="blink bold red",
            )


def list_repositories(limit: int, property: str, role: str) -> None:
    params = {"per_page": limit, "sort": property, "type": role}
    resp = requests.get(
        f"{settings.API_URL}/user/repos", headers=headers, params=params
    )
    if resp.status_code == 200:
        repos = json.loads(resp.text)
        repo_names = [repo["full_name"] for repo in repos]
        for repo_name in repo_names:
            rich_output(f"- {repo_name}", fmt="blink bold green")
        rich_output(f"\nTotal repositories: {len(repo_names)}", fmt="blink bold green")
    else:
        rich_output(
            f"Failed to list repositories for {settings.USER}\
                with status code {resp.status_code}",
            fmt="blink bold red",
        )


def vulnerability_alerts(name: str, option: str, org: str) -> None:
    if org is not None and option == "true":
        resp_org = requests.put(
            f"{settings.API_URL}/repos/{org}/{name}/vulnerability-alerts",
            headers=headers,
        )
        if resp_org.status_code == 204:
            rich_output(
                f"Enable vulnerability alerts\nRepository: {org}/{name}",
                fmt="blink bold green",
            )
        else:
            rich_output(
                f"Failed to enable vulnerability alerts for {name} repository with status code {resp_org.status_code}",
                fmt="blink bold red",
            )
    elif org is not None:
        resp_org = requests.delete(
            f"{settings.API_URL}/repos/{org}/{name}/vulnerability-alerts",
            headers=headers,
        )
        if resp_org.status_code == 204:
            rich_output(
                f"Disable vulnerability alerts\nRepository: {org}/{name}",
                fmt="blink bold green",
            )
        else:
            rich_output(
                f"Failed to enable vulnerability alerts for {name} repository with status code {resp.status_code}",
                fmt="blink bold red",
            )
    elif option == "true":
        resp = requests.put(
            f"{settings.API_URL}/repos/{settings.USER}/{name}/vulnerability-alerts",
            headers=headers,
        )
        if resp.status_code == 204:
            rich_output(
                f"Enable vulnerability alerts\nRepository: {settings.USER}/{name}",
                fmt="blink bold green",
            )
        else:
            rich_output(
                f"Failed to enable vulnerability alerts for {name} repository with status code {resp.status_code}",
                fmt="blink bold red",
            )
    else:
        resp = requests.delete(
            f"{settings.API_URL}/repos/{settings.USER}/{name}/vulnerability-alerts",
            headers=headers,
        )
        if resp.status_code == 204:
            rich_output(
                f"Disable vulnerability alerts\nRepository: {settings.USER}/{name}",
                fmt="blink bold green",
            )
        else:
            rich_output(
                f"Failed to enable vulnerability alerts for {name} repository with status code {resp.status_code}",
                fmt="blink bold red",
            )


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
        help="Get a specific repository from github",
        required=True,
        dest="name",
    )

    # list-repository function parser
    parser_list_repository = subparsers.add_parser(
        "list-repository", help="List repositories for authenticated user"
    )
    parser_list_repository.add_argument(
        "-r",
        "--role",
        help="Type role for list repositories",
        required=False,
        dest="role",
    )
    parser_list_repository.add_argument(
        "-l",
        "--limit",
        help="The number of results per page",
        required=False,
        default=50,
        dest="limit",
    )
    parser_list_repository.add_argument(
        "-s",
        "--sort",
        help="The property to sort the results by",
        required=False,
        default="pushed",
        dest="sort",
    )

    # create-repository function parser
    parser_create_repository = subparsers.add_parser(
        "create-repository", help="Create new repository"
    )
    parser_create_repository.add_argument(
        "-n", "--name", help="Name for new repository", required=True, dest="name"
    )
    parser_create_repository.add_argument(
        "-p",
        "--public",
        help="Whether the repository is private.",
        required=False,
        default="true",
        dest="public",
    )
    parser_create_repository.add_argument(
        "-o",
        "--org",
        help="The organization name",
        required=False,
        dest="org",
    )

    # delete-repository function parser
    parser_delete_repository = subparsers.add_parser(
        "delete-repository", help="Delete repository"
    )
    parser_delete_repository.add_argument(
        "-n", "--name", help="Repository name to delete", required=True, dest="name"
    )
    parser_delete_repository.add_argument(
        "-o",
        "--org",
        help="The organization name",
        required=False,
        dest="org",
    )

    # vulnerability-alerts function parser
    parser_vulnerability = subparsers.add_parser(
        "vulnerability", help="Enables vulnerability alerts for a repository"
    )
    parser_vulnerability.add_argument(
        "-n",
        "--name",
        help="Repository name to enable automated security fixes",
        required=True,
        dest="alerts",
    )
    parser_vulnerability.add_argument(
        "-e",
        "--enabled",
        help="Enable or disable vulnerability alerts",
        required=True,
        dest="enabled",
    )
    parser_vulnerability.add_argument(
        "-o",
        "--org",
        help="The organization name",
        dest="org",
    )


    args = parser.parse_args()

    if args.command == "get-repository":
        get_repository(args.name)
    elif args.command == "list-repository":
        list_repositories(args.limit, args.sort, args.role)
    elif args.command == "create-repository":
        create_repository(args.name, args.public, args.org)
    elif args.command == "delete-repository":
        delete_repository(args.name, args.org)
    elif args.command == "vulnerability":
        vulnerability_alerts(args.alerts, args.enabled, args.org)
    else:
        return False


if __name__ == "__main__":
    main()
