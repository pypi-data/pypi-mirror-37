import socket

import requests
from docopt import docopt as docoptinit

from . import util

register_kong_doc = """
Usage:
    register_kong [options]
    
Options:
    --name=<name>
    --uris=<uris>
    --hosts=<hosts>
    --port=<port>
    --ip=<ip>
    --region=<region>
    --preserve-host
    --timeout=<timeout>   [default: 3]
"""


def register_kong(argv):
    docopt = docoptinit(register_kong_doc, argv)
    print(docopt)
    name = docopt['--name']
    uris = docopt['--uris']
    port = docopt['--port']
    hosts = docopt['--hosts']
    timeout = float(docopt['--timeout'])
    region = docopt['--region']
    preserve = docopt['--preserve-host']
    if region == 'alihz':
        url = 'http://alihz-master-0.internal.qbtrade.org:8001/apis'
    elif region == 'alihk-stage':
        url = 'http://alihk-stage-0.qbtrade.org:8001/apis'
    elif region == 'alihk-0-14':
        url = 'http://alihk-master.qbtrade.org:9001/apis'
    else:
        url = 'http://kong-admin.qbtrade.org/apis'
    if not docopt['--ip']:
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = docopt['--ip']
    r = requests.delete('{url}/{name}'.format(url=url, name=name), timeout=timeout)
    print('delete', r.text)
    seconds = 1000
    data = {'name': name,
            'upstream_url': 'http://{}:{}'.format(ip, port),
            'upstream_connect_timeout': seconds,
            'upstream_read_timeout': 30 * seconds,
            'upstream_send_timeout': 30 * seconds,
            }

    if hosts:
        data['hosts'] = hosts
    if uris:
        data['uris'] = uris
        data['strip_uri'] = 'true'
    if preserve:
        data['preserve_host'] = 'true'

    print('post', url, data)
    r = util.must_success(requests.post, url, data=data)
    print('add', r.text, ip)


if __name__ == '__main__':
    # register_kong(['--name', 'pytest', '--ip', '1.2.3.4', '--uris', '/pytest', '--port', '8080'])
    register_kong(['--name', 'pytest', '--ip', '1.2.3.4', '--hosts', 'pytest.qbtrade.org', '--port', '8080'])
