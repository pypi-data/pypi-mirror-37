import getpass
import json
import os
import sys

CONFIGURATION_MESSAGE = """
To start using zespa, run:

zespa configure
""".strip()
ZESPA_CONFIG_DIR = os.path.join(os.environ['HOME'], '.zespa')
CONFIG_PATH = os.path.join(os.environ['HOME'], '.zespa', 'config.json')


class ZespaConfiguration():
    def __init__(self):
        if not os.path.exists(ZESPA_CONFIG_DIR):
            os.mkdir(ZESPA_CONFIG_DIR)

    def _is_configured(self):
        return os.path.exists(CONFIG_PATH)

    def _set_config(self, config_dict):
        f = open(CONFIG_PATH, 'w')
        f.write(json.dumps(config_dict))
        f.close()

    def _get_config(self):
        if not os.path.exists(CONFIG_PATH):
            return {}
        f = open(CONFIG_PATH, 'r')
        json_str = f.read()
        f.close()
        return json.loads(json_str)

    def get_github_token(self):
        config = self._get_config()
        if 'github_token' not in config:
            return ''
        return config['github_token']

    def get_repo_name(self):
        config = self._get_config()
        if 'repo_name' not in config:
            return ''
        return config['repo_name']

    def get_zenhub_token(self):
        config = self._get_config()
        if 'zenhub_token' not in config:
            return ''
        return config['zenhub_token']

    def check(self):
        if self._is_configured():
            return True
        print(CONFIGURATION_MESSAGE)
        sys.exit(1)

    def create(self):
        github_token = getpass.getpass(prompt='GitHub Token:')
        zenhub_token = getpass.getpass(prompt='ZenHub Token:')

        repo_name = input('Repository Name (e.g.: octokit/go-octokit):')

        config_dict = {
            'github_token': github_token,
            'zenhub_token': zenhub_token,
            'repo_name': repo_name,
        }
        self._set_config(config_dict)
        print("Saved to '{}'".format(CONFIG_PATH))
