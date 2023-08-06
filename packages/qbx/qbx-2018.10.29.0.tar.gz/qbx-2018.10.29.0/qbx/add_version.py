doc = """
Usage:
    add-version [options]
    
Options:
    --gitsync
"""


def new_date_version():
    import arrow
    new_r = str(arrow.now().date()).replace('-', '.')
    new_r = new_r.split('.')
    return '.'.join(str(int(x)) for x in new_r)


def add_version(argv):
    import os
    import re

    from . import util
    docopt = util.docopt(doc, argv)
    package = os.getcwd()
    package = os.path.split(package)[-1]
    import os
    target = os.path.join(os.getcwd(), package, '__init__.py')
    print(f'add version {target}')
    txt = open(target).read()
    r = re.findall("__version__ = '(.*)'", txt)[0]
    new_r = new_date_version()
    last = r.split('.')[-1]
    if r.startswith(new_r):
        new_r = new_r + '.' + str(int(last) + 1)
    else:
        new_r = new_r + '.0'
    print(r, new_r)
    txt = txt.replace(r, new_r)
    open(target, 'w', newline='\n').write(txt)
    if docopt['--gitsync']:
        os.system('git add . ')
        os.system('git commit -m "add version {}"'.format(new_r))
        os.system('git pull')
        os.system('git push')

    r = util.Redis.set(f'cache:pip:{package}.latest',  new_r)
    print(r.json())


if __name__ == '__main__':
    add_version([])
