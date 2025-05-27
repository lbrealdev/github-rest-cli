import requests
import json
from github_rest_cli.globals import GITHUB_URL, HEADERS
from github_rest_cli.utils import rich_output, rprint


def request_with_handling(
    method, url, success_msg: str = None, error_msg: str = None, **kwargs
):
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        if success_msg:
            rich_output(success_msg)
        else:
          return response
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if error_msg and status in error_msg:
            rich_output(error_msg[status], format_str="bold red")
        else:
            rich_output(f"Request failed: status code {status}", format_str="bold red")
        return None
    except requests.exceptions.RequestException as e:
        rich_output(f"Request error: {e}", format_str="bold red")
        return None


def build_url(*segments: str) -> str:
    """
    Build an GitHub REST API endpoint

    Example:
      build_url("repos", "org", "repo", "environments", "prod")

    Result:
      https://api.github.com/repos/org/repo/environments/prod
    """
    base = GITHUB_URL.rstrip("/")
    path = "/".join(segment.strip("/") for segment in segments)
    return f"{base}/{path}"


def fetch_user():
    url = build_url("user")
    response = request_with_handling("GET", url, headers=HEADERS)
    if response:
        data = response.json()
        return data.get("login")
    return None


def get_repository(owner: str, name: str, org: str = None):
    url = build_url("repos", org or owner, name)
    response = request_with_handling("GET", url, headers=HEADERS)
    if response:
        data = response.json()
        rprint(data)


def create_repository(owner: str, name: str, visibility: str, org: str = None):
    data = {
        "name": name,
        "auto_init": "true",
        "visibility": visibility,
    }

    if visibility == "private":
        data["private"] = True

    url = build_url("orgs", org, "repos") if org else build_url("user", "repos")

    return request_with_handling(
        "POST",
        url,
        headers=HEADERS,
        json=data,
        success_msg=f"Repository successfully created in {owner or org }/{name}",
        error_msg={
            401: "Unauthorized access. Please check your token or credentials.",
            422: "Repository name already exists on this account or organization.",
        },
    )


def delete_repository(owner: str, name: str, org: str = None):
    url = build_url("repos", org, name) if org else build_url("repos", owner, name)

    return request_with_handling(
        "DELETE",
        url,
        headers=HEADERS,
        success_msg=f"Repository sucessfully deleted in {owner or org}/{name}",
        error_msg={
            403: "The authenticated user does not have sufficient permissions to delete this repository.",
            404: "The requested repository was not found.",
        },
    )


def list_repositories(page: int, property: str, role: str):
    url = build_url("user", "repos")

    params = {
      "per_page": page,
      "sort": property,
      "type": role
    }

    response = request_with_handling(
      "GET",
      url,
      params=params,
      headers=HEADERS,
      error_msg={
          401: "Unauthorized access. Please check your token or credentials."
      },
    )

    if response:
        data = response.json()
        repo_full_name = [repo['full_name'] for repo in data]
        for repos in repo_full_name:
            rich_output(f"- {repos}")
        rich_output(f"\nTotal repositories: {len(repo_full_name)}")


def dependabot_security(owner: str, name: str, org: str, enabled: bool):
    is_enabled = bool(enabled)

    try:
        url = (
            f"{GITHUB_URL}/repos/{org}/{name}"
            if org
            else f"{GITHUB_URL}/repos/{owner}/{name}"
        )
        if is_enabled:
            for endpoint in ["vulnerability-alerts", "automated-security-fixes"]:
                req = requests.put(f"{url}/{endpoint}", headers=HEADERS)
                req.raise_for_status()
            rich_output(
                f"Dependabot has been activated on repository {org or owner}/{name}",
                format_str="bold green",
            )
        else:
            req = requests.delete(f"{url}/vulnerability-alerts", headers=HEADERS)
            req.raise_for_status()
            rich_output(
                f"Dependabot has been disabled on repository {org or owner}/{name}",
                format_str="bold green",
            )
    except requests.exceptions.RequestException as e:
        rprint(f"Error: {e}")


def deployment_environment(owner: str, name: str, env: str, org: str = None):
    try:
        url = (
            f"{GITHUB_URL}/repos/{org}/{name}/environments/{env}"
            if org
            else f"{GITHUB_URL}/repos/{owner}/{name}/environments/{env}"
        )
        req = requests.put(url, headers=HEADERS)
        req.raise_for_status()
        rich_output(
            f"Environment '{env.upper()}' created.\n"
            + f"Repository: {owner or org}/{name}",
            format_str="bold green",
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            rich_output(
                f"Failed to create environment {env.upper()}",
                format_str="bold red",
            )
        else:
            rprint(f"Error: {e}")
