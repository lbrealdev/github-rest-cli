import requests
import argparse
from config import settings
from rich.console import Console
from rich import print
from rich.text import Text
import json


GITHUB_URL = f"{settings.API_URL}"
GITHUB_USER = f"{settings.USER}"
GITHUB_TOKEN = f"{settings.AUTH_TOKEN}"


console = Console()


headers = {
    "X-GitHub-Api-Version": "2022-11-28",
    "Authorization": f"token {GITHUB_TOKEN}",
}


def rich_output(input: str, fmt: str) -> None:
    text = Text(input)
    text.stylize(fmt)
    console.print(text)


def get_repository(name: str, org: str) -> None:
    if org is None:
        get_user_repository_info = requests.get(
            f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}", headers=headers
        )
        
        status_code = get_user_repository_info.status_code

        if status_code == 200:
            source_repo = json.loads(get_user_repository_info.text)
            print(source_repo)
        elif status_code == 404:
            rich_output("The requested repository does not exist!", fmt="blink bold red")
        else:
            rich_output(
                f"Failed to get repository {name} with status code {status_code}",
                fmt="blink bold red",
            )
    elif org is not None:
        get_org_repository_info = requests.get(
            f"{GITHUB_URL}/repos/{org}/{name}", headers=headers
        )

        status_code = get_org_repository_info.status_code

        if status_code == 200:
            data_json = json.loads(get_org_repository_info.text)
            print(data_json)
        elif status_code == 404:
            rich_output(
                f"Repository not found on {org} organization",
                fmt="blink bold red",
            )
        else:
            rich_output(
                f"Failed to get repository {name} in organization {org}\n" +
                f"Status code: {status_code}",
                fmt="blink bold red"
            )
    else:
        print("Failed!")


def create_repository(name: str, public: str, org: str) -> None:
    data = {
        "name": name,
        "auto_init": "true",
        "private": public.lower() != "true",
    }
    if org is not None:
        resp_org = requests.post(
            f"{GITHUB_URL}/orgs/{org}/repos", headers=headers, json=data
        )
        if resp_org.status_code == 201:
            rich_output(
                f"Repository sucessfully created in {org}/{name}",
                fmt="blink bold green"
            )
        elif resp_org.status_code == 422:
            rich_output(
                f"Repository name already exists on this organization",
                fmt="blink bold red",
            )
        else:
            rich_output(
                f"Failed to create repository {name} in organization {org}\n" +
                f"Status code: {resp_org.status_code}",
                fmt="blink bold red"
            )
    else:
        resp = requests.post(
            f"{GITHUB_URL}/user/repos", headers=headers, json=data
        )
        if resp.status_code == 201:
            rich_output(
                f"Repository created sucessfully on {settings.USER}/{name}", 
                fmt="blink bold green",
            )
        elif resp.status_code == 422:
            rich_output(
                "Repository name already exists on this account!",
                fmt="blink bold red"
            )
        else:
            rich_output(
                f"Failed to create repository {settings.USER}/{name}" +
                f" with status code {resp.status_code}", fmt="blink bold red"
            )


def delete_repository(name: str, org: str) -> None:
    if org is not None:
        resp_org = requests.delete(
            f"{GITHUB_URL}/repos/{org}/{name}", headers=headers
        )
        if resp_org.status_code == 204:
            rich_output(
                f"Repository sucessfully deleted in {org}/{name}",
                fmt="blink bold green"
            )
        elif resp_org.status_code == 403:
            rich_output(
                "You are not an admin of this repository", fmt="blink bold red"
            )
        elif resp_org.status_code == 404:
            rich_output(
                f"Repository not found in organization {org}", fmt="blink bold red"
            )
            rich_output(f"Repository: {name}", fmt="blink bold red")
    else:
        resp = requests.delete(
            f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}", headers=headers
        )
        if resp.status_code == 204:
            rich_output(
                f"Repository deleted sucessfully on {GITHUB_USER}/{name}", 
                fmt="blink bold green",
            )
        elif resp.status_code == 404:
            rich_output("Repository not found!", fmt="blink bold red")
        else:
            rich_output(
                f"Failed to delete repository {GITHUB_USER}/{name}\
                    with status code {resp.status_code}",
                fmt="blink bold red",
            )


