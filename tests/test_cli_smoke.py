import pytest
from github_rest_cli.main import build_parser, cli, __version__


def test_version_flag(capsys):
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--version"])

    assert exc_info.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_help_flag(capsys):
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--help"])

    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "repo" in out
    assert "dependabot" in out
    assert "environment" in out


def test_no_command_prints_help(mocker, capsys):
    mocker.patch("sys.argv", ["github-rest-cli"])

    cli()

    out = capsys.readouterr().out
    assert "GitHub REST API" in out or "usage:" in out.lower()


def test_repo_help_lists_subcommands(capsys):
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["repo", "--help"])

    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "get" in out
    assert "list" in out
    assert "create" in out
    assert "delete" in out


def test_repo_get_subcommand_help(capsys):
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["repo", "get", "--help"])

    assert exc_info.value.code == 0
    assert "--name" in capsys.readouterr().out
