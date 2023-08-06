import json
import os
import uuid

from shortesttrack_tools.api_client.endpoints import ExecAPIEndpoint, DataEndpoint
from shortesttrack_tools.functional import cached_property

from shortest_image_builder.docker_handler import DockerHandler
from shortest_image_builder.stdockerfile import STDockerfile
from shortest_image_builder.utils import APIClient, getLogger

logger = getLogger('highlevel-image-builder')


class ImageBuilder:
    def __init__(self, host, sec_id, issc_id, sec_refresh_token,
                 gcr_host='us.gcr.io', gcr_project='synapse-157713'):
        self._issc_id = issc_id
        self._sec_id = sec_id
        self._docker = DockerHandler()

        api_client = APIClient(host, sec_id, issc_id, sec_refresh_token)
        self.exec_api = ExecAPIEndpoint(api_client=api_client, script_execution_configuration_id=sec_id)
        self.data_endpoint = DataEndpoint(api_client=api_client, script_execution_configuration_id=sec_id)

        name = 'i-script-images'
        self._gcr_prefix = f'{gcr_host}/{gcr_project}/{name}/{self.issc["owner_id"]}'

    @cached_property
    def issc(self) -> dict:
        path = f'issc/{self._issc_id}/'
        return self.exec_api.request(self.exec_api.GET, path)

    @cached_property
    def script_content(self) -> bytes:
        return self.data_endpoint.request(self.data_endpoint.GET, f'script-execution-configurations/'
                                          f'{self._sec_id}/script/content', raw_content=True)

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

        ipynb_content = self.script_content.decode()

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
        self._docker.build(dockerfile.to_string(), name=full_name, tag=tag, force_rm=force_rm,
                           no_cache=no_cache, params=params)

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
