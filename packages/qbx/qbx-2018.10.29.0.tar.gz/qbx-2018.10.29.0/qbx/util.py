import sys

from docopt import docopt as docoptinit


def must_success(func, *args, **kwargs):
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 5
    try:
        r = func(*args, **kwargs)
    except Exception as e:
        print('force exit, statuscode != 200', type(e))
        sys.exit(1)
    if r.status_code >= 300:
        print(r, r.text)
        print('force exit, statuscode != 200')
        sys.exit(1)
    return r


def docopt(doc, argv):
    return docoptinit(doc, argv=argv)


class Redis:
    inst = None

    @classmethod
    def __get_instance(cls):
        import redis
        if cls.inst is None:
            cls.inst = redis.StrictRedis(host='redis.svc.qbtrade.org', socket_connect_timeout=5, socket_timeout=5,
                                         decode_responses=True)
        return cls.inst

    @classmethod
    def get(cls, key):
        return cls.__get_instance().get(key)

    @classmethod
    def set(cls, key, value):
        return cls.__get_instance().set(key, value)


if __name__ == '__main__':
    r = Redis.get('config:v1ws')
    print(r)
    r = Redis.set('test:config:v1ws', 'hello-world')
    print(r)
