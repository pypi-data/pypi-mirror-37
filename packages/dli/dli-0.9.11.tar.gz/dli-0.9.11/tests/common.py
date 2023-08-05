import unittest
import logging
import requests
import json
import os
import datetime
import time
import socket
import s3fs

from six.moves.urllib import parse
from mock import patch
from dli.client import session, builders


logger = logging.getLogger(__name__)
# this token allows us to login when running datacat in dev mode
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImlhdCI6MTUxMzMzMTUwOSwiZXhwIjo5NTEzMzM1MTA5fQ.eyJhdWQiOiJkYXRhbGFrZS1hY2NvdW50cyIsImF1dGhfdGltZSI6MTUxMzMzMTUwOSwiZGF0YWxha2UiOnsiYWNjb3VudHMiOnsiaWJveHgiOiJydyIsIm1yZCI6InIiLCJkYXRhbGFrZS1tZ210IjoicncifX0sImVtYWlsIjoiamltQGV4YW1wbGUuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6OTUxMzMzNTEwOSwiaWF0IjoxNTEzMzMxNTA5LCJpc3MiOiJodHRwczovL2h5ZHJhLWRldi51ZHBtYXJraXQubmV0Iiwibm9uY2UiOiI1YTgyMzI2NC1iN2QzLTQ4NWUtYjc2MS1lYzE1MTI5NDQ4MTQiLCJzdWIiOiJ1c2VyOjEyMzQ1OmppbSJ9.mB9-W8KCyARq5zkLsjSdmE4KKQ7Q7MBvmX5J6rYMMtM"


def build_fake_s3fs(key, secret, token):
    # Nasty: Resolve the hostname so that the we connect
    # using the ip address instead of the hostname
    # this is due a limitation in fake-s3, read more here:
    # https://github.com/jubos/fake-s3/issues/17
    s3_hostname = socket.gethostbyname(os.environ.get("FAKE_S3_HOST", "localhost"))
    s3_port = os.environ.get("FAKE_S3_PORT", 4569)

    return s3fs.S3FileSystem(
        key=key,
        secret=secret,
        token=token,
        client_kwargs={
            "endpoint_url": "http://%s:%s" % (s3_hostname, s3_port)
        }
    )


class SdkIntegrationTestCase(unittest.TestCase):
    """
    Helper TestCase to test against a local docker container running the datacat api.
    To run these locally, run `docker-compose up` on the root directory
    """

    # FIXME
    # -----
    # By now we patch the response to return a token we know will authenticate
    # instead of generating an api key, this isn't ideal as the behaviour is
    # not exactly the same, but it is good enough by now.
    @patch("dli.client.dli_client._get_auth_key", lambda k, r, h: token)
    def setUp(self):
        self.headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(token),
            'Cookie': 'oidc_id_token=' + token
        }
        self.root_url = os.environ.get("DATA_LAKE_INTERFACE_URL", "http://localhost:9000/__api/")
        self.api_key = self.get_api_key()
        self.client = self.create_session()
        self.s3 = []

        # create a fake s3 repo
        self.set_s3_client_mock()

    def set_s3_client_mock(self):
        def _upload(_, files, location, tr=None, r=None):
            result = []
            for f in files:
                path = location + os.path.basename(f)
                self.s3.append(path)
                result.append({"path": "s3://" + path})
            return result

        s3_upload = patch('dli.client.s3.Client.upload_files_to_s3', _upload)
        s3_upload.start()
        s3_download = patch('dli.client.s3.Client.download_file')
        self.s3_download_mock = s3_download.start()

        # cleanup
        self.addCleanup(s3_upload.stop)
        self.addCleanup(s3_download.stop)

    def get_api_key(self):
        # url = "%s/generate-my-key" % self.root_url
        # payload = {
        #     "account": "datalake-mgmt",
        #     "rights": "rw",
        #     "expiration": "2030-01-01"
        # }

        # response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        # return response.text
        return "key"

    def create_package(self, name, access="Restricted"):
        return self.client.register_package(
            name=name + "_" + str(datetime.datetime.now()),
            description="asd",
            publisher="datalake-mgmt",
            manager="datalake-mgmt",
            access_manager="datalake-mgmt",
            tech_data_ops="datalake-mgmt",
            topic="Academic/Education",
            access=access,
            data_source="External",
            data_sensitivity="Public",
            terms_and_conditions="Terms and Conditions"
        ).packageId

    def create_collection(self, name):
        root = self.client.get_root_siren()
        collections = root.collections_root()
        return collections.create_collection(__json={
            "name": name + "_" + str(datetime.datetime.now()),
            "description": "test",
            "managerId": "datalake-mgmt"
        }).collectionId

    def dataset_builder(self, package_id, dataset_name):
        return builders.DatasetBuilder(
            package_id=package_id,
            name=dataset_name,
            description="a testing dataset",
            content_type="Pricing",
            data_format="CSV",
            publishing_frequency="Daily"
        )

    def create_session(self):
        return session.start_session(self.api_key, self.root_url)

    def register_aws_account(self, aws_account_id):
        response = requests.post(
            parse.urljoin(self.root_url, "me/aws-accounts"),
            headers=self.headers,
            data=json.dumps({
                "awsAccountId": str(aws_account_id),
                "awsAccountName": str(aws_account_id),
                "awsAccessKeyId": "accessKey",
                "awsSecretAccessKey": "secretAccessKey",
                "awsRegion": "eu-west-1",
                "accountIds": ["datalake-mgmt"]
            })
        )

        self.assertEqual(response.status_code, 200)


def eventually(assertion, delay=1, retries=5):
    try:
        return assertion()
    except Exception as e:
        if retries <= 1:
            raise e
        time.sleep(delay)
        return eventually(assertion, delay=delay, retries=retries-1)
