doc = """
Usage:
    build-curdir [options]
    
Options:
    --repo=<repo>
    --no-cache
"""


def build_curdir(argv):
    import os
    from docopt import docopt as docoptinit
    import json
    import sys
    from .cdi import docker_retag_and_push_all, get_docker_client
    docopt = docoptinit(doc, argv)
    folder = os.path.abspath('.')

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
    if os.environ.get('QB_REGION') == 'alihk':
        docker_retag_and_push_all(tag, 'registry-vpc.cn-hongkong.aliyuncs.com/' + tag)
    else:
        docker_retag_and_push_all(tag, 'registry.cn-hongkong.aliyuncs.com/' + tag)

    docker_retag_and_push_all(tag, 'registry.cn-hangzhou.aliyuncs.com/' + tag)

    # db[folder] = parent_hash
