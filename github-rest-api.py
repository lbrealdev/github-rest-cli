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


def rich_output(input: str, fmt: str) -> str:
    text = Text(input)
    text.stylize(fmt)
    console.print(text)


def get_repository(name: str) -> str:
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
        return False


def create_repository(name: str, public: str) -> str:
    data = {
        "name": name,
        "auto_init": "true",
        "private": public.lower() != "true",
    }
    resp = requests.post(f"{settings.API_URL}/user/repos", headers=headers, json=data)
    if resp.status_code == 201:
        rich_output("Repository created sucessfully!", fmt="blink bold green")
    elif resp.status_code == 422:
        rich_output(
            "Repository name already exists on this account!", fmt="blink bold red"
        )
    else:
        rich_output(
            f"Failed to create repository {name} with status code {resp.status_code}",
            fmt="blink bold red",
        )
        return False


def delete_repository(name: str) -> str:
    resp = requests.delete(
        f"{settings.API_URL}/repos/{settings.USER}/{name}", headers=headers
    )
    if resp.status_code == 204:
        rich_output("Repository deleted!", fmt="blink bold green")
    elif resp.status_code == 404:
        rich_output("Repository not found!", fmt="blink bold red")
    else:
        rich_output(
            f"Failed to delete repository {name} with status code {resp.status_code}",
            fmt="blink bold red",
        )
        return False


def list_repositories(limit: int, property: str, role: str) -> str:
    params = {"per_page": limit, "sort": property, "type": role}
    resp = requests.get(
        f"{settings.API_URL}/user/repos", headers=headers, params=params
    )
    if resp.status_code == 200:
        repos = json.loads(resp.text)
        repo_names = [repo["name"] for repo in repos]
        for repo_name in repo_names:
            rich_output(f"- {repo_name}", fmt="blink bold green")
    else:
        rich_output(
            f"Failed to list repositories for {settings.USER}\
                with status code {resp.status_code}",
            fmt="blink bold red",
        )
        return False


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
        "get-repository", help="Get repository data for authenticated user"
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

    # delete-repository function parser
    parser_delete_repository = subparsers.add_parser(
        "delete-repository", help="Delete repository"
    )
    parser_delete_repository.add_argument(
        "-n", "--name", help="Repository name to delete", required=True, dest="name"
    )

    args = parser.parse_args()

    if args.command == "get-repository":
        get_repository(args.name)
    elif args.command == "list-repository":
        list_repositories(args.limit, args.sort, args.role)
    elif args.command == "create-repository":
        create_repository(args.name, args.public)
    elif args.command == "delete-repository":
        delete_repository(args.name)
    else:
        return False


if __name__ == "__main__":
    main()
