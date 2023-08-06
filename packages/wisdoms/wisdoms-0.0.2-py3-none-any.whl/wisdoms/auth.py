from nameko.standalone.rpc import ClusterRpcProxy
from functools import wraps

# 微服务 rabbitMQ url
MS_HOST = {'AMQP_URI': "amqp://guest:guest@localhost"}


def auth(f):
    @wraps(f)
    def inner(*args, **kwargs):
        srv_name = args[0].name
        uid = args[1]['uid']
        f_name = f.__name__
        with ClusterRpcProxy(MS_HOST) as rpc:
            res = rpc.db_service.isrole_app(srv_name, uid, f_name)
        if res['err_num'] == 0:
            return f(*args, **kwargs)
        return res

    return inner
