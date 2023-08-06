import logging
import os
import sys

help_doc = """
usage: qbx [--help] 
           <command> [<args>]

These are some qbx commands:
    auth_wrapper
    register-kong
    register-ws
    watch_git
    watch_git_http
    build-curdir
    watch-http
    pull
    haproxy
    uproxy
    update-package
    add-version
"""


def print_help():
    print(help_doc)


def warning(message, seconds=10):
    import time
    logging.warning(message + f'sleep {seconds}s to let you change')
    for i in range(10, 0, -1):
        print(i, 'seconds left')
        time.sleep(1)


def run():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    print('argv---', sys.argv)
    if len(sys.argv) == 1:
        print_help()
    else:
        argv = sys.argv[2:]
        if sys.argv[1] == 'register-kong':
            from .register_kong import register_kong
            register_kong(argv)
        elif sys.argv[1] == 'register_kong':
            warning('register_kong is deprecated use "qbx register-kong" instead')
            from .register_kong import register_kong
            register_kong(argv)
        elif sys.argv[1] == 'register_ws':
            from .register_ws import register_ws
            warning('register_ws is deprecated use "qbx register-ws" instead')
            register_ws(argv)
        elif sys.argv[1] == 'register-ws':
            from .register_ws import register_ws
            register_ws(argv)
        elif sys.argv[1] == 'build-curdir':
            from .build_curdir import build_curdir
            build_curdir(argv)
        elif sys.argv[1] == 'watch_git':
            from .watchgit import watch_git
            watch_git(argv)
        elif sys.argv[1] == 'watch_git_http':
            from .watchgit import watch_git_http
            watch_git_http(argv)
        elif sys.argv[1] == 'haproxy':
            from .haproxy import haproxy
            haproxy(argv)
        elif sys.argv[1] == 'pull':
            from .pull import pull
            pull(argv)
        elif sys.argv[1] == 'uproxy':
            from .uproxy import uproxy
            uproxy(argv)
        elif sys.argv[1] == 'auth_wrapper':
            from .auth_wrapper import auth_wrapper
            auth_wrapper(argv)
        elif sys.argv[1] == 'kube-start':
            from . import kube_start
            kube_start.start()
        elif sys.argv[1] == 'upload':
            from .upload import upload
            upload(argv)
        elif sys.argv[1] == 'update-package':
            from .update_package import update_package
            update_package(argv)
        elif sys.argv[1] == 'add-version':
            from .add_version import add_version
            add_version(argv)
        elif sys.argv[1] == 'watch-http':
            from .watch_http import watch_http
            watch_http(argv)
        else:
            if sys.argv[1] != 'help' and sys.argv[1] != '--help':
                logging.warning('method not regognize')
            print_help()


def qbs():
    print(sys.argv)
    print(os.environ)
    run_cmdline_when_cond(sys.argv[1:])


def run_cmdline_when_cond(cmdline):
    print('cmdline: ', cmdline)
    import subprocess
    import time
    import arrow
    process = subprocess.Popen(cmdline)
    while True:
        if process.poll() is None:
            time.sleep(1)
        else:
            print('program exit itself')
            break
    print('end at', arrow.now(), 'sleep 30s before exit')
    time.sleep(30)


if __name__ == '__main__':
    # from .watchgit import watch_git
    # watch_git(['git+ssh://git@github.com/qbtrade/quantlib.git', 'log_rpc.py'])
    from . import kube_start

    kube_start.start()
