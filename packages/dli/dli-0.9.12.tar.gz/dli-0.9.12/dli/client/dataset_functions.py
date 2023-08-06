
import logging
import os
import six

from dli.siren import siren_to_entity, siren_to_dict
from dli.client import utils
from dli.client.exceptions import CatalogueEntityNotFoundException

logger = logging.getLogger(__name__)


class DatasetFunctions(object):

    @property
    def __root(self):
        return self.get_root_siren().datasets_root()

    def get_s3_access_keys_for_dataset(self, dataset_id, use_cached=False):
        """
        Retrieve S3 access keys for the specified account to access the
        specified package. The retrieved keys and session token will be stored
        in the client context.

        :param str dataset_id: The id of the dataset.
        :param bool refresh: Optional flag to force refresh the token.

        :returns: A dictionary containing the AWS keys, dataset id and session
                token. For example:


                .. code-block:: python

                    {
                       "datasetId": "d0b545dd-83ee-4293-8dc7-5d0607bd6b10",
                       "accessKeyId": "39D19A440AFE452B9",
                       "secretAccessKey": "F426A93CDECE45C9BFF8F4F19DA5CB81",
                       "sessionToken": "C0CC405803F244CA99999"
                    }
        """
        if dataset_id in self.ctx.s3_keys and use_cached:
            return self.ctx.s3_keys[dataset_id]

        # otherwise we go and attempt to fetch one from the API
        dataset = self._get_dataset(dataset_id)
        if not dataset:
            raise CatalogueEntityNotFoundException('Dataset', id=dataset_id)

        keys = dataset.request_access_keys()
        val = {
            "accessKeyId": keys.accessKeyId,
            "datasetId": keys.datasetId,
            "secretAccessKey": keys.secretAccessKey,
            "sessionToken": keys.sessionToken
        }

        # cache the key for future usages
        self.ctx.s3_keys[dataset_id] = val
        return val

    def get_dataset(self, dataset_id):
        """
        Retrieves a dataset (or `None` if it doesn't exist).

        :param str dataset_id: The id of the dataset to retrieve.

        :returns: The dataset.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                dataset = client.get_dataset(dataset_id)
        """
        p = self._get_dataset(dataset_id)
        if not p:
            logger.warn("No dataset found with id `%s`", dataset_id)
            return

        return siren_to_entity(p)

    def register_dataset(self, builder):
        """
        Submit a request to create a new dataset under a specified package in the Data Catalogue.

        :param dli.client.builders.DatasetBuilder builder: An instance of DatasetBuilder. This builder object sets sensible defaults and exposes
                                                           helper methods on how to configure its storage options.

        :returns: A newly created Dataset.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # Please refer to builder docs for examples on
                # how to creata an instance of DatasetBuilder.

                dataset = client.register_dataset(builder)
        """
        payload = builder.build()
        package_id = payload["packageId"]
        if not self._get_package(package_id):
            raise CatalogueEntityNotFoundException('Package', id=package_id)

        result = self.__root.create_dataset(__json=payload)
        return siren_to_entity(result)

    def edit_dataset(
        self,
        dataset_id,
        name=None,
        description=None,
        content_type=None,
        data_format=None,
        publishing_frequency=None,
        keywords=None,
        naming_convention=None,
        documentation=None
    ):
        """
        Updates information on a dataset, returning the updated instance.
        Fields that are left as ``None`` will not be changed.

        :param str dataset_id: Id of the dataset being updated.
        :param str name: A descriptive name of a dataset. It should be unique within the package.
        :param str description: A short description of a package.
        :param str content_type: A way for the data steward to classify the type of data in the dataset (e.g. pricing).
        :param str data_format: The format of the data: csv, parquet, etc.
        :param str publishing_frequency: The internal on which data is published (e.g. daily, monthly, etc.).
        :param list[str] keywords: User-defined list of keywords that can be used to find this dataset through the search interface.
        :param str naming_convention: Key for how to read the dataset name.
        :param str documentation: Documentation about this dataset in markdown format.

        :returns: Updated Dataset.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                updated_dataset = client.edit_dataset(
                    "my-dataset-id",
                    description="Updated my dataset description"
                )
        """
        dataset = self._get_dataset(dataset_id)
        if not dataset:
            raise CatalogueEntityNotFoundException('Dataset', id=dataset_id)

        fields = {
            "packageId": dataset.packageId,
            "name": name,
            "description": description,
            "keywords": keywords,
            "contentType": content_type,
            "location": dataset.location,
            "dataFormat": {"type": data_format} if data_format else None,
            "publishingFrequency": publishing_frequency,
            "namingConvention": naming_convention,
            "documentation": documentation
        }

        # clean up any unknown fields, and update the entity
        dataset_as_dict = siren_to_dict(dataset)
        for key in list(dataset_as_dict.keys()):
            if key not in fields:
                del dataset_as_dict[key]

        payload = {k: v for k, v in fields.items() if v is not None}
        dataset_as_dict.update(payload)

        # perform the update and return the resulting entity
        return siren_to_entity(dataset.edit_dataset(__json=dataset_as_dict))

    def delete_dataset(self, dataset_id):
        """
        Marks a particular dataset (and all its datafiles) as deleted.
        This dataset will no longer be accessible by consumers.

        :param str dataset_id: The id of the dataset to be deleted.

        :returns:

        - **Sample**

        .. code-block:: python

                client.delete_dataset(dataset_id)

        """
        dataset = self._get_dataset(dataset_id)
        if not dataset:
            raise CatalogueEntityNotFoundException('Dataset', id=dataset_id)

        dataset.delete_dataset()

    def _get_dataset(self, dataset_id):
        return self.__root.get_dataset(dataset_id=dataset_id)

    def get_datafiles(self, dataset_id, name_contains=None, as_of_date_start=None, as_of_date_end=None, count=100):
        """
        Returns a list of all datafiles registered under a dataset.

        :param str dataset_id: The id of the dataset.
        :param str name_contains: Optional. Look up only those datafiles for the dataset where name contains this string.
        :param str as_of_date_start: Optional. Datafiles having data_as_of date greater than or equal to this date. This must be specified in YYYY-MM-DD format.
        :param str as_of_date_end: Optional. Datafiles having data_as_of date less than or equal to this date. This must be specified in YYYY-MM-DD format.
        :param int count: Optional count of datafiles to be returned. Defaulted to 100.

        :returns: List of all datafiles registered under the dataset.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                datafiles = client.get_datafiles(
                    dataset_id,
                    name_contains='My Test Data',
                    as_of_date_start='2018-10-11',
                    as_of_date_end='2018-10-15',                    
                    count=10
                )
        """
        utils.ensure_count_is_valid(count)

        params = {
            'name': name_contains,
            'as_of_date_start': as_of_date_start,
            'as_of_date_end': as_of_date_end,
            'page_size': count
        }

        query_params = {k: v for k, v in six.iteritems(params) if v is not None}

        dataset = self._get_dataset(dataset_id)
        if not dataset:
            raise CatalogueEntityNotFoundException('Dataset', id=dataset_id)
            
        datafiles = dataset.get_datafiles(**query_params).get_entities(rel="datafile")

        return [siren_to_entity(df) for df in datafiles]
