from s3vault.vault import Vault
from unittest.mock import patch
from unittest import TestCase
import responses


class VaultTestCase(TestCase):

    @patch('boto3.client')
    def setUp(self, mock_client):
        self.object_id = 3656
        self.vault = Vault(
            "s3vault-test",
            1,
            'invoices',
            aws_access_key_id="12345",
            aws_secret_access_key="12345",
            aws_s3_region_name="eu-central-1"
        )

    def test_get_url(self):
        res = self.vault.get_url(self.object_id)

    def test_get_versions(self):
        res = self.vault.get_versions(self.object_id)

        versions = res.get('Versions', [])
        [self.vault.get_url(
            self.object_id,
            version_id=version.get('VersionId')
        ) for version in versions]

    @patch('boto3.client')
    @responses.activate
    def test_put_object(self, mock_put_object):
        mock_put_object.put_object = True
        url = "http://kmmc.in/wp-content/uploads/2014/01/lesson2.pdf"
        responses.add(
            responses.GET,
            url,
            status=200
        )

        self.vault.upload_from_url(
            url,
            "invoice"
        )
