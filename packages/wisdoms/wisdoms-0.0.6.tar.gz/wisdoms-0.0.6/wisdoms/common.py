# Created by Q-ays.
# whosqays@gmail.com

import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

err_num = {
    "OK": 0,
    "DATAERR": 1,
    "DSANF": 2,
    "PARM": 3,
    "PARGERR": 4,
    "NOadmin": 5,
    "NOAUTH": 6
}

err_msg = {
    "OK": "OK",
    "DATAERR": "数据库错误",
    "DSANF": "第三方服务错误",
    "PARM": "参数错误",
    "PARGERR": "数据错误",
    "NOadmin": "被管理者",
    "NOAUTH": "没有权限"
}

"""
    状态码
    
    Notice::
        大于0，顺利执行
        小于0，执行出错        
    
"""
state_code = {

    -1: 'GET_WAY_ERROR',
    -2: 'MS_ERROR',
    -3: 'DATABASE_ERROR',
    -4: 'NOT_AUTHORIZED',
    -5: 'DATA_FORMAT_ERROR',
    -6: 'CONNECTION_TIMEOUT',
    -7: 'UNKNOWN_ERROR',
    -8: 'THIRD_PARTY_ERROR',
    -9: 'PARAM_ERROR',

    1: 'SUCCESS'
}

state_desc = {
    'GET_WAY_ERROR': 'api 网关错误',
    'MS_ERROR': '微服务错误',
    'DATABASE_ERROR': '数据库错误',
    'NOT_AUTHORIZED': '未授权，拒绝访问',
    'DATA_FORMAT_ERROR': '数据格式错误',
    'CONNECTION_TIMEOUT': '连接超时',
    'UNKNOWN_ERROR': '未知错误',
    'THIRD_PARTY_ERROR': '第三方服务错误',
    'PARAM_ERROR': '参数错误',

    'SUCCESS': '成功'

}


def revert(code, data=None, desc=None):
    """
    公共返回方法

    :param code: 状态码
    :param data: 返回数据
    :param desc: 描述
    :return:
    """

    try:
        msg = state_code[code]

        if not desc:
            desc = state_desc[msg]
    except KeyError as e:
        return revert(-9, e)

    if data:
        return {'code': code, 'msg': msg, 'desc': desc, 'data': data}
    else:
        return {'code': code, 'msg': msg, 'desc': desc}
