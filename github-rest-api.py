import requests
import argparse
from config import settings
from rich.console import Console


console = Console()


def check_repository(name):
    headers = {
       "Authorization": f"token {settings.AUTH_TOKEN}",
       "Accept": "application/vnd.github.v3+json"
    }
    resp = requests.get(
        f'{settings.API_URL}/repos/{settings.USER}/{name}',
        headers=headers
    )
    if resp.status_code == 200:
        console.print("The repository already exists!", style='blink bold green')
        return True
    else:
        return False

def create_repository(name):
    headers = {
        "Authorization": f"token {settings.AUTH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": name,
        "auto_init": "true",
        "private": "true",
    }
    resp = requests.post(
        f'{settings.API_URL}/user/repos',
        headers=headers,
        json=data
    )
    if resp.status_code == 201:
        console.print("Repository created sucessfully!", style="blink bold green")
    else:
        console.print(
            f"Failed to create repository {name} with status code {resp.status_code}",
            style='blink bold red')
        return False

def delete_repository(name):
    headers = {
       "Authorization": f"token {settings.AUTH_TOKEN}",
       "Accept": "application/vnd.github.v3+json"
    }
    resp = requests.delete(
        f'{settings.API_URL}/repos/{settings.USER}/{name}',
        headers=headers
    )
    if resp.status_code == 204:
        console.print("Repository deleted!", style='blink bold green')
    elif resp.status_code == 404:
        console.print("Repository not found!", style='blink bold red')
    else:
        console.print(
            f"Failed to delete repository {name} with status code {resp.status_code}",
            style='blink bold red')
        return False

def main():
    # top-level parser
    parser = argparse.ArgumentParser(
                prog='Python Github REST API',
                description='Python CLI to Github REST API',
                )
    subparsers = parser.add_subparsers(
                                    help="Python Github REST API commands",
                                    dest='command')
    
    # create-repository function parser
    parser_create_repository = subparsers.add_parser(
                                    'create-repository',
                                    help='Create new repository')
    parser_create_repository.add_argument(
                                    '-n', 
                                    '--name',
                                    help='Name for new repository',
                                    required=True,
                                    dest='name')
    
    # delete-repository function parser
    parser_delete_repository = subparsers.add_parser(
                                    'delete-repository',
                                    help='Delete repository')
    parser_delete_repository.add_argument(
                                    '-n',
                                    '--name',
                                    help='Repository name to delete',
                                    required=True,
                                    dest='name')
    
    args = parser.parse_args()

    if args.command == "create-repository":
        verify = check_repository(args.name)
        if verify is False:
            create_repository(args.name)
        else:
            pass
    elif args.command == "delete-repository":
        delete_repository(args.name)
    else:
        return False

if __name__ == '__main__':
    main()
