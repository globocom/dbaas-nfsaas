# -*- coding: utf-8 -*-
import unittest
from dbaas_nfsaas.dbaas_api import DatabaseAsAServiceApi
from tests import Credential


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credential = Credential()
        cls.dbaas_api = DatabaseAsAServiceApi(cls.credential)

    def test_dbaas_api_from_credential(self):
        self.assertEqual(self.credential.endpoint, self.dbaas_api.endpoint)
        self.assertEqual(self.credential.user, self.dbaas_api.user)
        self.assertEqual(self.credential.password, self.dbaas_api.password)
        self.assertEqual(self.credential.project, self.dbaas_api.tenant_name)

        self.assertIsInstance(self.dbaas_api.is_secure, bool)
        self.assertEqual(
            bool(self.credential.param_is_secure.value),
            self.dbaas_api.is_secure
        )

        self.assertIsInstance(self.dbaas_api.category, int)
        self.assertEqual(
            int(self.credential.param_category.value), self.dbaas_api.category
        )

        self.assertIsInstance(self.dbaas_api.access_permission, str)
        self.assertEqual(
            self.credential.param_access_permission.value,
            self.dbaas_api.access_permission
        )
