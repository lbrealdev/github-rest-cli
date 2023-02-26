import requests
import argparse
from config import settings


def github_check_repository(name):
    headers = {
       "Authorization": f"token {settings.AUTH_TOKEN}",
       "Accept": "application/vnd.github.v3+json"
    }
    resp = requests.get(
        f'{settings.API_URL}/repos/{settings.USER}/{name}', headers=headers
    )
    if resp.status_code == 200:
        print("The repository already exists!")
    return None

def github_create_repository(name):
    headers = {
        "Authorization": f"token {settings.AUTH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": f"{name}",
        "auto_init": True,
        "private": True,
    }
    resp = requests.post(
                        f'{settings.API_URL}/user/repos',
                        headers=headers,
                        json=payload
                        )
    if resp.status_code == 201:
        print("Repository created sucessfully!")
    else:
        print(f"Failed to create repository {name} with status code {resp.status_code}")

def main():
    parser = argparse.ArgumentParser(
                'Python Github REST API',
                description='Python CLI to Github REST API',
                )
    subparsers = parser.add_subparsers(help="Python Github REST API subcommands")
    parser_repository = subparsers.add_parser('new-repository',
                                              help='Create new repository')
    parser_repository.add_argument('-n', '--name',
                                   help='The repository name',
                                   required=True,
                                   dest='name')
    
    args = parser.parse_args()
    github_check_repository(args.name)

if __name__ == '__main__':
    main()
