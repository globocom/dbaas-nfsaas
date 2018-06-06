# -*- coding: utf-8 -*-
import requests
import logging
import paramiko
import socket
from ..errors import GenerateTokenError, GenerateResourceIdError

LOG = logging.getLogger(__name__)


def exec_remote_command(server, username, password, command, output={}):

    try:
        LOG.info(
            "Executing command [%s] on remote server %s" % (command, server))
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        log_stdout = stdout.readlines()
        log_stderr = stderr.readlines()
        exit_status = stdout.channel.recv_exit_status()
        LOG.info("Comand return code: %s, stdout: %s, stderr %s" %
                 (exit_status, log_stdout, log_stderr))
        output['stdout'] = log_stdout
        output['stderr'] = log_stderr
        return exit_status
    except (paramiko.ssh_exception.BadHostKeyException,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.SSHException,
            socket.error) as e:
        LOG.warning("We caught an exception: %s ." % e)
        output['exception'] = str(e)
        return None


def delete_all_disk_files(
        export_path, dir_name, export_id, host, cloud_host=None
):
    mount_path = "/mnt_{}_{}".format(dir_name, export_id)
    command = "mkdir -p {}".format(mount_path)
    command += "\nmount -t nfs -o bg,intr {} {}".format(
        export_path, mount_path
    )
    command += "\nrm -rf {}/*".format(mount_path)
    command += "\numount {}".format(mount_path)
    command += "\nrm -rf {}".format(mount_path)
    LOG.info(command)

    output = {}
    exec_remote_command(
        server=host.address, username=host.user,
        password=host.password, command=command, output=output
    )
    LOG.info(output)


def generate_token(dbaas_api):
    json_data = {
        "auth": {
            "tenantName": dbaas_api.tenant_name,
            "passwordCredentials": {
                "username": dbaas_api.user,
                "password": dbaas_api.password
            }
        }
    }

    response = requests.post(
        dbaas_api.token_endpoint, json=json_data, verify=not dbaas_api.is_secure
    )
    if response.status_code != 200:
        raise GenerateTokenError(response.content)
    return response.json()['access']['token']['id']


def generate_resource_id(disks, dbaas_api):
    token = generate_token(dbaas_api)

    exports = [disk.nfsaas_export_id for disk in disks]
    response = requests.post(
        dbaas_api.resource_endpoint, headers={'X-Auth-Token': token},
        data={'exports': exports}, verify=not dbaas_api.is_secure
    )

    if response.status_code != 200:
        raise GenerateResourceIdError(response.content)

    return response.json()['resource_id']
