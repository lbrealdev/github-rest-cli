from github_rest_cli import api


GET_HEADERS_FUNCTION = "github_rest_cli.api.get_headers"
FETCH_USER_FUNCTION = "github_rest_cli.api.fetch_user"
REQUEST_HANDLER_FUNCTION = "github_rest_cli.api.request_with_handling"


def test_delete_repository(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(FETCH_USER_FUNCTION, return_value="test-user")
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.delete_repository("my-repo")

    request_mock.assert_called_once()
    assert request_mock.call_args.args[0] == "DELETE"
    assert "test-user/my-repo" in request_mock.call_args.args[1]


def test_delete_repository_org(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.delete_repository("my-repo", org="my-org")

    assert "my-org/my-repo" in request_mock.call_args.args[1]


def test_dependabot_security_enable(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(FETCH_USER_FUNCTION, return_value="test-user")
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.dependabot_security("my-repo", True)

    assert request_mock.call_count == 2
    assert all(call.args[0] == "PUT" for call in request_mock.call_args_list)


def test_dependabot_security_disable(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(FETCH_USER_FUNCTION, return_value="test-user")
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.dependabot_security("my-repo", False)

    assert request_mock.call_count == 1
    assert request_mock.call_args.args[0] == "DELETE"


def test_deployment_environment(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    mocker.patch(FETCH_USER_FUNCTION, return_value="test-user")
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.deployment_environment("my-repo", "production")

    request_mock.assert_called_once()
    assert request_mock.call_args.args[0] == "PUT"
    assert request_mock.call_args.args[1].endswith(
        "/repos/test-user/my-repo/environments/production"
    )


def test_deployment_environment_org(mocker):
    mocker.patch(GET_HEADERS_FUNCTION, return_value={"Authorization": "token fake"})
    request_mock = mocker.patch(REQUEST_HANDLER_FUNCTION, return_value=None)

    api.deployment_environment("my-repo", "staging", org="my-org")

    assert request_mock.call_args.args[1].endswith(
        "/repos/my-org/my-repo/environments/staging"
    )