def list_repositories(limit: int, property: str, role: str) -> None:
    params = {"per_page": limit, "sort": property, "type": role}
    resp = requests.get(
        f"{GITHUB_URL}/user/repos", headers=headers, params=params
    )
    if resp.status_code == 200:
        repos = json.loads(resp.text)
        repo_names = [repo["full_name"] for repo in repos]
        for repo_name in repo_names:
            rich_output(f"- {repo_name}", fmt="blink bold green")
        rich_output(f"\nTotal repositories: {len(repo_names)}", fmt="blink bold green")
    else:
        rich_output(
            f"Failed to list repositories for {GITHUB_USER}\n" +
            f"Status code: {resp.status_code}",
            fmt="blink bold red",
        )


def dependabot_security(name: str, option: str, org: str) -> None:
    if org is not None:
        if option == "true":
            dependabot_on = requests.put(
                f"{GITHUB_URL}/repos/{org}/{name}/vulnerability-alerts",
                headers=headers,
            )
            status_code = dependabot_on.status_code
            if status_code == 204:
                rich_output(
                        f"Enable dependabot on repository: {org}/{name}",
                        fmt="blink bold green",
                    )
            else:
                rich_output(
                    f"Failed to enable dependabot for {org}/{name}\n" +
                    f"Status code: {status_code}",
                    fmt="blink bold red",
                )
        elif option == "false":
            dependabot_off = requests.delete(
                f"{GITHUB_URL}/repos/{org}/{name}/vulnerability-alerts",
                headers=headers,
            )           
            status_code = dependabot_off.status_code
            if status_code == 204:
                rich_output(
                    f"Disable dependabot on repository: {org}/{name}",
                    fmt="blink bold green"
                )
            else:
                rich_output(
                    f"Failed to disable dependabot for {org}/{name}\n" +
                    f"Status code: {status_code}",
                    fmt="blink bold red",
                )
    else:
        if option == "true":
            dependabot_on = requests.put(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/vulnerability-alerts",
                headers=headers,
            )
            status_code = dependabot_on.status_code
            if status_code == 204:
                rich_output(
                    f"Enable dependabot on repository: {GITHUB_USER}/{name}",
                    fmt="blink bold green",
                )
            else:
                rich_output(
                    f"Failed to enable dependabot for {GITHUB_USER}/{name}\n" +
                    f"Status code: {status_code}",
                    fmt="blink bold red",
                )
        elif option == "false":
            dependabot_off = requests.delete(
                f"{GITHUB_URL}/repos/{GITHUB_USER}/{name}/vulnerability-alerts",
                headers=headers,
            )
            status_code = dependabot_off.status_code
            if status_code == 204:
                rich_output(
                    f"Disable dependabot on repository: {GITHUB_USER}/{name}",
                    fmt="blink bold green",
                )
            else:
                rich_output(
                    f"Failed to disable dependabot for {GITHUB_USER}/{name}\n" +
                    f"Status code: {status_code}",
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
    parser_get_repository.add_argument(
        "-o",
        "--org",
        help="The organization name",
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

    # dependabot function parser
    parser_dependabot = subparsers.add_parser(
        "dependabot", help="Github dependabot security"
    )
    parser_dependabot.add_argument(
        "-n",
        "--name",
        help="Repository name to enable automated security fixes",
        required=True,
        dest="name",
    )
    parser_dependabot.add_argument(
        "-e",
        "--enabled",
        help="Enable or disable vulnerability alerts",
        required=True,
        dest="enabled",
    )
    parser_dependabot.add_argument(
        "-o",
        "--org",
        help="The organization name",
        dest="org",
    )


    args = parser.parse_args()

    if args.command == "get-repository":
        get_repository(args.name, args.org)
    elif args.command == "list-repository":
        list_repositories(args.limit, args.sort, args.role)
    elif args.command == "create-repository":
        create_repository(args.name, args.public, args.org)
    elif args.command == "delete-repository":
        delete_repository(args.name, args.org)
    elif args.command == "dependabot":
        dependabot_security(args.name, args.enabled, args.org)
    else:
        return False


if __name__ == "__main__":
    main()
