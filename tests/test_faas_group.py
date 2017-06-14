# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from dbaas_nfsaas.faas_provider import Provider
from tests import Credential, FakeHostClass, GROUPS, FakeCloudClass, \
    FakeGroup, FakeDatabaseInfra, clean_faas_environment, FakePhysicalHost, \
    FakePhysicalInstance


class TestFaaS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = Credential()
        cls.dbaas_api = DatabaseAsAServiceApi(credentials=cls.credential)
        cls.provider = Provider(
            dbaas_api=cls.dbaas_api, host_class=FakeHostClass,
            group_klass=FakeGroup
        )

    @classmethod
    def tearDownClass(cls):
        clean_faas_environment(cls.provider)

    def test_create_and_destroy_group(self):
        self.assertEqual(len(GROUPS), 0)

        host = self.provider.create_export(size_kb=512, host=FakeCloudClass)
        self.assertIsNotNone(host.nfsaas_path)
        self.assertIsNotNone(host.nfsaas_path_host)
        self.assertEqual(host.nfsaas_size_kb, 512)
        self.assertGreater(host.nfsaas_export_id, 0)
        self.assertIn(host.group, GROUPS)
        self.assertEqual(len(GROUPS), 1)

        self.provider.delete_export(host.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 0)

    def test_three_hosts_same_group(self):
        self.assertEqual(len(GROUPS), 0)

        infra = FakeDatabaseInfra()
        new_host = FakeCloudClass
        new_host.instances.first().databaseinfra = infra
        host_1 = self.provider.create_export(size_kb=512, host=new_host)
        host_2 = self.provider.create_export(size_kb=512, host=new_host)
        host_3 = self.provider.create_export(size_kb=512, host=new_host)

        self.assertEqual(len(GROUPS), 1)
        self.assertEqual(host_1.group, host_2.group)
        self.assertNotEqual(host_1.nfsaas_path_host, host_2.nfsaas_path_host)

        self.assertEqual(host_2.group, host_3.group)
        self.assertNotEqual(host_2.nfsaas_path_host, host_3.nfsaas_path_host)

        self.assertEqual(host_3.group, host_1.group)
        self.assertNotEqual(host_3.nfsaas_path_host, host_1.nfsaas_path_host)

        self.provider.delete_export(host_1.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 1)

        self.provider.delete_export(host_2.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 1)

        self.provider.delete_export(host_3.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 0)

    def test_can_generate_resource_id_ha(self):
        self.assertEqual(len(GROUPS), 0)
        disk_1 = self.provider.create_export(size_kb=512, host=FakeCloudClass)
        disk_2 = self.provider.create_export(size_kb=512, host=FakeCloudClass)
        disk_3 = self.provider.create_export(size_kb=512, host=FakeCloudClass)

        self.assertEqual(len(GROUPS), 1)
        GROUPS[0].delete()
        self.assertEqual(len(GROUPS), 0)

        disk_1.group = None
        disk_2.group = None
        disk_3.group = None

        infra = FakeDatabaseInfra([
            FakePhysicalInstance(FakePhysicalHost([disk_1, disk_3])),
            FakePhysicalInstance(FakePhysicalHost([disk_2]))
        ])
        self.provider.create_resource_id(infra)

        self.assertEqual(len(GROUPS), 1)
        self.assertEqual(disk_1.group, GROUPS[0])
        self.assertEqual(disk_2.group, GROUPS[0])
        self.assertEqual(disk_3.group, GROUPS[0])
        self.assertEqual(len(GROUPS[0].hosts.all()), 3)
        self.assertIn(disk_1, GROUPS[0].hosts.all())
        self.assertIn(disk_2, GROUPS[0].hosts.all())
        self.assertIn(disk_3, GROUPS[0].hosts.all())

        self.provider.delete_export(disk_1.nfsaas_path_host, FakeCloudClass)
        self.provider.delete_export(disk_2.nfsaas_path_host, FakeCloudClass)
        self.provider.delete_export(disk_3.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 0)

    def test_can_generate_resource_id_single(self):
        self.assertEqual(len(GROUPS), 0)
        disk = self.provider.create_export(size_kb=512, host=FakeCloudClass)

        self.assertEqual(len(GROUPS), 1)
        GROUPS[0].delete()
        self.assertEqual(len(GROUPS), 0)
        disk.group = None

        infra = FakeDatabaseInfra([
            FakePhysicalInstance(FakePhysicalHost([disk]))
        ])
        self.provider.create_resource_id(infra)

        self.assertEqual(len(GROUPS), 1)
        self.assertEqual(disk.group, GROUPS[0])

        self.provider.delete_export(disk.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 0)

    def test_can_generate_resource_id_multi_infra(self):
        infra_1 = FakeDatabaseInfra()
        infra_1.databaseinfra = 'Fake_01'

        infra_2 = FakeDatabaseInfra()
        infra_2.databaseinfra = 'Fake_02'

        self.assertEqual(len(GROUPS), 0)
        disk_1 = self.provider.create_export(size_kb=512, host=FakeCloudClass(infra_1))
        disk_2 = self.provider.create_export(size_kb=512, host=FakeCloudClass(infra_2))

        self.assertEqual(len(GROUPS), 2)
        while GROUPS:
            GROUPS[0].delete()
        self.assertEqual(len(GROUPS), 0)
        disk_1.group = None
        disk_2.group = None

        infra_1.instances.items.append(
            FakePhysicalInstance(FakePhysicalHost([disk_1]))
        )
        self.provider.create_resource_id(infra_1)
        self.assertEqual(len(GROUPS), 1)

        infra_2.instances.items.append(
            FakePhysicalInstance(FakePhysicalHost([disk_2]))
        )
        self.provider.create_resource_id(infra_2)
        self.assertEqual(len(GROUPS), 2)

        self.assertEqual(disk_1.group, GROUPS[0])
        self.assertEqual(disk_2.group, GROUPS[1])

        self.provider.delete_export(disk_1.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 1)
        self.provider.delete_export(disk_2.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(GROUPS), 0)
