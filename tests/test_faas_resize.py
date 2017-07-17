# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from dbaas_nfsaas.faas_provider import Provider
from dbaas_nfsaas.errors import QuotaAPIError, ResizeAPIError
from tests import Credential, FakeHostClass, clean_faas_environment, FakeGroup


class TestFaaS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = Credential()
        cls.dbaas_api = DatabaseAsAServiceApi(credentials=cls.credential)
        cls.provider = Provider(
            dbaas_api=cls.dbaas_api, host_class=FakeHostClass,
            group_class=FakeGroup
        )

    @classmethod
    def tearDownClass(cls):
        clean_faas_environment(cls.provider)

    def test_can_get_export_quota(self):
        host = self.provider.create_export(size_kb=4096, host=None)
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 4096)
        self.assertGreaterEqual(quota['disk-used'], 0)

    def test_cannot_get_export_quota(self):
        self.assertRaises(QuotaAPIError, self.provider.get_export_size, 'fake')

    def test_can_do_resize_greater_size(self):
        host = self.provider.create_export(size_kb=512, host=None)
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 512)

        self.assertTrue(self.provider.resize(host.nfsaas_path_host, 1024))
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 1024)

    def test_can_do_resize_lower_size(self):
        host = self.provider.create_export(size_kb=2048, host=None)
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 2048)

        self.assertTrue(self.provider.resize(host.nfsaas_path_host, 256))
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 256)

    def test_can_do_resize_equal_size(self):
        host = self.provider.create_export(size_kb=512, host=None)
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 512)

        self.assertTrue(self.provider.resize(host.nfsaas_path_host, 512))
        quota = self.provider.get_export_size(host.nfsaas_path_host)
        self.assertEqual(quota['disk-limit'], 512)

    def test_cannot_create_snapshot_api_error(self):
        self.assertRaises(ResizeAPIError, self.provider.resize, '', -50)
