# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from dbaas_nfsaas.faas_provider import Provider
from dbaas_nfsaas.errors import CreateSnapshotAPIError, \
    DeleteSnapshotAPIError, RestoreSnapshotAPIError
from tests import Credential, FakeHostClass, clean_faas_environment, FakeGroup


class TestFaaS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = Credential()
        cls.dbaas_api = DatabaseAsAServiceApi(credentials=cls.credential)
        cls.provider = Provider(
            dbaas_api=cls.dbaas_api, host_class=FakeHostClass,
            group_klass=FakeGroup
        )
        cls.host = cls.provider.create_export(size_kb=512, host=None)

    def setUp(self):
        self.assertEqual(
            len(self.provider.list_access(self.host.nfsaas_path_host)), 0
        )

    @classmethod
    def tearDownClass(cls):
        clean_faas_environment(cls.provider)

    def test_can_create_snapshot(self):
        snapshot = self.provider.create_snapshot(self.host.nfsaas_path_host)
        self.assertIsNotNone(snapshot['snapshot']['name'])
        self.assertGreater(snapshot['snapshot']['id'], 0)
        self.assertIsNotNone(snapshot['snapshot']['type'])

    def test_cannot_create_snapshot_api_error(self):
        self.assertRaises(
            CreateSnapshotAPIError,
            self.provider.create_snapshot, ''
        )

    def test_can_delete_snapshot(self):
        snapshot = self.provider.create_snapshot(self.host.nfsaas_path_host)
        self.assertTrue(
            self.provider.delete_snapshot(
                self.host.nfsaas_path_host, snapshot['snapshot']['id']
            )
        )

    def test_cannot_delete_snapshot_api_error(self):
        self.assertRaises(
            DeleteSnapshotAPIError, self.provider.delete_snapshot,
            self.host.nfsaas_path_host, -111
        )

    def test_can_restore_snapshot(self):
        snapshot = self.provider.create_snapshot(self.host.nfsaas_path_host)
        restore = self.provider.restore_snapshot(
            self.host.nfsaas_path_host, snapshot['snapshot']['id']
        )
        self.assertIsNotNone(restore['job'])
        self.assertIsNotNone(restore['created_at'])

    def test_cannot_restore_snapshot_api_error(self):
        self.assertRaises(
            RestoreSnapshotAPIError, self.provider.restore_snapshot,
            self.host.nfsaas_path_host, -111
        )

    def test_can_wait_for_restore_finished(self):
        snapshot = self.provider.create_snapshot(self.host.nfsaas_path_host)
        restore = self.provider.restore_snapshot(
            self.host.nfsaas_path_host, snapshot['snapshot']['id']
        )
        status = self.provider.wait_for_job_finished(restore['job'])
        self.assertIn('id', status)
        self.assertIn('path', status)
        self.assertIn('full_path', status)
        self.assertIn('original_export', status)

    def test_cannot_wait_for_restore_finished_api_error(self):
        self.assertRaises(
            RestoreSnapshotAPIError, self.provider.wait_for_job_finished, -111
        )

    def test_cannot_wait_for_restore_finished_short_time(self):
        snapshot = self.provider.create_snapshot(self.host.nfsaas_path_host)
        restore = self.provider.restore_snapshot(
            self.host.nfsaas_path_host, snapshot['snapshot']['id']
        )
        self.assertFalse(
            self.provider.wait_for_job_finished(restore['job'], 0, 0)
        )
        self.assertTrue(
            self.provider.wait_for_job_finished(restore['job'])
        )
