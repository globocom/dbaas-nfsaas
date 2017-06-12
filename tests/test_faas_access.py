# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from dbaas_nfsaas.faas_provider import Provider
from dbaas_nfsaas.errors import CreateAccessAPIError, DeleteAccessAPIError, \
    ListAccessAPIError
from tests import Credential, FakeHostClass, FakeFaaSAPI, FakeCloudClass, \
    FakeGroup
from tests import FAKE_IP, FAKE_IP_OTHER


class TestFaaS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = Credential()
        cls.dbaas_api = DatabaseAsAServiceApi(credentials=cls.credential)
        cls.provider = Provider(
            dbaas_api=cls.dbaas_api, host_class=FakeHostClass,
            group_klass=FakeGroup
        )
        cls.host = cls.provider.create_export(size_kb=512, host=FakeCloudClass)

    def setUp(self):
        self.assertEqual(
            len(self.provider.list_access(self.host.nfsaas_path_host)), 0
        )

    @classmethod
    def tearDownClass(cls):
        cls.provider.delete_export(cls.host.nfsaas_path_host, FakeCloudClass)

    def tearDown(self):
        for access in self.provider.list_access(self.host.nfsaas_path_host):
            self.assertTrue(
                self.provider.delete_access(
                    self.host.nfsaas_path_host, access['host']
                )
            )

    def test_can_create_access(self):
        self.assertFalse(
            self.provider.check_access_exist(
                self.host.nfsaas_path_host, FAKE_IP
            )
        )
        access = self.provider.create_access(
            self.host.nfsaas_path_host, FAKE_IP
        )

        self.assertEqual(access['host'], FAKE_IP)
        self.assertEqual(access['permission'],
                         self.dbaas_api.access_permission)
        self.assertTrue(
            self.provider.check_access_exist(
                self.host.nfsaas_path_host, FAKE_IP
            )
        )

    def test_cannot_create_access_twice(self):
        access = self.provider.create_access(
            self.host.nfsaas_path_host, FAKE_IP
        )
        found = self.provider.create_access(
            self.host.nfsaas_path_host, FAKE_IP
        )

        self.assertEqual(
            len(self.provider.list_access(self.host.nfsaas_path_host)), 1
        )

        self.assertEqual(access, found)

    def test_cannot_create_access_api_error(self):
        faas_client = self.provider.client

        try:
            self.provider.client = FakeFaaSAPI()
            self.assertRaises(
                CreateAccessAPIError, self.provider.create_access,
                self.host.nfsaas_path_host, FAKE_IP
            )
        finally:
            self.provider.client = faas_client

    def test_can_delete_access(self):
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP)
        self.assertTrue(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )

        self.assertTrue(
            self.provider.delete_access(self.host.nfsaas_path_host, FAKE_IP)
        )
        self.assertFalse(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )

    def test_cannot_delete_deleted_access(self):
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP)
        self.assertTrue(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )
        self.assertTrue(
            self.provider.delete_access(self.host.nfsaas_path_host, FAKE_IP)
        )

        self.assertFalse(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )
        self.assertTrue(
            self.provider.delete_access(self.host.nfsaas_path_host, FAKE_IP)
        )
        self.assertFalse(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )

    def test_cannot_delete_access_api_error(self):
        faas_client = self.provider.client

        try:
            self.provider.client = FakeFaaSAPI()
            self.provider.client.accesses.append({'host': FAKE_IP, 'id': 1})
            self.assertRaises(
                DeleteAccessAPIError, self.provider.delete_access,
                self.host.nfsaas_path_host, FAKE_IP
            )
        finally:
            self.provider.client = faas_client

    def test_can_list_access(self):
        self.provider.list_access(self.host.nfsaas_path_host)
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP)
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP_OTHER)

        access_list = self.provider.list_access(self.host.nfsaas_path_host)
        self.assertEqual(
            len(access_list), 2
        )

    def test_cannot_list_api_error(self):
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP)
        self.assertRaises(
            ListAccessAPIError, self.provider.list_access, 'WRONG_HOST'
        )

    def test_can_find_created_access(self):
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP)
        self.assertTrue(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )

        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP_OTHER)
        self.assertTrue(
            self.provider.check_access_exist(
                self.host.nfsaas_path_host, FAKE_IP_OTHER
            )
        )

    def test_cannot_find_access(self):
        self.provider.create_access(self.host.nfsaas_path_host, FAKE_IP)
        self.assertTrue(
            self.provider.check_access_exist(self.host.nfsaas_path_host,
                                             FAKE_IP)
        )

        self.assertFalse(
            self.provider.check_access_exist(
                self.host.nfsaas_path_host, FAKE_IP_OTHER
            )
        )

    def test_cannot_find_access_empty_list(self):
        self.assertFalse(
            self.provider.check_access_exist(
                self.host.nfsaas_path_host, FAKE_IP
            )
        )
