import json
import socket

from docopt import docopt as docoptinit

register_kong_doc = """
Usage:
    register_ws [options]
    
Options:
    --ot             1Token Endpoint (it will only register into  config:v1ws also)
    --v2             Register to v2
    --name=<name>
    --uri=<uri>
    --ip=<ip>
    --port=<port>
    --test           For testing only
"""


def register_ws(argv):
    docopt = docoptinit(register_kong_doc, argv)
    print(docopt)
    dst_list = []
    if docopt['--v2']:
        dst_list.append('wsv2')
    if docopt['--ot']:
        dst_list.append('v1ws')
    for dst in dst_list:
        print('check', dst)
        from . import util
        # r = util.must_success(requests.get, f'http://api.qbtrade.org/redis/get?key=config:{dst}&raw=1')
        r = util.Redis.get(f'config:{dst}')
        r = json.loads(r)
        print('get', r)
        port = docopt['--port']
        if not docopt['--ip']:
            ip = socket.gethostbyname(socket.gethostname())
        else:
            ip = docopt['--ip']
        uri = docopt['--uri']
        r[docopt['--name']] = f'ws://{ip}:{port}/{uri}'
        print('new record', r)

        data = json.dumps(r)
        if docopt['--test']:
            key = f'test:config:{dst}'
        else:
            key = f'config:{dst}'
        print('going to set', key, data)
        r = util.Redis.set(key, data)
        assert r


if __name__ == '__main__':
    # register_kong(['--name', 'pytest', '--ip', '1.2.3.4', '--uris', '/pytest', '--port', '8080'])
    register_ws(['--name', '/pytest', '--uri', '/ws-random', '--port', '3000', '--ot'])
