#!/usr/bin/env python3

"""
This file needs to be independent, use only basic library

NO SUPPORT for python2

Let Python3.4 can use it


This is entry point for small tools manage the project

Usage:
    qb.py [options] create_docker_image
    qb.py [options] cdi
    qb.py [options] build_curdir [--repo=<repo>]

Options:
    --run                  Run
    --filter=<filter>      Give a filter for parent folder
    --no-cache             Disable cache on docker build
    --always-rebuild       Force re-build the image
    -v                     Verbose Mode, will set_logger(..., debug=True)
    --root=<root>          Root directory [default: .]


create_docker_image:
    for a Dockerfile such as telegraf/0.12-machine/Dockerfile
    it will build an image with tag
    qbtrade/telegraf:0.12-machine
    or with tag
    telegraf:0.12-machine, and put it in private repo

    if config.yaml has
        public: false
    in repo, then push it only to private(aliyun) repo

rsync <folder>:
"""

import hashlib
import json
import logging
import os
import sys
from functools import lru_cache

import arrow
import yaml
from docopt import docopt as docoptinit


@lru_cache()
def get_docker_client():
    print('docker client created')
    import docker
    client = docker.APIClient(version='1.23')
    print(client.version())
    print(client.base_url)
    return client


def get_hash_of_dirs(directory, verbose=0):
    sha1 = hashlib.sha1()
    if not os.path.exists(directory):
        return -1

    try:
        for root, dirs, files in os.walk(directory):
            for names in files:
                if verbose == 1:
                    print('Hashing', names)
                filepath = os.path.join(root, names)
                try:
                    f1 = open(filepath, 'rb')
                    while 1:
                        # Read file in as little chunks
                        buf = f1.read(4096)
                        if not buf:
                            break
                        t = hashlib.sha1(buf).hexdigest()
                        sha1.update(t.encode('utf8'))
                except:
                    continue
                finally:
                    f1.close()
    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2
    return sha1.hexdigest()


def docker_push(tag):
    for line in get_docker_client().push(tag, stream=True):
        line = line.decode('utf8')
        try:
            # print(line, end='')
            js = json.loads(line)
            print(' '.join('{}={}'.format(k, v) for k, v in js.items()))
        except:
            print(line, end='')


def docker_retag(taga, tagb):
    """
    only support
    :param taga: qbtrade/python
    :param tagb: registry.cn-hangzhou.aliyuncs.com/qbtrade/python
    :return:
    """
    if taga == tagb:
        return
    sp = tagb.find(':')
    repo, tag = tagb[:sp], tagb[sp + 1:]
    print('repo', repo, 'tag', tag)
    get_docker_client().tag(taga, repository=repo, tag=tag)


def docker_retag_and_push(taga, tagb):
    docker_retag(taga, tagb)
    docker_push(tagb)


def load_cdi_config(folder):
    # x = os.path.isfile(os.path.join(folder, '.private'))
    if not os.path.isfile(os.path.join(folder, 'config.yaml')):
        return {}
    t = yaml.load(open(os.path.join(folder, 'config.yaml')))
    return t


def docker_retag_and_push_all(tag, param):
    print('push all', tag, param)
    date_str = arrow.now().strftime('%Y%m%d')
    datetime_str = arrow.now().strftime('%Y%m%d-%H%M%S')
    docker_retag_and_push(tag, param)
    docker_retag_and_push(tag, param + '-' + date_str)
    docker_retag_and_push(tag, param + '-' + datetime_str)


def pull_newest_image_before_build(path):
    for line in open(path).read().splitlines():
        if line.strip().startswith('FROM'):
            image = line.split(' ')[1]
            cmd = 'docker pull {}'.format(image)
            print(cmd)
            os.system(cmd)
            break


