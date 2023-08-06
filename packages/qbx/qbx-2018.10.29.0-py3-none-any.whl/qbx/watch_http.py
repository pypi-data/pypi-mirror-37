import arrow
import requests
from docopt import docopt as docoptinit

watch_http_doc = """
Usage:
    watch_http <url> [options]

Options:
    --timeout=<t>   Timeout [default: 30]
"""


def check(url):
    if not url.startswith('http://'):
        url = 'http://' + url
    try:
        r = requests.get(url, timeout=1)
        if r.status_code == 200:
            return True
        return False
    except:
        return False


def watch_http(argv):
    print(watch_http_doc)
    print(argv)
    docopt = docoptinit(watch_http_doc, argv)
    print(docopt)
    url = docopt['<url>']
    timeout = int(docopt['--timeout'])
    start = arrow.now()
    while arrow.now() < start.shift(seconds=timeout):
        if check(url):
            return True
        print('check', url, 'fail')
        import time
        time.sleep(1)
    import sys
    print('fail watch http')
    sys.exit(1)


def play():
    watch_http(['www.baidu.com', '--timeout', '10'])
    watch_http(['qadfaf.afafasfsadfasdfasf.com', '--timeout', '10'])
    # watch_http(['www.baidu.com'])


if __name__ == '__main__':
    play()
