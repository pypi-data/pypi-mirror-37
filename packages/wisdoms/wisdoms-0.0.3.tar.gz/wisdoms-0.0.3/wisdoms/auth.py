"""
    :usage:
        from wisdoms.auth import permit

        host = 'xxxx'

        auth = permit(host)

        class A:
            @auth
            def func():
                pass
"""

from nameko.standalone.rpc import ClusterRpcProxy
from functools import wraps


def permit(host):
    """ 调用微服务功能之前，进入基础微服务进行权限验证

    :param: host: micro service host
    """

    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            srv_name = args[0].name
            uid = args[1]['uid']
            f_name = f.__name__
            with ClusterRpcProxy(host) as rpc:
                res = rpc.db_service.isrole_app(srv_name, uid, f_name)
            if res['err_num'] == 0:
                return f(*args, **kwargs)
            return res

        return inner

    return wrapper
