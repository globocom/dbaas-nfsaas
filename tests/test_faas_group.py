# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from dbaas_nfsaas.faas_provider import Provider
from tests import Credential, FakeHostClass, GROUPS, FakeCloudClass, \
    FakeGroup, FakeDatabaseInfra, clean_faas_environment


class TestFaaS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = Credential()
        cls.dbaas_api = DatabaseAsAServiceApi(credentials=cls.credential)
        cls.provider = Provider(
            dbaas_api=cls.dbaas_api, host_class=FakeHostClass,
            group_klass=FakeGroup
        )

    def tearDown(self):
        clean_faas_environment(self.provider)

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
