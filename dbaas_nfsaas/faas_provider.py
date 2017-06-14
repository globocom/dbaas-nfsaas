import time
from faasclient.client import Client
from util import delete_all_disk_files, generate_resource_id
from errors import CreateExportAPIError, DeleteExportAPIError, \
    CreateAccessAPIError, DeleteAccessAPIError, ListAccessAPIError, \
    CreateSnapshotAPIError, DeleteSnapshotAPIError, RestoreSnapshotAPIError, \
    QuotaAPIError, ResizeAPIError, AccessAPIError


class Provider(object):

    def __init__(self, dbaas_api, host_class, group_klass):
        self.dbaas_api = dbaas_api
        self.client = Client(
            authurl=dbaas_api.endpoint, user=dbaas_api.user,
            key=dbaas_api.password, tenant_name=dbaas_api.tenant_name,
            insecure=dbaas_api.is_secure
        )
        self.host_class = host_class
        self.group_klass = group_klass

    def _get_or_create_infra_group(self, host):
        if not host:
            return self.group_klass()

        infra = host.instances.first().databaseinfra
        group = self.group_klass.objects.filter(infra=infra).first()
        if not group:
            group = self.group_klass()
            group.infra = infra
            group.resource_id = None
        return group

    def create_export(self, host, size_kb):
        group = self._get_or_create_infra_group(host)
        request = self.client.export_create(
            size_kb, self.dbaas_api.category, group.resource_id
        )

        if request[0] != 201:
            raise CreateExportAPIError(request)

        export = request[1]

        if not group.resource_id:
            group.resource_id = export['resource_id']
            group.save()

        disk = self.host_class(
            host=host,
            nfsaas_export_id=export['id'],
            nfsaas_path_host=export['path'],
            nfsaas_path=export['full_path'],
            nfsaas_size_kb=size_kb,
            group=group
        )
        disk.save()

        return disk

    def delete_export(self, path, cloud_host=None):
        disk = self.host_class.objects.get(nfsaas_path_host=path)

        try:
            self.create_access(disk.nfsaas_path_host, disk.host.address)
        except AccessAPIError:
            pass

        delete_all_disk_files(
            disk.nfsaas_path, disk.nfsaas_path_host,
            disk.nfsaas_export_id, disk.host, cloud_host
        )

        request = self.client.export_delete(disk.nfsaas_path_host)
        if request[0] != 200:
            raise DeleteExportAPIError(request)

        disk.delete()

        if disk.group:
            group = disk.group
            if not group.hosts.all():
                group.delete()

        return True

    def list_access(self, export_path):
        request = self.client.access_list(export_path)
        if request[0] != 200:
            raise ListAccessAPIError(request)

        return request[1]

    def check_access_exist(self, export_path, address):
        for item in self.list_access(export_path):
            if item['host'] == address:
                return item

    def create_access(self, export_path, address):
        access = self.check_access_exist(export_path, address)
        if access:
            return access

        request = self.client.access_create(
            export_path, self.dbaas_api.access_permission, address
        )
        if request[0] != 201:
            raise CreateAccessAPIError(request)

        return request[1]

    def delete_access(self, export_path, address):
        access = self.check_access_exist(export_path, address)
        if not access:
            return True

        request = self.client.access_delete(export_path, access['id'])
        if request[0] != 200:
            raise DeleteAccessAPIError(request)

        return True

    def create_snapshot(self, export_path):
        request = self.client.snapshot_create(export_path)
        if request[0] != 201:
            raise CreateSnapshotAPIError(request)

        return request[1]

    def delete_snapshot(self, export_path, snapshot_id):
        request = self.client.snapshot_delete(export_path, snapshot_id)
        if request[0] != 200:
            raise DeleteSnapshotAPIError(request)

        return True

    def restore_snapshot(self, export_path, snapshot_id):
        request = self.client.snapshot_restore(export_path, snapshot_id)
        if request[0] != 200:
            raise RestoreSnapshotAPIError(request)

        return request[1]

    def wait_for_job_finished(self, restore_job, attempts=50, interval=30):
        for i in xrange(attempts):
            request = self.client.jobs_get(restore_job)

            if request[0] != 200:
                raise RestoreSnapshotAPIError(request)

            if request[1]['status'] == 'finished':
                return request[1]['result']

            time.sleep(interval)

    def get_export_size(self, export_path):
        request = self.client.quota_get(export_path)
        if request[0] != 200:
            raise QuotaAPIError(request)

        return request[1]

    def resize(self, export_path, new_size_kb):
        request = self.client.quota_post(export_path, new_size_kb)
        if request[0] != 200:
            raise ResizeAPIError(request)

        return True

    def create_resource_id(self, infra):
        disks = set()
        for instance in infra.instances.all():
            for disk in instance.hostname.nfsaas_host_attributes.all():
                disks.add(disk)

        group = self.group_klass()
        group.infra = infra
        group.resource_id = generate_resource_id(disks, self.dbaas_api)
        group.save()

        for disk in disks:
            disk.group = group
            disk.save()
