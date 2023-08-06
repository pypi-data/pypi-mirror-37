import requests
import boto3
import os


class Vault:

    def __init__(self,
                 bucket,
                 owner_id,
                 collection,
                 aws_access_key_id=None,
                 aws_secret_access_key=None,
                 aws_s3_region_name=None
                 ):
        if aws_access_key_id is None:
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        if aws_secret_access_key is None:
            aws_access_key_id = os.environ.get('AWS_SECRET_ACCESS_KEY')
        if aws_s3_region_name is None:
            aws_access_key_id = os.environ.get('AWS_S3_REGION_NAME')
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_s3_region_name
        )
        self.bucket = bucket
        self.owner_id = owner_id
        self.collection = collection

    def __key(self, object_id):
        return '{}/{}/{}.pdf'.format(
            self.collection,
            self.owner_id,
            object_id
        )

    def create_bucket(self):
        """
        If bucket doesn't exist, create it with the correct settings
        """
        pass

    def upload_from_url(self, url, filename):
        res = requests.get(url)
        if res.ok:
            bucket = self.bucket
            # self.client.meta.client.upload_fileobj(res.content, bucket, 'hello.txt')
            self.client.put_object(
                Bucket=self.bucket,
                Key=filename,
                Body=res.content,
                ContentType='application/pdf',
                ACL='private',
                ServerSideEncryption='AES256'
            )
        else:
            error_message = 'HTTP request failed with status: {}'.format(res.status_code)
            raise Exception(error_message)

    def get_url(self, object_id, version_id=None, expires=3600):
        params = {'Bucket': self.bucket, 'Key': self.__key(object_id)}
        if version_id is not None:
            params['VersionId'] = version_id
        return self.client.generate_presigned_url(
            'get_object',
            Params = params,
            ExpiresIn = expires
        )

    def get_object(self, object_id):
        key = self.__key(object_id)
        return self.client.get_object(Bucket=self.bucket, Key=key)

    def get_versions(self, object_id):
        key = self.__key(object_id)
        return self.client.list_object_versions(Bucket=self.bucket, Prefix=key)
