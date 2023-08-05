import logging
import datetime
from functools import partial
from unittest import skip
from tests.common import SdkIntegrationTestCase, eventually
from dli.client.exceptions import PackageNotFoundException, NoAccountSpecified, NoPackageIdSpecifiedException


logger = logging.getLogger(__name__)


class PackageFunctionsTestCase(SdkIntegrationTestCase):

    def test_get_unknown_package_raises_package_not_found(self):
        with self.assertRaises(PackageNotFoundException):
            self.client.get_package("unknown")

    def test_get_package_returns_non_siren_response(self):
        package_id = self.create_package(
            name="test_get_package_returns_non_siren_response"
        )
        package = self.client.get_package(package_id)
        self.assertEqual(package.packageId, package_id)

    def test_get_datasets_in_package(self):
        client = self.client
        package_id = self.create_package("test_get_datasets_in_package")
        builder = self.dataset_builder(package_id, "test_package_functions").with_data_lake_storage("foo")
        self.client.register_dataset(builder)

        datasets = client.get_package_datasets(package_id)

        self.assertEqual(len(datasets), 1)

    def test_get_datasets_in_package_with_None_should_be_handled_gracefully(self):
        with self.assertRaises(NoPackageIdSpecifiedException):
            self.client.get_package_datasets(None)

    def test_search(self):
        package_id = self.create_package("searcheable package")
        collection_id = self.create_collection("searcheable collection")

        def entities_are_returned_in_search():
            result = self.client.search("searcheable")
            self.assertTrue(len(result) >= 2)
            self.assertIn(package_id, [p.packageId for p in result if hasattr(p, "packageId")])
            self.assertIn(collection_id, [c.collectionId for c in result if hasattr(c, "collectionId")])

        eventually(entities_are_returned_in_search)
        self.assertEqual(len(self.client.search(term="")), 0)

    def test_search_raises_error_for_invalid_count(self):
        with self.assertRaises(ValueError):
            self.client.search("searcheable", count=-1)

        with self.assertRaises(ValueError):
            self.client.search("searcheable", count=0)

        with self.assertRaises(ValueError):
            self.client.search("searcheable", count="test")

    def test_can_delete_package(self):
        package_id = self.create_package(
            "test_can_delete_package"
        )
        self.client.delete_package(package_id)
        with self.assertRaises(PackageNotFoundException):
            self.client.get_package(package_id)

    def test_delete_unknown_package_raises_exception(self):
        with self.assertRaises(PackageNotFoundException):
            self.client.delete_package("unknown")

    @skip("requires /me")
    def test_get_my_consumed_packages(self):
        package_1 = self.create_package(
            name="test_get_my_consumed_packages"
        )
        package_2 = self.create_package(
            name="test_get_my_consumed_packages"
        )

        packages = self.client.get_my_consumed_packages(count=1000)
        package_ids = [package.id for package in packages]

        self.assertIn(package_1, package_ids)
        self.assertIn(package_2, package_ids)


class RegisterPackageTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super(RegisterPackageTestCase, self).setUp()

        self.create = partial(
            self.client.register_package,
            name="RegisterPackageTestCase" + str(datetime.datetime.now()),
            description="my package description",
            topic="Automotive",
            access="Restricted",
            data_source="Internal",
            data_sensitivity="Public",
            terms_and_conditions="Terms",
            publisher="Bloomberg",
            access_manager="datalake-mgmt",
            tech_data_ops="datalake-mgmt",
            manager="datalake-mgmt"
        )

    def test_can_not_default_accounts_if_api_key_has_multiple_accounts(self):
        with self.assertRaises(NoAccountSpecified):
            self.create(manager=None)

    def test_edit_unknown_package_raises_unknown_package_exception(self):
        with self.assertRaises(PackageNotFoundException):
            self.client.edit_package(package_id="unknown")

    def test_edit_package_allows_changing_single_field(self):
        package = self.create()
        edited = self.client.edit_package(
            package.packageId, description="enhanced description"
        )
        self.assertEqual(edited.packageId, package.packageId)
        self.assertEqual(edited.description, "enhanced description")

        # accounts were not changed
        self.assertEqual(edited.managerId, package.managerId)
        self.assertEqual(edited.techDataOpsId, package.techDataOpsId)
        self.assertEqual(edited.publisher, package.publisher)
        self.assertEqual(edited.accessManagerId, package.accessManagerId)

        # name is still the same
        self.assertEqual(edited.name, package.name)

    def test_edit_can_change_account_ids(self):
        package = self.create()

        edited = self.client.edit_package(
            package.packageId,
            tech_data_ops="iboxx"
        )

        self.assertEqual(edited.packageId, package.packageId)
        self.assertEqual(edited.techDataOpsId, "iboxx")
