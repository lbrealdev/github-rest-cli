import argparse
from argparse import Namespace
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


class _HelpFormatter(argparse.HelpFormatter):
    """Widen the option column so flag help stays on one line."""

    def __init__(self, prog: str) -> None:
        super().__init__(prog, max_help_position=40)


def _add_repo_name_args(
    parser: argparse.ArgumentParser, *, name_required: bool = True
) -> None:
    parser.add_argument(
        "-n",
        "--name",
        help="The repository name",
        required=name_required,
        dest="name",
    )
    parser.add_argument(
        "-o", "--org", help="The organization name", required=False, dest="org"
    )


def _add_format_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-f",
        "--format",
        metavar="FORMAT",
        required=False,
        default="table",
        choices=["table", "json"],
        dest="format",
        help="Output format (table or json)",
    )


def run_get_repo(args: Namespace) -> None:
    repo = get_repository(args.name, args.org, args.format)
    if repo is not None:
        print(repo)  # noqa: T201


def run_list_repo(args: Namespace) -> None:
    repos = list_repositories(args.page, args.sort, args.role, args.format)
    if repos is not None:
        print(repos)  # noqa: T201


def run_create_repo(args: Namespace) -> None:
    create_repository(args.name, args.visibility, args.org, args.empty)


def run_delete_repo(args: Namespace) -> None:
    if not confirm_delete_repository(args.name, args.org, yes=args.yes):
        print("Aborted.")  # noqa: T201
        return
    delete_repository(args.name, args.org)


def run_dependabot(args: Namespace) -> None:
    dependabot_security(args.name, args.control, args.org)


def run_environment_create(args: Namespace) -> None:
    deployment_environment(args.name, args.env, args.org)


def _subcommand(
    subparsers: argparse._SubParsersAction,
    name: str,
    *,
    help: str,
) -> argparse.ArgumentParser:
    return subparsers.add_parser(name, help=help, formatter_class=_HelpFormatter)


def build_parser() -> argparse.ArgumentParser:
    """
    Create parsers and subparsers for CLI arguments
    """
    parser = argparse.ArgumentParser(
        description="Python CLI for GitHub REST API",
        formatter_class=_HelpFormatter,
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(help="GitHub REST API commands", dest="command")

    # repo {get,list,create,delete}
    repo_parser = _subcommand(subparsers, "repo", help="Manage repositories")
    repo_subparsers = repo_parser.add_subparsers(
        help="Repository commands", dest="repo_command"
    )
    repo_subparsers.required = True

    get_repo_parser = _subcommand(
        repo_subparsers, "get", help="Get a repository's details"
    )
    _add_repo_name_args(get_repo_parser)
    _add_format_arg(get_repo_parser)
    get_repo_parser.set_defaults(func=run_get_repo)

    list_repo_parser = _subcommand(
        repo_subparsers,
        "list",
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
    _add_format_arg(list_repo_parser)
    list_repo_parser.set_defaults(func=run_list_repo)

    create_repo_parser = _subcommand(
        repo_subparsers,
        "create",
        help="Create a new repository",
    )
    _add_repo_name_args(create_repo_parser)
    create_repo_parser.add_argument(
        "-v",
        "--visibility",
        metavar="VISIBILITY",
        required=False,
        default="public",
        dest="visibility",
        help="Repository visibility (e.g. public or private)",
    )
    create_repo_parser.add_argument(
        "-e",
        "--empty",
        required=False,
        action="store_true",
        dest="empty",
        help="Create an empty repository",
    )
    create_repo_parser.set_defaults(func=run_create_repo)

    delete_repo_parser = _subcommand(
        repo_subparsers,
        "delete",
        help="Delete an existing repository",
    )
    _add_repo_name_args(delete_repo_parser)
    delete_repo_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        dest="yes",
        help="Skip the confirmation prompt and delete immediately",
    )
    delete_repo_parser.set_defaults(func=run_delete_repo)

    # dependabot {enable,disable}
    dependabot_parser = _subcommand(
        subparsers,
        "dependabot",
        help="Manage Dependabot settings",
    )
    dependabot_subparsers = dependabot_parser.add_subparsers(
        help="Dependabot commands", dest="dependabot_command"
    )
    dependabot_subparsers.required = True

    dependabot_enable_parser = _subcommand(
        dependabot_subparsers,
        "enable",
        help="Enable Dependabot security updates",
    )
    _add_repo_name_args(dependabot_enable_parser)
    dependabot_enable_parser.set_defaults(func=run_dependabot, control=True)

    dependabot_disable_parser = _subcommand(
        dependabot_subparsers,
        "disable",
        help="Disable Dependabot security updates",
    )
    _add_repo_name_args(dependabot_disable_parser)
    dependabot_disable_parser.set_defaults(func=run_dependabot, control=False)

    # environment create
    environment_parser = _subcommand(
        subparsers,
        "environment",
        help="Manage deployment environments",
    )
    environment_subparsers = environment_parser.add_subparsers(
        help="Environment commands", dest="environment_command"
    )
    environment_subparsers.required = True

    environment_create_parser = _subcommand(
        environment_subparsers,
        "create",
        help="Create a deployment environment",
    )
    _add_repo_name_args(environment_create_parser)
    environment_create_parser.add_argument(
        "-e",
        "--env",
        required=True,
        dest="env",
        help="Deployment environment name",
    )
    environment_create_parser.set_defaults(func=run_environment_create)

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

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
