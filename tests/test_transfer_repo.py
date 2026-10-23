from unittest.mock import MagicMock

import pytest

from github_rest_cli import api
from github_rest_cli.handlers.repos import confirm_transfer_repository
from github_rest_cli.main import cli
from github_rest_cli.parser import build_parser

GET_HEADERS_FUNCTION = "github_rest_cli.api.base.get_headers"
FETCH_USER_FUNCTION = "github_rest_cli.api.base.fetch_user"
REQUEST_HANDLER_FUNCTION = "github_rest_cli.api.base.request_with_handling"


def _post_response(payload):
    response = MagicMock()
    response.json.return_value = payload
    return response


def _users_response(account_type):
    response = MagicMock()
    response.json.return_value = {"type": account_type}
    return response


def test_transfer_repo_flags_parse():
    parser = build_parser()
    args = parser.parse_args(
        [
            "repo",
            "transfer",
            "--name",
            "my-repo",
            "--org",
            "my-org",
            "--new-owner",
            "other-org",
            "--new-name",
            "renamed-repo",
            "--yes",
            "--format",
            "json",
        ]
    )

    assert args.command == "repo"
    assert args.repo_command == "transfer"
    assert args.name == "my-repo"
    assert args.org == "my-org"
    assert args.new_owner == "other-org"
    assert args.new_name == "renamed-repo"
    assert args.yes is True
    assert args.format == "json"


def test_transfer_repo_requires_new_owner():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["repo", "transfer", "--name", "my-repo"])


def test_confirm_transfer_skips_prompt_with_yes(mocker):
    prompt = mocker.patch("github_rest_cli.handlers.repos.input")

    assert confirm_transfer_repository("my-repo", "other-user", yes=True) is True
    prompt.assert_not_called()


def test_confirm_transfer_accepts_yes(mocker):
    mocker.patch("github_rest_cli.handlers.repos.input", return_value="y")

    assert confirm_transfer_repository("my-repo", "other-user", org="my-org") is True


def test_confirm_transfer_rejects_other_answers(mocker):
    mocker.patch("github_rest_cli.handlers.repos.input", return_value="n")

    assert confirm_transfer_repository("my-repo", "other-user") is False


def test_cli_transfer_repo_aborts_without_confirmation(mocker, capsys):
    mocker.patch(
        "github_rest_cli.handlers.repos.confirm_transfer_repository",
        return_value=False,
    )
    transfer_mock = mocker.patch("github_rest_cli.handlers.repos.transfer_repository")
    mocker.patch(
        "sys.argv",
        [
            "github-rest-cli",
            "repo",
            "transfer",
            "--name",
            "my-repo",
            "--new-owner",
            "other-user",
        ],
    )

    cli()

    transfer_mock.assert_not_called()
    assert "Aborted." in capsys.readouterr().out


def test_cli_transfer_repo_proceeds_with_yes(mocker):
    transfer_mock = mocker.patch("github_rest_cli.handlers.repos.transfer_repository")
    prompt = mocker.patch("github_rest_cli.handlers.repos.input")
    mocker.patch(
        "sys.argv",
        [
            "github-rest-cli",
            "repo",
            "transfer",
            "--name",
            "my-repo",
            "--new-owner",
            "other-user",
            "--yes",
        ],
    )

    cli()

    prompt.assert_not_called()
    transfer_mock.assert_called_once_with(
        "my-repo",
        "other-user",
        None,
        new_name=None,
        team_ids=None,
        output_format="table",
    )


def test_cli_transfer_repo_passes_team_ids(mocker):
    transfer_mock = mocker.patch("github_rest_cli.handlers.repos.transfer_repository")
    mocker.patch(
        "sys.argv",
        [
            "github-rest-cli",
            "repo",
            "transfer",
            "--name",
            "my-repo",
            "--new-owner",
            "other-org",
            "--team-ids",
            "12,34",
            "--yes",
        ],
    )

    cli()

    transfer_mock.assert_called_once_with(
        "my-repo",
        "other-org",
        None,
        new_name=None,
        team_ids=[12, 34],
        output_format="table",
    )


def test_cli_transfer_repo_prints_json_output(mocker, capsys):
    mocker.patch(
        "github_rest_cli.handlers.repos.transfer_repository",
        return_value='{"full_name": "other-org/my-repo"}',
    )
    mocker.patch(
        "sys.argv",
        [
            "github-rest-cli",
            "repo",
            "transfer",
            "--name",
            "my-repo",
            "--new-owner",
            "other-org",
            "--yes",
            "--format",
            "json",
        ],
    )

    cli()

    assert '"full_name": "other-org/my-repo"' in capsys.readouterr().out


def test_transfer_repository_api_request_body(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.transfer_repository("my-repo", "other-org", org="my-org", new_name="renamed")

    request_mock.assert_called_once()
    call = request_mock.call_args
    assert call.args[0] == "POST"
    assert call.args[1].endswith("/repos/my-org/my-repo/transfer")
    assert call.kwargs["json"] == {"new_owner": "other-org", "new_name": "renamed"}


def test_transfer_repository_api_request_body_with_team_ids(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.transfer_repository("my-repo", "other-org", org="my-org", team_ids=[12, 34])

    assert request_mock.call_args.kwargs["json"] == {
        "new_owner": "other-org",
        "team_ids": [12, 34],
    }


def test_transfer_repository_202_prints_processing_message(mocker, capsys):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    request_mock = mocker.patch(
        REQUEST_HANDLER_FUNCTION,
        side_effect=[_post_response({"full_name": "other-org/my-repo"})],
    )

    result = api.transfer_repository("my-repo", "other-org", org="my-org")

    assert result is None
    request_mock.assert_called_once()
    output = capsys.readouterr().out
    assert "accepted and is being processed" in output
    assert "other-org/my-repo" in output
    assert "pending" not in output
    assert "personal account" in output


def test_transfer_repository_json_format(mocker, capsys):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(
        REQUEST_HANDLER_FUNCTION,
        side_effect=[
            _post_response({"full_name": "other-org/my-repo"}),
            _users_response("Organization"),
        ],
    )

    result = api.transfer_repository(
        "my-repo", "other-org", org="my-org", output_format="json"
    )

    assert result is not None
    assert '"full_name": "other-org/my-repo"' in result


def test_transfer_repository_error_paths_return_none(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    assert api.transfer_repository("my-repo", "other-org", org="my-org") is None

    error_msg = request_mock.call_args.kwargs["error_msg"]
    assert set(error_msg) >= {403, 404, 422}


def test_repo_help_lists_transfer(capsys):
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["repo", "--help"])

    assert "transfer" in capsys.readouterr().out
