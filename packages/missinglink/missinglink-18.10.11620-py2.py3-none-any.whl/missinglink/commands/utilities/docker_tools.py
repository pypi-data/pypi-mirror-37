import logging
from collections import namedtuple

import click
import docker
import docker.errors as docker_errors
import requests
import six
from missinglink.core.api import ApiCaller

from .path_tools import PathTools

logger = logging.getLogger(__file__)

rm_config = namedtuple('RmConfig', ['rm_socket_server', 'rm_manager_image', 'rm_config_volume', 'rm_container_name', 'ml_backend'])
running_ml_container = namedtuple('RunningRmContainer', ['id', 'name', 'display', 'container'])


class DockerTools(object):
    @classmethod
    def get_config_prefix_and_file(cls, config):
        with open(config.config_file_abs_path, 'rb') as f:
            config_data = f.read()
        prefix = None
        if config.config_prefix is not None:
            prefix = config.config_prefix
        return prefix, config_data

    ADMIN_VOLUME = {'/var/run/docker.sock': {'bind': '/var/run/docker.sock'}}
    DOCKER_IMAGE = 'docker:latest'

    @classmethod
    def _get_combined_volume_path(cls, *args):
        res = {}
        for a in args:
            res.update(a)

        return res

    @classmethod
    def create(cls, ctx, **kwargs):
        return cls(ctx, **kwargs)

    def __init__(self, ctx, cloud_credentials=None, **kwargs):
        self.ctx = ctx
        self.cloud_credentials = cloud_credentials
        self.config = rm_config(
            rm_socket_server=kwargs.pop('rm_socket_server', self.ctx.obj.config.rm_socket_server),
            rm_manager_image=kwargs.pop('rm_manager_image', self.ctx.obj.config.rm_manager_image),
            rm_container_name=kwargs.pop('rm_container_name', self.ctx.obj.config.rm_container_name),
            rm_config_volume=kwargs.pop('rm_config_volume', self.ctx.obj.config.rm_config_volume),
            ml_backend=kwargs.pop('ml_backend', self.ctx.obj.config.api_host)
        )

        self._client = kwargs.pop('client', None)

    @property
    def client(self):
        if self._client is None:
            logger.warning('validating docker')
            self._client = self.validate_and_get_docker_client()

        return self._client

    def pull_image_from_image(self, image, msg=None):

        try:
            self.client.images.get(self.DOCKER_IMAGE)
        except docker_errors.NotFound:
            click.echo(msg or ('Pulling docker image: %s' % image))
            self.client.images.pull(self.DOCKER_IMAGE)

        cmd = 'docker pull {}'.format(image)
        socket_volumes = {'/var/run/docker.sock': {'bind': '/var/run/docker.sock'}}

        cont = self.client.containers.run(self.DOCKER_IMAGE, command=cmd, auto_remove=True, volumes=socket_volumes, environment={'ML_RM_MANAGER': '1'}, detach=True)
        logger_handler = cont.logs(stdout=True, stderr=True, stream=True)
        for log in logger_handler:
            logger.info(log)

        return self.client.images.get(image)

    def pull_rm_image(self):
        click.echo('Getting/updating MissingLinks Resource Manager image')
        img = self.pull_image_from_image(self.config.rm_manager_image)
        return img

    def _api_call(self, *args, **kwargs):
        return ApiCaller.call(self.ctx.obj, self.ctx.obj.session, *args, **kwargs)

    def auth_resource(self, org):
        return self._api_call('get', '{org}/resource/authorise'.format(org=org)).get('token')

    @classmethod
    def validate_and_get_docker_client(cls):
        client = docker.from_env()
        try:
            client.ping()
        except docker_errors.DockerException as ex:
            raise click.BadArgumentUsage('Docker: Failed to connect to docker host %s' % (str(ex)))
        except requests.exceptions.ConnectionError as ex:
            raise click.BadArgumentUsage('Docker: Failed to connect to docker host %s' % (str(ex)))

        logging.info('Docker host verified')

        return client

    @classmethod
    def _docker_present_return_instance(cls, command, *args, **kwargs):
        try:
            return command(*args, **kwargs)
        except docker_errors.NotFound:
            pass

    @classmethod
    def _docker_present(cls, command, *args, **kwargs):
        try:
            return command(*args, **kwargs) or True  # we are looking only for exceptions here
        except docker_errors.NotFound:
            return False

    def validate_no_running_resource_manager(self, force):
        current_rm = self._docker_present_return_instance(self.client.containers.get, self.config.rm_container_name)
        if current_rm is None:
            return

        if not force:
            raise click.BadOptionUsage('Can not install resource manger while one is running. run `docker kill {}` do stop and reuse config or re-run with `--force` flag to clear all configuration'.format(current_rm.name))

        click.echo('Killing current Resource Manger (%s) due to --force flag' % current_rm.id)
        if current_rm.status == 'running':
            current_rm.kill()

        current_rm.remove(force=True)

    @classmethod
    def export_key_from_path(cls, ssh_key_path):
        from missinglink.crypto import SshIdentity

        return SshIdentity(ssh_key_path).export_private_key_bytes()

    def validate_local_config(self, org, force, ssh_key_path, token):

        ssh_key = None
        if (not self.config_volume_if_present() or force) and ssh_key_path is None:
            ssh_key_path = click.prompt(text='SSH key path (--ssh-key-path)', default=PathTools.get_ssh_path())

        token = self._handle_token_and_data_path(force, org, token=token)

        if ssh_key_path is not None:
            ssh_key = self.export_key_from_path(ssh_key_path).decode('utf-8')

        prefix, ml_data = self.get_config_prefix_and_file(self.ctx.obj.config)

        self.setup_rms_volume(ssh_key=ssh_key, token=token, ml_data=ml_data, prefix=prefix, force=True)

    def _handle_token_and_data_path(self, force, org, token=None):
        cur_config = self.ctx.obj.config.resource_manager_config
        if force:
            click.echo('Current host config is deleted due to `--force` flag')
            cur_config = {}

        new_token = token or cur_config.get('token')

        if new_token is None:
            new_token = self.auth_resource(org)
        self.ctx.obj.config.update_and_save({
            'resource_manager': {
                'token': new_token,
            }
        })
        return new_token

    def _apply_ssh_params(self, ssh_key):
        if ssh_key is not None:
            return ['--ssh-private-key', ssh_key]

        return []

    def _apply_ws_server(self):
        if self.config.rm_socket_server:
            return ['--ml-server', self.config.rm_socket_server]

        return []

    def _ensure_auth(self):
        id_token = self.ctx.obj.config.id_token
        if id_token is None:
            raise click.BadOptionUsage('Please call `ml auth init` first')

    def _decode_if_needed(self, data):
        if data and isinstance(data, six.binary_type):
            return data.decode('utf-8')

        return data

    def _apply_ml_data(self, prefix, ml_data):
        if prefix is None and ml_data is None:
            self._ensure_auth()
            prefix, ml_data = self.get_config_prefix_and_file(self.ctx.obj.config)

        ml_data = self._decode_if_needed(ml_data)
        res = ['--ml-config-file', ml_data]

        if prefix is not None:
            res.extend(['--ml-config-prefix', prefix])

        return res

    def _apply_token(self, token):
        if token is not None:
            return ['--ml-token', token]

        return []

    def _apply_backend(self):
        if self.config.ml_backend is not None:
            return ['--ml-backend', self.config.ml_backend]

        return []

    def append_cred_data_to_command(self, command):
        if self.cloud_credentials:
            self.cloud_credentials.extend_command_with_creds(command)

    def _apply_config_to_volume(self, ssh_key=None, token=None, prefix=None, ml_data=None):
        config_volume = {self.config.rm_config_volume: {'bind': '/config'}}
        conf_mounts = self._get_combined_volume_path(self.ADMIN_VOLUME, config_volume)
        command = ['config']
        command.extend(self._apply_ws_server())
        command.extend(self._apply_backend())
        command.extend(self._apply_ssh_params(ssh_key))
        command.extend(self._apply_ml_data(prefix, ml_data))
        command.extend(self._apply_token(token))
        self.append_cred_data_to_command(command)
        cont = self.client.containers.run(
            self.config.rm_manager_image, command=command,
            volumes=conf_mounts,
            environment={'ML_RM_MANAGER': '1'}, detach=True)
        exit_code = cont.wait()
        if exit_code != 0:
            click.echo(cont.logs())
        cont.remove()

    def validate_config_volume(self):
        if not self.config_volume_if_present():
            raise click.BadArgumentUsage('Configuration volume is missing. Please re-install')

    def run_resource_manager(self):

        self.validate_config_volume()
        click.echo('Starting Resource Manager')
        config_volume = {self.config.rm_config_volume: {'bind': '/config'}}
        run_mounts = self._get_combined_volume_path(self.ADMIN_VOLUME, config_volume)
        return self.client.containers.run(
            self.config.rm_manager_image,
            command=['run'],
            auto_remove=False,
            restart_policy={"Name": 'always'},
            volumes=run_mounts,
            environment={'ML_RM_MANAGER': '1', 'ML_CONFIG_VOLUME': self.config.rm_config_volume},
            detach=True,
            network='host',
            name=self.config.rm_container_name)

    def config_volume_if_present(self):
        return self._docker_present(self.client.volumes.get, self.config.rm_config_volume)

    def ensure_cache_volume_present(self):
        cache_volume = '{}_cache'.format(self.config.rm_config_volume)
        if not self._docker_present(self.client.volumes.get, cache_volume):
            self.client.volumes.create(cache_volume)

        return cache_volume

    def resource_manager_server_container_if_present(self):
        return self._docker_present(self.client.containers.get, self.config.rm_container_name)

    def ensure_rms_volume(self, force):
        if self.config_volume_if_present() and force:
            self.client.volumes.get(self.config.rm_config_volume).remove(force=True)

        if not self.config_volume_if_present():
            self.client.volumes.create(self.config.rm_config_volume)

    def setup_rms_volume(self, ssh_key=None, token=None, prefix=None, ml_data=None, force=False):
        click.echo('building volume')
        self.ensure_rms_volume(force)
        self._apply_config_to_volume(ssh_key, token, prefix=prefix, ml_data=ml_data)

    def remove_current_rm_servers(self):
        click.echo('Clear containers')
        for container in self.client.containers.list():
            if container.name == self.config.rm_container_name:
                click.echo("\t  KILL: %s" % container.id)
                container.kill()
        click.echo('Remove containers')
        for container in self.client.containers.list():
            if container.name == self.config.rm_container_name:
                container.remove(force=True)

    def has_nvidia(self):
        try:
            logger.debug('Validating GPU...')
            self.pull_image_from_image('nvidia/cuda:10.0-base', 'Validating GPU configuration')
            logger.debug('Validating GPU... Run')
            self.client.containers.run('nvidia/cuda:10.0-base', 'env', runtime='nvidia', auto_remove=True)
            logger.info('Validating GPU... True')
            return True
        except Exception as ex:
            logger.debug('GPU not found, ignore the error if you do not have GPU installed on this machine', exc_info=1)
            logger.info('GPU not found, ignore the error if you do not have GPU installed on this machine: %s', str(ex))
            return False

    def _extract_container_display(self, container):
        if container.name == self.config.rm_container_name:
            return 'Resource manager'

        res = []
        if 'ML_JOB_ID' in container.labels:
            res.append(container.labels['ML_JOB_ID'])
        if 'ML_STAGE_NAME' in container.labels:
            res.append(container.labels['ML_STAGE_NAME'])

        return ': '.join(res)

    def running_ml_containers(self):
        return [
            running_ml_container(container.short_id, container.name, self._extract_container_display(container), container)
            for container in self.client.containers.list()
            if container.name == self.config.rm_container_name or 'ML' in container.labels
        ]
