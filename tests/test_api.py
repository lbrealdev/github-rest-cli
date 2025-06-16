import pytest
from github_rest_cli import api


def test_fetch_user(mocker):
  mocker.patch("github_rest_cli.api.get_headers", return_value={"Authorization": "token fake"})

  mock_response = mocker.Mock()
  mock_response.status_code = 200
  mock_response.json.return_value = {"login": "test-user"}
  mock_response.raise_for_status = lambda: None

  mocker.patch("github_rest_cli.api.request_with_handling", return_value=mock_response)

  result = api.fetch_user()

  assert result == "test-user"
