# -*- coding: utf8 -*-
import click

from .utilities import CommonOptions, CloudCredentialsHandler
from .utilities import DockerTools


@click.group('resources', help='Resource Management')
def resources_commands_old():
    pass


@click.group('resource', help='Resource Management')
def resources_commands():
    pass


@resources_commands.group('local-grid')
def local_grid():
    pass


@local_grid.command('install')
@click.pass_context
@CommonOptions.org_option()
@click.option('--ssh-key-path', type=str, help='Path to the private ssh key to be used by the resource manager', default=None)
@click.option('--force/--no-force', default=False, help='Force installation (stops current resource manager if present')
@click.option('--resource-token', default=None, type=str, help='MissingLink resource token. One will be generated if this instance of ml is authorized')
# cloud creds
@click.option('--link-aws/--no-aws-link', required=False, default=True)
@click.option('--env-aws/--no-aws-env', required=False, default=True)
@click.option('--link-gcp/--no-gcp', required=False, default=True)
def install_rm(ctx, org, ssh_key_path, force, resource_token, **kwargs):
    cred_sync = CloudCredentialsHandler(kwargs)
    docker_tools = DockerTools.create(ctx, cloud_credentials=cred_sync)

    docker_tools.pull_rm_image()
    docker_tools.validate_no_running_resource_manager(force)
    docker_tools.validate_local_config(org=org, force=force, ssh_key_path=ssh_key_path, token=resource_token)

    docker_tools.run_resource_manager()
    click.echo('The resource manager is configured and running')


@resources_commands_old.command('restore_aws_template', help="restores predefined cloud configuration")
@click.pass_context
@click.option('--arn', type=str, help='arn of the KMS encryption key', required=True)
@click.option('--ssh', type=(str, str, str), help='ssh key data', required=True)
@click.option('ml', '--ml', '--mali', type=(str, str, str), help='mali config data', required=True)
@click.option('--prefix', type=str, help='ml prefix type', required=False)
@click.option('--token', type=str, help='ml prefix type', required=True)
@click.option('--rm-socket-server', type=str, help='web socket server', required=True)
@click.option('--rm-manager-image', type=str, required=True)
@click.option('--rm-config-volume', type=str, required=True)
@click.option('--rm-container-name', type=str, required=True)
@click.option('--ml-backend', type=str, required=True)
def apply_aws_template(
        ctx, arn, ssh, ml, prefix, token, rm_socket_server, rm_manager_image,
        rm_config_volume, rm_container_name, ml_backend):
    from .cloud.aws import AwsContext
    if prefix == str(None):
        prefix = None

    click.echo('decrypting data')
    kms = AwsContext.get_kms(arn)
    ssh_key = AwsContext.decrypt(kms, ssh).decode('utf-8')
    ml_data = AwsContext.decrypt(kms, ml).decode('utf-8')
    click.echo('building installation config')
    docker_tools = DockerTools.create(ctx, rm_socket_server=rm_socket_server, rm_manager_image=rm_manager_image, rm_config_volume=rm_config_volume, rm_container_name=rm_container_name, ml_backend=ml_backend)

    click.echo('pulling RM')
    docker_tools.pull_rm_image()

    click.echo('killing RM')
    docker_tools.validate_no_running_resource_manager(True)

    docker_tools.setup_rms_volume(ssh_key, token, prefix=prefix, ml_data=ml_data, force=True)
    docker_tools.remove_current_rm_servers()
    inst = docker_tools.run_resource_manager()
    click.echo('The resource manager is configured and running %s' % inst.id)
    click.echo('docker logs -f %s ' % rm_container_name)
