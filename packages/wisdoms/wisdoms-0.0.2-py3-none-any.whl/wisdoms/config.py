# Created by Q-ays.
# whosqays@gmail.com


import yaml


class Config:
    def __init__(self):

        with open('../../.env', 'r', encoding='utf-8') as f:
            env = f.read().strip()
            print(env)

        if env:
            with open('../config/' + env + '.yml') as f:
                self.configuration = yaml.load(f)
                print(self.configuration)

    def get(self, key):
        if self.configuration:
            return self.configuration[key]
        else:
            return {'err_code': 'maybe environment variable is missed'}


c = Config()
