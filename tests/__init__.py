# -*- coding: utf-8 -*-
FAKE_IP = '1.2.3.4'
FAKE_IP_OTHER = '1.2.3.5'
HOSTS = []


def get_config(parameter):
    import os
    from ConfigParser import ConfigParser

    file_path = os.path.dirname(os.path.abspath(__file__))

    config = ConfigParser()
    config.read(file_path + '/config/faas_api.ini')
    return config.get('faas', parameter)


def clean_faas_environment(provider):
    import socket
    import os

    machine_ip = socket.gethostbyname(socket.gethostname())
    for export in provider.client.export_list()[1]:
        try:
            dir_name = export['path']
            export_id = export['id']
            export_path = export['full_path']

            mount_path = "mnt_{}_{}".format(dir_name, export_id)
            provider.create_access(dir_name, machine_ip)

            os.system("mkdir -p {}".format(mount_path))
            os.system(
                "mount -t nfs -o bg,intr {} {}".format(export_path, mount_path)
            )
            os.system("rm -rf {}/*".format(mount_path))
            os.system("umount {}".format(mount_path))
            os.system("rm -rf {}".format(mount_path))
            provider.client.export_delete(export['id'])
        except Exception as e:
            print e


class ObjectDoesNotExist(Exception):
    pass


class DjangoObjects(object):
    def __init__(self, items):
        self.items = items

    def filter(self, **kwargs):
        for item in self.items:
            if self._match(item, kwargs):
                yield item

    def get(self, **kwargs):
        for item in self.items:
            if self._match(item, kwargs):
                return item
        raise ObjectDoesNotExist()

    @staticmethod
    def _match(item, kwargs):
        return all((item.__dict__[k] == v for k, v in kwargs.items()))


class Parameter(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Credential(object):
    def __init__(self):
        self.endpoint = get_config('end_point')
        self.user = get_config('user')
        self.password = get_config('password')
        self.project = get_config('project')
        self.parameters = []

        self.param_is_secure = Parameter('is_secure', 'True')
        self.param_category = Parameter('category_id', '2')
        self.param_access_permission = Parameter(
            'access_permission', 'read-write'
        )
        self.parameters.append(self.param_is_secure)
        self.parameters.append(self.param_category)
        self.parameters.append(self.param_access_permission)

    def get_parameter_by_name(self, name):
        for param in self.parameters:
            if param.name == name:
                return param.value


class FakeHostClass(object):

    objects = DjangoObjects(HOSTS)

    def __init__(
            self, host, nfsaas_export_id, nfsaas_path,
            nfsaas_path_host, nfsaas_size_kb
    ):
        self.host = host
        self.nfsaas_export_id = nfsaas_export_id
        self.nfsaas_path_host = nfsaas_path_host
        self.nfsaas_path = nfsaas_path
        self.nfsaas_size_kb = nfsaas_size_kb

    def save(self):
        HOSTS.append(self)

    def delete(self):
        HOSTS.remove(self)


class FakeFaaSAPI(object):
    accesses = []

    def access_list(self, export_path):
        return (200, self.accesses)

    def access_create(self, export_path, permission, address):
        return (999, 'FaaS - FakeAPI Error - Adding Access')

    def access_delete(self, export_path, address):
        return (999, 'FaaS - FakeAPI Error - Removing Access')


class FakeCloudClass(object):
    objects = DjangoObjects([])
    address = 'F.a.k.e'
