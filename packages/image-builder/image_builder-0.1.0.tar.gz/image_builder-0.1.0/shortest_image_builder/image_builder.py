import os
import uuid
import json

from shortest_image_builder.docker_handler import DockerHandler
from shortest_image_builder.stdockerfile import STDockerfile
from shortest_api_client.auth_helper import AuthHelper
from shortest_api_client.issc_helper import ISSCHelper
from shortest_api_client.sec_helper import SECHelper
from shortest_api_client import getLogger

logger = getLogger('highlevel-image-builder')
logger.setLevel('DEBUG')

class ImageBuilder:
    def __init__(self, issc_id, token, host=None,
                 sec_host=None, auth_host=None, issc_host=None,
                 gcr_host='us.gcr.io', gcr_project='synapse-157713') -> None:

        self._sec_host = host if sec_host is None else sec_host
        self._issc_host = host if issc_host is None else issc_host
        self._auth_host = host if auth_host is None else auth_host

        self._at = AuthHelper(self._auth_host).get_access_token_from_refresh_token(token)
        self._issc = ISSCHelper(issc_id).get_issc(self._issc_host, self._at.get())
        self._docker = DockerHandler()

        self._gcr_prefix = '{}/{}/{}/{}'.format(gcr_host, gcr_project, 'i-script-images', self._issc['owner_id'])

    def _ipynb_to_py(self, ipynb, with_markdown=False):

        py = ''
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'code':
                py += ''.join(cell['source'])
            if cell['cell_type'] == 'markdown' and with_markdown:
                py += '\n# ' + '# '.join(cell['source'])
            py += '\n\n'

        return py

    def build(self, base_image: str,
              name: str = None,
              tag: str = None,
              force_rm: bool = False,
              no_cache: bool = False,
              params: list = None,
              use_prefix: bool = True) -> str:

        params = [] if not params else params

        ipynb_content = SECHelper(self._issc['configuration']['id']).get_content(self._sec_host, self._at.get()).decode()

        try:
            script_content = self._ipynb_to_py(json.loads(ipynb_content))
        except:
            logger.exception('Decode .ipynb -> .py error')
            script_content = ipynb_content

        logger.info(f'script content: {script_content}')
        with open('user_script.py', 'w') as f:
            f.write(script_content)

        dockerfile = STDockerfile()
        dockerfile.base(base_image)
        dockerfile.add('user_script.py', '/home/root/')

        if name is None:
            name = uuid.uuid4()

        full_name = f'{self._gcr_prefix}/{name}' if use_prefix else name
        self._docker.build(dockerfile.to_string(), name=full_name, tag=tag, force_rm=force_rm, no_cache=no_cache, params=params)
        os.remove('user_script.py')

        return full_name

    def rmi(self, id: str = None,
            name: str = None,
            tag: str = None,
            force: bool = False,
            params: list = None,
            use_prefix: bool = True) -> None:

        params = [] if not params else params
        if name is not None:
            full_name = f'{self._gcr_prefix}/{name}' if use_prefix else name
            self._docker.rmi(name=full_name, tag=tag, force=force, params=params)

        elif id is not None:
            self._docker.rmi(name=id, force=force, params=params)

    def rmi_all(self, force: bool = False, params: list = None) -> None:
        params = [] if not params else params
        ids = self._docker.images().split('\n')[0:-1]
        for id in ids:
            self.rmi(id=id, force=force, params=params)

    def push(self, name: str, tag: str = None, params: list = None, use_prefix=True) -> None:
        params = [] if not params else params
        full_name = f'{self._gcr_prefix}/{name}' if use_prefix else name
        self._docker.push(name=full_name, tag=tag, params=params)

    def pull(self, name: str, tag: str = None, params: list = None, use_prefix=True) -> None:
        params = [] if not params else params
        full_name = f'{self._gcr_prefix}/{name}' if use_prefix else name
        self._docker.pull(name=full_name, tag=tag, params=params)
