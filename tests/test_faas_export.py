# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from dbaas_nfsaas.faas_provider import Provider
from dbaas_nfsaas.errors import CreateExportAPIError, DeleteExportAPIError
from tests import Credential, FakeHostClass, ObjectDoesNotExist, HOSTS, \
    FakeCloudClass, FakeGroup


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
        pass

    def test_can_create_and_destroy_export(self):
        self.assertEqual(len(HOSTS), 0)

        host = self.provider.create_export(size_kb=512, host=FakeCloudClass)
        self.assertIsNotNone(host.nfsaas_path)
        self.assertIsNotNone(host.nfsaas_path_host)
        self.assertEqual(host.nfsaas_size_kb, 512)
        self.assertGreater(host.nfsaas_export_id, 0)
        self.assertIn(host, HOSTS)
        self.assertEqual(len(HOSTS), 1)

        self.provider.delete_export(host.nfsaas_path_host, FakeCloudClass)
        self.assertEqual(len(HOSTS), 0)

    def test_cannot_delete_deleted_export(self):
        self.assertEqual(len(HOSTS), 0)
        self.assertRaises(
            ObjectDoesNotExist, self.provider.delete_export, -500,
            FakeCloudClass
        )
        self.assertEqual(len(HOSTS), 0)

    def test_delete_export_api_error(self):
        self.assertEqual(len(HOSTS), 0)
        fake_host = FakeHostClass(
            host=FakeCloudClass(), nfsaas_export_id=-20,
            nfsaas_path='', nfsaas_path_host='', nfsaas_size_kb=1, group=None
        )
        HOSTS.append(fake_host)
        self.assertEqual(len(HOSTS), 1)

        self.assertRaises(
            DeleteExportAPIError,
            self.provider.delete_export, fake_host.nfsaas_path_host,
            FakeCloudClass
        )
        self.assertEqual(len(HOSTS), 1)

    def test_create_export_api_error(self):
        self.assertEqual(len(HOSTS), 0)
        self.assertRaises(
            CreateExportAPIError,
            self.provider.create_export, None, None
        )
        self.assertEqual(len(HOSTS), 0)
