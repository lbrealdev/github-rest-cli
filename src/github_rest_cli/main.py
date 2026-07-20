import argparse
from github_rest_cli.api import (
    get_repository,
    create_repository,
    delete_repository,
    list_repositories,
    dependabot_security,
    deployment_environment,
)
from importlib.metadata import version
import logging


__version__ = version("github-rest-cli")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_parser() -> argparse.ArgumentParser:
    """
    Create parsers and subparsers for CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="Python CLI for GitHub REST API",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(help="GitHub REST API commands", dest="command")

    # Subparser for "get-repo" function
    get_repo_parser = subparsers.add_parser(
        "get-repo", help="Get a repository's details"
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
    get_repo_parser.add_argument(
        "-f",
        "--format",
        required=False,
        default="table",
        choices=["table", "json"],
        dest="format",
        help="Format to display the repository in",
    )
    get_repo_parser.set_defaults(func=get_repository)

    # Subparser for "list-repo" function
    list_repo_parser = subparsers.add_parser(
        "list-repo",
        help="List your repositories",
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
        default=20,
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
    list_repo_parser.add_argument(
        "-f",
        "--format",
        required=False,
        default="table",
        choices=["table", "json"],
        dest="format",
        help="Format to display the list of repositories in",
    )
    list_repo_parser.set_defaults(func=list_repositories)

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
    create_repo_parser.add_argument(
        "-e",
        "--empty",
        required=False,
        action="store_true",
        dest="empty",
        help="Create an empty repository",
    )
    create_repo_parser.set_defaults(func=create_repository)

    # Subparser for "delete-repository" function
    delete_repo_parser = subparsers.add_parser(
        "delete-repo",
        help="Delete an existing repository",
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
    delete_repo_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        dest="yes",
        help="Skip the confirmation prompt and delete immediately",
    )
    delete_repo_parser.set_defaults(func=delete_repository)

    # Subparser for "dependabot" function
    dependabot_parser = subparsers.add_parser(
        "dependabot",
        help="Manage Dependabot settings",
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
    control_group = dependabot_parser.add_mutually_exclusive_group(required=True)
    control_group.add_argument(
        "--enable",
        action="store_const",
        const=True,
        dest="control",
        help="Enable dependabot security updates",
    )
    control_group.add_argument(
        "--disable",
        action="store_const",
        const=False,
        dest="control",
        help="Disable dependabot security updates",
    )
    dependabot_parser.set_defaults(func=dependabot_security)

    # Subparser for "deployment-environments" function
    deploy_env_parser = subparsers.add_parser(
        "environment",
        help="Manage deployment environments",
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
    deploy_env_parser.set_defaults(func=deployment_environment)

    return parser


def confirm_delete_repository(
    name: str, org: str | None = None, *, yes: bool = False
) -> bool:
    """Return True if deletion should proceed."""
    if yes:
        return True

    target = f"{org}/{name}" if org else name
    answer = input(f"Delete repository '{target}'? This cannot be undone. [y/N] ")
    return answer.strip().lower() in {"y", "yes"}


def cli():
    parser = build_parser()
    args = parser.parse_args()
    command = args.command

    if hasattr(args, "func"):
        if command == "get-repo":
            repo = args.func(args.name, args.org, args.format)
            if repo is not None:
                print(repo)  # noqa: T201
        elif command == "list-repo":
            repos = args.func(args.page, args.sort, args.role, args.format)
            if repos is not None:
                print(repos)  # noqa: T201
        elif command == "create-repo":
            args.func(args.name, args.visibility, args.org, args.empty)
        elif command == "delete-repo":
            if not confirm_delete_repository(args.name, args.org, yes=args.yes):
                print("Aborted.")  # noqa: T201
                return
            args.func(args.name, args.org)
        elif command == "dependabot":
            args.func(args.name, args.control, args.org)
        elif command == "environment":
            args.func(args.name, args.env, args.org)
        else:
            return False
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
