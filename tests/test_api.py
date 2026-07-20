from github_rest_cli import api


GET_HEADERS_FUNCTION = "github_rest_cli.api.get_headers"
FETCH_USER_FUNCTION = "github_rest_cli.api.fetch_user"
REQUEST_HANDLER_FUNCTION = "github_rest_cli.api.request_with_handling"


def test_fetch_user(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"login": "test-user"}
    mock_response.raise_for_status = lambda: None

    mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=mock_response)

    result = api.fetch_user()

    assert result == "test-user"


def test_create_repository_user(mocker):
    expected_message = "Repository successfully created in test-user/test-repo."

    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(FETCH_USER_FUNCTION, return_value="test-user")
    mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=expected_message)

    result = api.create_repository("test-repo", "public")

    assert result == expected_message


def test_create_repository_org(mocker):
    expected_message = "Repository successfully created in test-org/test-repo."

    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=expected_message)

    result = api.create_repository("test-repo", "public", "test-org")

    assert result == expected_message


SAMPLE_REPO = {
    "name": "test-repo",
    "owner": {"login": "test-user"},
    "html_url": "https://github.com/test-user/test-repo",
    "visibility": "public",
}


def _mock_repo_response(mocker, payload):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(FETCH_USER_FUNCTION, return_value="test-user")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = payload
    mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=mock_response)


def test_get_repository_json_format(mocker):
    _mock_repo_response(mocker, SAMPLE_REPO)

    result = api.get_repository("test-repo", output_format="json")

    assert isinstance(result, str)
    assert '"name": "test-repo"' in result
    assert '"visibility": "public"' in result


def test_get_repository_table_format(mocker):
    _mock_repo_response(mocker, SAMPLE_REPO)

    result = api.get_repository("test-repo", output_format="table")

    table_text = str(result)
    assert "test-repo" in table_text
    assert "test-user" in table_text
    assert not table_text.strip().startswith("{")


def test_list_repositories_json_format(mocker):
    _mock_repo_response(mocker, [SAMPLE_REPO])

    result = api.list_repositories(20, "pushed", None, "json")

    assert isinstance(result, str)
    assert '"repositories"' in result
    assert '"name": "test-repo"' in result


def test_list_repositories_table_format(mocker):
    _mock_repo_response(mocker, [SAMPLE_REPO])

    result = api.list_repositories(20, "pushed", None, "table")

    table_text = str(result)
    assert "test-repo" in table_text
    assert "GITHUB REPOSITORIES" in table_text.upper()
