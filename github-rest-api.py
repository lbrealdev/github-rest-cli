import requests
import pprint
import os
import argparse

GH_API_URL = "https://api.github.com"
GH_AUTH_TOKEN = os.environ.get('GH_API_TOKEN')

def github_user_data(user: str):
    resp = requests.get(
            f'{GH_API_URL}/users/{user}',
            headers={"Authorization": f'token {GH_AUTH_TOKEN}'}
            )
    if resp.status_code == 200:
        pprint.pprint(resp.json())
    else:
        print("Failed!")

def main():
    parser = argparse.ArgumentParser(
                'Github REST API',
                description='Python CLI to Github REST API',
                )
    parser.add_argument('-u', '--user',
                        help='Github user',
                        required=True,
                        dest='user')
    
    args = parser.parse_args()
    github_user_data(args.user)

if __name__ == '__main__':
    main()
