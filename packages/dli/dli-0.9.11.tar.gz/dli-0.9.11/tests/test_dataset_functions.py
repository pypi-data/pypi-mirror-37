import logging
import os

import six

from backports import tempfile
from .common import SdkIntegrationTestCase
from unittest import skip
from mock import patch, call

from dli.client import utils, builders

from dli.client.exceptions import (
    PackageNotFoundException,
    InvalidPayloadException,
    DatasetNotFoundException,
    DownloadFailed
)


logger = logging.getLogger(__name__)


class DatasetFunctionsTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super(DatasetFunctionsTestCase, self).setUp()

        self.package_id = self.create_package("test_dataset_functions")
        self.builder = self.dataset_builder(self.package_id, "test_dataset_functions")

    def test_get_unknown_dataset_returns_none(self):
        self.assertIsNone(self.client.get_dataset("unknown"))

    def test_can_get_existing_dataset(self):
        builder = self.builder.with_external_storage(
            location="jdbc://connectionstring:1232/my-db"
        )
        expected = self.client.register_dataset(builder)
        actual = self.client.get_dataset(expected.datasetId)

        self.assertEqual(expected, actual)

    def test_retrieve_keys_for_unknown_dataset_raises_error(self):
        with self.assertRaises(DatasetNotFoundException):
            self.client.get_s3_access_keys_for_dataset("unknown")

    def test_can_retrieve_keys_for_dataset(self):
        builder = self.builder.with_data_lake_storage("my-happy-bucket")
        dataset = self.client.register_dataset(builder)
        keys = self.client.get_s3_access_keys_for_dataset(dataset.datasetId)

        self.assertEqual(dataset.datasetId, keys["datasetId"])

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
        self.assertEqual(dataset.location["type"], "Other")

    def test_can_create_dataset_with_external_bucket(self):
        # we need an aws account present first
        aws_account_id = 12345679
        self.register_aws_account(aws_account_id)

        # create a package with the external account
        builder = self.builder.with_external_s3_storage(
            bucket_name="my-happy-external-bucket",
            aws_account_id=aws_account_id
        )

        dataset = self.client.register_dataset(builder)
        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.location["type"], "S3")
        self.assertEqual(dataset.location["bucket"], "my-happy-external-bucket")

    def test_can_create_dataset_with_data_lake_bucket(self):
        builder = self.builder.with_data_lake_storage("my-happy-bucket")
        dataset = self.client.register_dataset(builder)

        self.assertIsNotNone(dataset)
        self.assertEqual(dataset.location["type"], "S3")
        self.assertEqual(dataset.location["bucket"], "dev-ihsm-dl-pkg-my-happy-bucket")

    def test_can_edit_dataset_with_same_values(self):
        builder = self.builder.with_data_lake_storage("my-happy-bucket")
        dataset = self.client.register_dataset(builder)

        updated = self.client.edit_dataset(
            dataset.datasetId,
            name=dataset.name,
            description=dataset.description,
            content_type=dataset.contentType,
            data_format=dataset.dataFormat["type"]
        )

        self.assertEqual(dataset.datasetId, updated.datasetId)
        self.assertEqual(dataset.packageId, updated.packageId)
        self.assertEqual(dataset.name, updated.name)
        self.assertEqual(dataset.location, updated.location)
        self.assertEqual(dataset.createdAt, updated.createdAt)
        # updated has changed
        self.assertNotEqual(dataset.updatedAt, updated.updatedAt)

    def test_can_edit_and_change_values(self):
        builder = self.builder.with_data_lake_storage("my-happy-bucket")
        dataset = self.client.register_dataset(builder)

        updated = self.client.edit_dataset(
            dataset.datasetId,
            description="new desc",
            content_type="content type",
            keywords=["test", "2"]
        )

        self.assertEqual(updated.datasetId, dataset.datasetId)
        self.assertEqual(updated.packageId, dataset.packageId)
        self.assertEqual(updated.name, dataset.name)
        self.assertEqual(updated.description, "new desc")
        self.assertEqual(updated.contentType, "content type")
        self.assertEqual(updated.keywords, ["test", "2"])

    def test_can_delete_dataset(self):
        builder = self.builder.with_data_lake_storage("my-happy-bucket")
        dataset = self.client.register_dataset(builder)

        # delete
        self.client.delete_dataset(dataset.datasetId)

        self.assertIsNone(self.client.get_dataset(dataset.datasetId))

    def test_delete_unknown_dataset_raises_error(self):
        with self.assertRaises(DatasetNotFoundException):
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
        builder = builder.with_data_lake_storage("my-happy-bucket")

        with self.assertRaises(PackageNotFoundException):
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
        datafiles = self.client.get_datafiles(dataset.datasetId)
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
                dataset.datasetId,
                "datafile %s" % i,
                files
            )

        datafiles = self.client.get_datafiles(dataset.datasetId)
        self.assertEqual(len(datafiles), 3)

        datafiles_paged = self.client.get_datafiles(dataset.datasetId, count=2)
        self.assertEqual(len(datafiles_paged), 2)

    def test_get_dataset_datafiles_raises_error_for_invalid_count(self):
        with self.assertRaises(ValueError):
            self.client.get_datafiles("some_dataset", count=-1)

        with self.assertRaises(ValueError):
            self.client.get_datafiles("some_dataset", count=0)

        with self.assertRaises(ValueError):
            self.client.get_datafiles("some_dataset", count="test")
