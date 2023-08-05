import subprocess
import os

from shortest_api_client import getLogger

logger = getLogger('lowlevel-image-builder')
logger.setLevel('DEBUG')


class DockerHandler:
    def __init__(self):
        pass

    def build(self, dockerfile, name=None, tag=None, force_rm=False, no_cache=False, params=None):
        params = [] if not params else params
        logger.info(f'DOCKERFILE:\n {dockerfile}\n')
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile)

        cmd = ['docker', 'build']
        if name is not None:
            cmd.append('-t')
            if tag is not None:
                cmd.append('{}:{}'.format(name, tag))
            else:
                cmd.append(name)

        if force_rm:
            cmd.append('--force-rm')
        if no_cache:
            cmd.append('--no-cache')
        for p in params:
            cmd.append(p)

        cmd.append('.')
        logger.info('start build\n')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        rcode = p.wait()
        os.remove('Dockerfile')
        if rcode:
            err = p.stderr.read().decode()
            logger.error(err)
            raise Exception(err)
        logger.info('finish build\n')

    def rmi(self, name, tag=None, force=False, params=None):
        params = [] if not params else params
        if params is None:
            params = []
        full_name = name
        if tag is not None:
            full_name += ':' + tag

        cmd = ['docker', 'rmi']
        if force:
            cmd.append('-f')

        for p in params:
            cmd.append(p)

        cmd.append(full_name)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        rcode = p.wait()
        if rcode:
            err = p.stderr.read().decode()
            logger.error(err)
            raise Exception(err)
        logger.info(f'remove image: {full_name}\n')

    def images(self):
        p = subprocess.Popen(['docker', 'images', '-q'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        rcode = p.wait()
        if rcode:
            err = p.stderr.read().decode()
            logger.error(err)
            raise Exception(err)

        return p.stdout.read().decode()

    def pull(self, name, tag=None, params=None):
        params = [] if not params else params
        cmd = ['docker', 'pull']
        for p in params:
            cmd.append(p)

        if tag is not None:
            cmd.append('{}:{}'.format(name, tag))
        else:
            cmd.append(name)
        logger.info(f'start pull: {name}\n')
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        rcode = p.wait()
        if rcode:
            err = p.stderr.read().decode()
            logger.error(err)
            raise Exception(err)
        logger.info(f'finish pull: {name}\n')

    def push(self, name, tag=None, params=None):
        params = [] if not params else params
        cmd = ['docker', 'push']
        for p in params:
            cmd.append(p)

        if tag is not None:
            cmd.append('{}:{}'.format(name, tag))
        else:
            cmd.append(name)
        logger.info(f'start push: {name}\n')
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        rcode = p.wait()
        if rcode:
            err = p.stderr.read().decode()
            logger.error(err)
            raise Exception(err)

        logger.info(f'finish push: {name}\n')
