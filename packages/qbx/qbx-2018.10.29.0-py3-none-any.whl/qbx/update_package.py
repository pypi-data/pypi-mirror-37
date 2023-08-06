"""
Usage:
    udpate_package.py [<pkg>...]


"""
import redis
import socket


def check_dns():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    # r = sock.connect(('service.qbtrade.org', 6379))
    try:
        sock.connect(('service.qbtrade.org', 6379))
    except ConnectionError:
        print('fail connect to service.qbtrade.org:6379')
        return False
    sock.close()
    return True
    # sock.settimeout(None)
    # fileobj = sock.makefile('rb', 0)


def sleep_until_check_pass():
    sleep = 60
    import time
    while True:
        try:
            if check_dns():
                return
            print('check fail sleep {}'.format(sleep))
            sleep = min(300, sleep * 2)
            time.sleep(sleep)
        except:
            import logging
            logging.exception('unexpected failed')
            import time
            time.sleep(300)
            print('sleep 300s and panic')
            import os
            # noinspection PyProtectedMember
            os._exit(1)


def check_package(pkg='qbtrade'):
    r = redis.StrictRedis(host='service.qbtrade.org', socket_connect_timeout=1, socket_timeout=1, decode_responses=True)
    y = r.get(f'cache:pip:{pkg}.latest')
    import pkg_resources

    try:
        x = pkg_resources.get_distribution(pkg)
        version = x.version
    except:
        version = 'not-exist'
    if version != y:
        import os
        print(f'update version from {version} to {y}')
        os.system(f'pip install http://api.qbtrade.org/oss/public/{pkg}-latest-py3-none-any.whl -U --no-deps')


def update_package(argv):
    from docopt import docopt as docoptinit
    docopt = docoptinit(__doc__, argv)
    # print(docopt)
    # sleep_until_check_pass()
    pkg = docopt['<pkg>']
    if not pkg:
        pkg = ['qbtrade', 'otlib']
    print('update package', pkg)
    for p in pkg:
        check_package(p)
        # check_package('otlib')


if __name__ == '__main__':
    # docopt(__doc__)

    # docopt = docoptinit(['qbtrade', 'otlib'])
    update_package([])
    # update_package(['qbtrade', 'otlib'])
    # if docopt['--daemon']:
    #     pass
    # else:
    #     qb.run_until_complete(play())
