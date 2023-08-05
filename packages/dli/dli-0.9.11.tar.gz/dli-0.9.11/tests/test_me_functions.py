import logging
import os
import six

from .common import SdkIntegrationTestCase


class MeFunctionsTestCase(SdkIntegrationTestCase):
    def test_my_consumed_packages(self):
        package_id = self.create_package('test_consumed_packages', access="Unrestricted")
        package = self.client._get_package(package_id)
        package.request_access(
            accountId='iboxx',
            operation='request',
            comment='Hello there!'
        )
        packages = self.client.get_my_consumed_packages(count=1000)
        package_ids = [p.packageId for p in packages]
        self.assertIn(package_id, package_ids)

    def test_get_my_packages_validates_page_size(self):
        with self.assertRaises(ValueError):
            self.client.get_my_packages(count=-1)
        with self.assertRaises(ValueError):
            self.client.get_my_packages(count=0)
        with self.assertRaises(ValueError):
            self.client.get_my_packages(count="test")

    def test_get_my_packages_return_packages(self):
        self.package_id = self.create_package("test_me_functions")
        self.assertGreater(len(self.client.get_my_packages()), 0)
        self.assertEquals(len(self.client.get_my_packages(count=1)), 1)
