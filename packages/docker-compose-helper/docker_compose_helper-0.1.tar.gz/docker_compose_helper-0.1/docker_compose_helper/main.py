import re
import subprocess
import sys
import os
import argparse

COMPOSE_FILE = 'docker-compose.yml'
COMPOSE_DEV_FILE = 'docker-compose.dev.yml'
COMPOSE_PROD_FILE = 'docker-compose.prod.yml'

def get_extra_args(dev):
    if not os.path.exists(COMPOSE_FILE):
        return []

    extra_args = ['-f', COMPOSE_FILE]

    if dev:
        RE_PARAMS = re.compile('dc-dev:(.+)')
    else:
        RE_PARAMS = re.compile('dc-prod:(.+)')


    f = open(COMPOSE_FILE, 'r')
    for line in f:
        m = RE_PARAMS.search(line)
        if m:
            tmp = m.group(1).strip()
            extra_args += [a.strip() for a in tmp.split(' ')]
            break

    if dev:
        if os.path.exists(COMPOSE_DEV_FILE):
            extra_args += ['-f', COMPOSE_DEV_FILE]
    else:
        if os.path.exists(COMPOSE_PROD_FILE):
            extra_args += ['-f', COMPOSE_PROD_FILE]

    return extra_args

def main():
    args = sys.argv[1:]
    try:
        args.remove('--dev')
        dev = True
    except ValueError:
        dev = False

    if args[0] == 'shell':
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        parser.add_argument('--dev', action='store_true')
        parser.add_argument('service')
        command_args = parser.parse_args()
        args = ['exec', command_args.service, 'sh']

    cmd = ['docker-compose', ] + get_extra_args(dev) + args
    p = subprocess.Popen(cmd)
    try:
        p.wait()
    except KeyboardInterrupt:
        # SIGINT is also sent child procesess
        pass
    return p.returncode

if __name__ == '__main__':
    sys.exit(main())