def handle_folder(folder):
    """
    a folder contains Dockerfile
    build it and upload
    :param folder:
    :return:
    """
    print('handle', folder)
    sp = os.path.split(folder)
    if sp[0] == '.':
        image = sp[1]
        version = 'latest'
    else:
        image = os.path.split(sp[0])[1]
        version = sp[1]

    tag = 'qbtrade/{}:{}'.format(image, version)

    if docopt['--run']:
        parent_hash = get_hash_of_dirs(folder)
        if not docopt['--always-rebuild']:
            if folder in db and db[folder] == parent_hash:
                print('{} hash check sum'.format(folder))
                return
        success = False
        print('------build------', folder)
        pull_newest_image_before_build(os.path.join(folder, 'Dockerfile'))
        for line in get_docker_client().build(path=folder,
                                              dockerfile='Dockerfile',
                                              nocache=docopt['--no-cache'],
                                              tag=tag,
                                              rm=True):
            line = line.decode('utf8')
            try:
                print(json.loads(line)['stream'], end='')
            except:
                print(line, end='')
            if 'Successfully built' in line:
                success = True
        if not success:
            sys.exit(1)
        print('------push------')
        # today_str = arrow.now().strftime('%Y%m%d')
        cfg = load_cdi_config(folder)
        if cfg.get('public', True):
            docker_retag_and_push_all(tag, tag)
        else:
            print('only push to private repo')
        docker_retag_and_push_all(tag, 'registry.cn-hangzhou.aliyuncs.com/' + tag)
        if os.environ['QB_REGION'] == 'alihk':
            docker_retag_and_push_all(tag, 'registry-vpc.cn-hongkong.aliyuncs.com/' + tag)
        else:
            docker_retag_and_push_all(tag, 'registry.cn-hongkong.aliyuncs.com/' + tag)

        db[folder] = parent_hash
    else:
        print('add --run to run')


def build_curdir():
    folder = os.path.abspath(os.path.expanduser(docopt['--root']))
    print('build folder', folder)
    # parent_hash = get_hash_of_dirs(folder)
    # if not docopt['--always-rebuild']:
    #     if folder in db and db[folder] == parent_hash:
    #         print('{} hash check sum'.format(folder))
    #         return
    success = False
    if docopt['--repo']:
        repo = docopt['--repo']
    else:
        repo = os.path.basename(folder)
    tag = 'qbtrade/{}:latest'.format(repo)
    print('------build------', folder, tag)
    for line in get_docker_client().build(path=folder,
                                          dockerfile='Dockerfile',
                                          nocache=docopt['--no-cache'],
                                          tag=tag,
                                          rm=True):
        try:
            line = line.decode('utf8')
            print(json.loads(line)['stream'], end='')
        except:
            print(line, end='')
        if 'Successfully built' in line:
            success = True
    if not success:
        sys.exit(1)
    print('------push------')
    # cfg = load_cdi_config(folder)
    # if cfg.get('public', True):
    #     docker_push(tag)
    #     docker_retag_and_push(tag, tag + '-' + date_str)
    # else:
    #     print('only push to private repo')
    docker_retag_and_push_all(tag, 'registry.cn-hangzhou.aliyuncs.com/' + tag)

    # db[folder] = parent_hash


def create_docker_image():
    """
    This should display failed information if some docker build fails
    :return:
    """
    print('create_docker_image')
    fail = []

    folder = os.path.abspath(os.path.expanduser(docopt['--root']))
    print('build folder', folder)
    for parent, y, files in os.walk(folder):
        if docopt['--filter'] and parent.find(docopt['--filter']) < 0:
            continue
        if 'Dockerfile' in files:
            handle_folder(parent)
    for x in fail:
        print('fail {}'.format(x))


# def show_config():
#     qb.config.log_config()


# def rsync():
#     import getpass
#     cmd = 'rsync -a --delete --exclude=".git/ " {}  alihk9.qbtrade.org:/home/{}/dev'.format(docopt['<folder>'],
#                                                                                             getpass.getuser())
#     print('exec', cmd)
#     os.system(cmd)


# def init_config():
#     # f = os.path.expanduser('~/.qb.jinja2.yaml')
#     # x = open(f).read()
#     # t = jinja2.Template(x)
#     # s = t.render({'QB_REGION': os.getenv('QB_REGION', 'urwork'), 'QB_ENV': os.getenv('QB_ENV', 'debug')})
#     #
#     # open(os.path.expanduser('~/.qbconf'), 'w').write(s)
#     folder = os.path.expanduser('~/.qb')
#     os.makedirs(folder, exist_ok=True)
#
#     open(os.path.join(folder, 'auth_config.yml'), 'w').write("user: tyz\nsecret_path: /qb_rsa\n")


def main():
    # qb.init('qb.py', debug=False, log_config=False)
    logging.basicConfig(level=logging.DEBUG)
    if docopt['cdi'] or docopt['create_docker_image']:
        create_docker_image()
    elif docopt['build_curdir']:
        build_curdir()
    # if docopt['rsync']:
    #     rsync()
    # if docopt['initconfig']:
    #     init_config()
    #     # if docopt['config']:
    #     #     show_config()


if __name__ == '__main__':
    dotfolder = os.path.expanduser('~/.qbtrade/')
    os.makedirs(dotfolder, exist_ok=True)
    from unqlite import UnQLite

    db = UnQLite(os.path.join(dotfolder, 'qbtrade.db'))

    docopt = docoptinit(__doc__)
    print('docopt', docopt)
    main()
