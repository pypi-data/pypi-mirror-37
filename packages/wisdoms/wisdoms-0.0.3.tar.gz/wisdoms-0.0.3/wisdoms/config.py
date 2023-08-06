# Created by Q-ays.
# whosqays@gmail.com


"""
    :usage:
        from wisdoms.config import c
        c.get('name')
"""

import yaml


class Config:
    """
    读取yml配置文件
    """

    def __init__(self):

        with open('../../.env', 'r', encoding='utf-8') as f:
            env = f.read().strip()

        if env:
            with open('../config/' + env + '.yml') as f:
                self.configuration = yaml.load(f)

    def get(self, key):
        if self.configuration:
            return self.configuration[key]
        else:
            return {'err_code': 'maybe environment variable is missed'}


c = Config()
