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

        try:
            with open('../.env', 'r', encoding='utf-8') as f:
                env = f.read().strip()
        except Exception as e:
            print('file path is ../../.env')
            with open('../../.env', 'r', encoding='utf-8') as f:
                env = f.read().strip()

        if env:
            try:
                with open('./config/' + env + '.yml') as f:
                    self.configuration = yaml.load(f)
            except Exception as e:
                print('file path is ../config')
                with open('../config/' + env + '.yml') as f:
                    self.configuration = yaml.load(f)

    def get(self, key):
        if self.configuration:
            return self.configuration[key]
        else:
            return {'err_code': 'maybe environment variable is missed'}

    def to_dict(self):
        if self.configuration:
            return self.configuration


c = Config()
