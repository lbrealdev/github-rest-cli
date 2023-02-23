import requests
import pprint
import os

GH_API_URL = "https://api.github.com"
GH_AUTH_TOKEN = os.environ.get('GH_API_TOKEN')

def github_get_user(username: str):
    resp = requests.get(f'{GH_API_URL}/users/{username}', headers={"Authorization": "token {}".format(GH_AUTH_TOKEN)})
    if resp.status_code == 200:
        pprint.pprint(resp.json())
    else:
        print("Failed!")

if __name__ == '__main__':
    github_get_user(username="lbrealdev")
