import logging
import six

from .common import SdkIntegrationTestCase
from dli.client import builders
from dli.client.exceptions import (
    CatalogueEntityNotFoundException,
    DownloadFailed,
    InvalidPayloadException,
)


class DatasetFunctionsTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super(DatasetFunctionsTestCase, self).setUp()

        self.package_id = self.create_package("test_dataset_functions")
        self.builder = self.dataset_builder(self.package_id, "test_dataset_functions")

    def create_datalake_dataset(self):
        return self.register_s3_dataset(
            package_id=self.package_id,
            dataset_name="test_dataset_functions",
            bucket_name="my-happy-bucket"
        )

    def test_get_unknown_dataset_returns_none(self):
        self.assertIsNone(self.client.get_dataset("unknown"))

    def test_can_get_existing_dataset(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        expected = self.client.register_dataset(builder)
        actual = self.client.get_dataset(expected.dataset_id)

        self.assertEqual(expected, actual)

    def test_retrieve_keys_for_unknown_dataset_raises_error(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_s3_access_keys_for_dataset("unknown")

    def test_can_retrieve_keys_for_dataset(self):
        dataset = self.create_datalake_dataset()
        keys = self.client.get_s3_access_keys_for_dataset(dataset.dataset_id)

        self.assertEqual(dataset.dataset_id, keys["datasetId"])

    def test_can_retrieve_cached_keys_for_dataset(self):
        dataset = self.create_datalake_dataset()
        keys = self.client.get_s3_access_keys_for_dataset(dataset.dataset_id)
        cached_keys = self.client.get_s3_access_keys_for_dataset(dataset.dataset_id, use_cached=True)

        self.assertDictEqual(keys, cached_keys)

    def test_can_not_create_dataset_without_location(self):
        with self.assertRaises(Exception):
            self.client.register_dataset(self.builder)

    def test_can_create_dataset_with_other_location(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        dataset = self.client.register_dataset(builder)

        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.description, self.builder.payload["description"])
        self.assertEqual(dataset.location.type, "Other")

    def test_can_create_dataset_with_external_bucket(self):
        # create a package with the external account
        builder = self.builder.with_external_s3_storage(
            bucket_name="my-happy-external-bucket",
            aws_account_id=self.aws_account_id,
            prefix="/"
        )

        dataset = self.client.register_dataset(builder)
        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.location.type, "S3")
        self.assertEqual(dataset.location.bucket, "my-happy-external-bucket")

    def test_can_edit_dataset_with_same_values(self):
        dataset = self.create_datalake_dataset()

        updated = self.client.edit_dataset(
            dataset.dataset_id,
            name=dataset.name,
            description=dataset.description,
            content_type=dataset.content_type,
            data_format=dataset.data_format.type
        )

        self.assertEqual(dataset.dataset_id, updated.dataset_id)
        self.assertEqual(dataset.package_id, updated.package_id)
        self.assertEqual(dataset.name, updated.name)
        self.assertEqual(dataset.location, updated.location)
        self.assertEqual(dataset.created_at, updated.created_at)
        # updated has changed
        self.assertNotEqual(dataset.updated_at, updated.updated_at)

    def test_can_edit_and_change_values(self):
        dataset = self.create_datalake_dataset()
        
        updated = self.client.edit_dataset(
            dataset.dataset_id,
            description="new desc",
            content_type="content type",
            keywords=["test", "2"]
        )

        self.assertEqual(updated.dataset_id, dataset.dataset_id)
        self.assertEqual(updated.package_id, dataset.package_id)
        self.assertEqual(updated.name, dataset.name)
        self.assertEqual(updated.description, "new desc")
        self.assertEqual(updated.content_type, "content type")
        self.assertEqual(updated.keywords, ["test", "2"])

    def test_can_delete_dataset(self):
        dataset = self.create_datalake_dataset()
        # delete
        self.client.delete_dataset(dataset.dataset_id)
        self.assertIsNone(self.client.get_dataset(dataset.dataset_id))

    def test_delete_unknown_dataset_raises_error(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_dataset("unknown")

    def test_register_dataset_in_unknown_package_raises_error(self):
        builder = builders.DatasetBuilder(
            package_id="unknown",
            name="test",
            description="a testing dataset",
            content_type="Pricing",
            data_format="CSV",
            publishing_frequency="Daily"
        )
        builder = builder.with_external_storage("s3://my-happy-bucket")

        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.register_dataset(builder)


class DatasetDatafilesTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super(DatasetDatafilesTestCase, self).setUp()

    def test_get_dataset_datafiles_raises_exception_if_dataset_does_not_exists(self):
        with self.assertRaises(Exception):
            self.client.get_datafiles("unknown")

    def test_get_dataset_datafiles_returns_empty_when_no_datafiles(self):
        package_id = self.create_package(
            name="test_get_dataset_datafiles_returns_empty_when_no_datafiles"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_dataset_datafiles_returns_empty_when_no_datafiles"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )
        datafiles = self.client.get_datafiles(dataset.dataset_id)
        self.assertEqual(datafiles, [])

    def test_get_dataset_datafiles_returns_datafiles_for_dataset(self):
        files = [{'path': "/path/to/file/A", 'size': 99999}, {'path': "/path/to/file/B", 'size': 88888}]
        package_id = self.create_package(
            name="test_get_dataset_datafiles_returns_datafiles_for_dataset"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_dataset_datafiles_returns_datafiles_for_dataset"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )

        for i in range(1, 4):
            self.client.register_datafile_metadata(
                dataset.dataset_id,
                "datafile %s" % i,
                files,
                data_as_of="2018-10-1%s" % i
            )

        datafiles = self.client.get_datafiles(dataset.dataset_id)
        self.assertEqual(len(datafiles), 3)

        datafiles_paged = self.client.get_datafiles(dataset.dataset_id, count=2)
        self.assertEqual(len(datafiles_paged), 2)

        # Other Lookup scenarios
        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, as_of_date_start='2018-10-12')
        self.assertEqual(len(datafiles_search_by_as_of_date), 2)
        self.assertTrue(all(df.name in ["datafile 2", "datafile 3"] for df in datafiles_search_by_as_of_date))

        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, as_of_date_end='2018-10-12')
        self.assertEqual(len(datafiles_search_by_as_of_date), 2)
        self.assertTrue(all(df.name in ["datafile 1", "datafile 2"] for df in datafiles_search_by_as_of_date))

        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, as_of_date_start='2018-10-10', as_of_date_end='2018-10-11')
        self.assertEqual(len(datafiles_search_by_as_of_date), 1)
        self.assertTrue(all(df.name == "datafile 1" for df in datafiles_search_by_as_of_date))

        datafiles_search_by_as_of_date = self.client.get_datafiles(dataset.dataset_id, name_contains='datafile 2', as_of_date_start='2018-10-10', as_of_date_end='2018-10-13')
        self.assertEqual(len(datafiles_search_by_as_of_date), 1)
        self.assertTrue(all(df.name == "datafile 2" for df in datafiles_search_by_as_of_date))

    def test_get_dataset_datafiles_raises_exception_for_invalid_as_of_date_params(self):
        package_id = self.create_package(
            name="test_get_dataset_datafiles_raises_exception_for_invalid_as_of_date_params"
        )
        dataset = self.client.register_dataset(
            self.dataset_builder(
                package_id,
                "test_get_dataset_datafiles_raises_exception_for_invalid_as_of_date_params"
            ).with_external_storage(location="jdbc://connectionstring:1232/my-db")
        )

        with self.assertRaises(InvalidPayloadException):
            self.client.get_datafiles(dataset.dataset_id, as_of_date_end='blah blah')
            self.client.get_datafiles(dataset.dataset_id, as_of_date_start='blah blah')
            self.client.get_datafiles(dataset.dataset_id, as_of_date_start='11/12/2017', as_of_date_end='15/12/2017')

    def test_get_dataset_datafiles_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.get_datafiles("some_dataset", count=c))
