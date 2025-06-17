from github_rest_cli import api


def test_fetch_user(mocker):
    mocker.patch(
        "github_rest_cli.api.get_headers", return_value={"Authorization": "token fake"}
    )

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"login": "test-user"}
    mock_response.raise_for_status = lambda: None

    mocker.patch(
        "github_rest_cli.api.request_with_handling", return_value=mock_response
    )

    result = api.fetch_user()

    assert result == "test-user"


def test_create_repository_user(mocker):
    mocker.patch(
        "github_rest_cli.api.get_headers", return_value={"Authorization": "token fake"}
    )

    mocker.patch("github_rest_cli.api.fetch_user", return_value="test-user")

    expected_message = "Repository successfully created in test-user/test-repo."

    mocker.patch(
        "github_rest_cli.api.request_with_handling", return_value=expected_message
    )

    result = api.create_repository("test-repo", "public")

    assert result == expected_message


def test_create_repository_org(mocker):
    mocker.patch(
        "github_rest_cli.api.get_headers", return_value={"Authorization": "token fake"}
    )

    expected_message = "Repository successfully created in test-org/test-repo."

    mocker.patch(
        "github_rest_cli.api.request_with_handling", return_value=expected_message
    )

    result = api.create_repository("test-repo", "public", "test-org")

    assert result == expected_message
