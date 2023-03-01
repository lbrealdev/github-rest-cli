import requests
import argparse
from config import settings
from rich.console import Console
from rich import print
import json


console = Console()


def get_repository(name: str) -> str:
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {settings.AUTH_TOKEN}",
    }
    resp = requests.get(
        f"{settings.API_URL}/repos/{settings.USER}/{name}", headers=headers
    )
    if resp.status_code == 200:
        source_repo = json.loads(resp.text)
        print(source_repo)
    elif resp.status_code == 404:
        console.print(
            "The requested repository does not exist!", style="blink bold red"
        )
    else:
        console.print(
            f"Failed to get repository {name} with status code {resp.status_code}",
            style="blink bold red",
        )
        return False


def create_repository(name: str, public: str) -> str:
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {settings.AUTH_TOKEN}",
    }
    data = {
        "name": name,
        "auto_init": "true",
        "private": public.lower() != "true",
    }
    resp = requests.post(f"{settings.API_URL}/user/repos", headers=headers, json=data)
    if resp.status_code == 201:
        console.print("Repository created sucessfully!", style="blink bold green")
    elif resp.status_code == 422:
        console.print(
            "Repository name already exists on this account!", style="blink bold red"
        )
    else:
        console.print(
            f"Failed to create repository {name} with status code {resp.status_code}",
            style="blink bold red",
        )
        return False


def delete_repository(name: str) -> str:
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {settings.AUTH_TOKEN}",
    }
    resp = requests.delete(
        f"{settings.API_URL}/repos/{settings.USER}/{name}", headers=headers
    )
    if resp.status_code == 204:
        console.print("Repository deleted!", style="blink bold green")
    elif resp.status_code == 404:
        console.print("Repository not found!", style="blink bold red")
    else:
        console.print(
            f"Failed to delete repository {name} with status code {resp.status_code}",
            style="blink bold red",
        )
        return False


def list_repository():
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {settings.AUTH_TOKEN}",
    }
    params = {"per_page": "100", "sort": "updated"}
    resp = requests.get(
        f"{settings.API_URL}/user/repos", headers=headers, params=params
    )
    if resp.status_code == 200:
        repos = json.loads(resp.text)
        repo_names = [repo["name"] for repo in repos]
        for repo_name in repo_names:
            print(f"- {repo_name}")
    else:
        console.print(
            f"Failed to list repositories for {settings.USER}\
                with status code {resp.status_code}",
            style="blink bold red",
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
    subparsers.add_parser(
        "list-repository", help="List repositories for authenticated user"
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
        list_repository()
    elif args.command == "create-repository":
        create_repository(args.name, args.public)
    elif args.command == "delete-repository":
        delete_repository(args.name)
    else:
        return False


if __name__ == "__main__":
    main()
