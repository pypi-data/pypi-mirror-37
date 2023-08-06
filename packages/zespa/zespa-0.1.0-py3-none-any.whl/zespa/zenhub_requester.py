import json

import requests

ZENHUB_API = 'https://api.zenhub.io'


class ZenHubRequester():
    def __init__(self, repo_id, token):
        self.repo_id = repo_id
        self.token = token

    def get_estimate(self, issue_id):
        resp = requests.get(f'{ZENHUB_API}/p1/repositories/{self.repo_id}/issues/{issue_id}?access_token={self.token}')
        issue_info = json.loads(resp.content.decode('utf-8'))
        estimate = issue_info.get('estimate', {}).get('value', 0)
        return estimate
