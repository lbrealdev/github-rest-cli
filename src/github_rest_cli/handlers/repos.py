from argparse import Namespace

from github_rest_cli.api import (
    create_repository,
    delete_repository,
    get_repository,
    list_repositories,
    transfer_repository,
    update_repository,
)


def run_get_repo(args: Namespace) -> None:
    repo = get_repository(args.name, args.org, args.format)
    if repo is not None:
        print(repo)  # noqa: T201


def run_list_repo(args: Namespace) -> None:
    repos = list_repositories(
        args.per_page,
        args.page,
        args.sort,
        args.role,
        args.format,
        fetch_all=args.fetch_all,
        org=args.org,
    )
    if repos is not None:
        print(repos)  # noqa: T201


def run_create_repo(args: Namespace) -> None:
    create_repository(
        args.name,
        args.visibility,
        args.org,
        empty=args.empty,
        template=args.template,
        include_all_branches=args.include_all_branches,
    )


def run_update_repo(args: Namespace) -> None:
    update_repository(
        args.name,
        args.org,
        new_name=args.new_name,
        description=args.description,
        homepage=args.homepage,
        visibility=args.visibility,
        default_branch=args.default_branch,
        archived=args.archived,
        is_template=args.is_template,
    )


def run_delete_repo(args: Namespace) -> None:
    if not confirm_delete_repository(args.name, args.org, yes=args.yes):
        print("Aborted.")  # noqa: T201
        return
    delete_repository(args.name, args.org)


def run_transfer_repo(args: Namespace) -> None:
    if not confirm_transfer_repository(
        args.name,
        args.new_owner,
        org=args.org,
        new_name=args.new_name,
        yes=args.yes,
    ):
        print("Aborted.")  # noqa: T201
        return
    result = transfer_repository(
        args.name,
        args.new_owner,
        args.org,
        new_name=args.new_name,
        team_ids=args.team_ids,
        output_format=args.format,
    )
    if result is not None:
        print(result)  # noqa: T201


def confirm_transfer_repository(
    name: str,
    new_owner: str,
    org: str | None = None,
    new_name: str | None = None,
    *,
    yes: bool = False,
) -> bool:
    """Return True if the transfer should proceed."""
    if yes:
        return True

    target = f"{org}/{name}" if org else name
    rename = f" and rename it to '{new_name}'" if new_name else ""
    answer = input(
        f"Transfer repository '{target}' to '{new_owner}'{rename}? "
        "This changes who owns the repository. [y/N] "
    )
    return answer.strip().lower() in {"y", "yes"}


def confirm_delete_repository(
    name: str, org: str | None = None, *, yes: bool = False
) -> bool:
    """Return True if deletion should proceed."""
    if yes:
        return True

    target = f"{org}/{name}" if org else name
    answer = input(f"Delete repository '{target}'? This cannot be undone. [y/N] ")
    return answer.strip().lower() in {"y", "yes"}
