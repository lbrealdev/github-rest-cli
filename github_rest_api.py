import re
import requests
import pprint
import os

GH_API_URL = "https://api.github.com/repos/lbrealdev/azure"
GH_AUTH_TOKEN = os.environ.get('GH_API_TOKEN')

def gh_get_repository():
    resp = requests.get(GH_API_URL, headers={"Authorization": "token {}".format(GH_AUTH_TOKEN)})
    if resp.status_code == requests.codes.okay:
        pprint.pprint(resp.json())
    else:
        print("Failed!")

if __name__ == '__main__':
    gh_get_repository()
