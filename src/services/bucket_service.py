import boto3
from VLE.config import config
from botocore.exceptions import ClientError

from VLE.settings import BASE_DIR


class Bucket:
    _client = None
    _resource = None

    @classmethod
    def get_resource(cls):
        if cls._resource is None:
            try:
                s3_resource = boto3.resource(
                    config.AWS_SERVICE_NAME,
                    endpoint_url=config.AWS_S3_ENDPOINT_URL,
                    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                )
                cls._resource = s3_resource
            except Exception as exc:
                pass

        return cls._resource

    def upload_file_with_path(self, file_path, object_name, bucket_name=config.AWS_STORAGE_BUCKET_NAME, acl='private'):
        with open(file_path, "rb") as file:
            self.upload_file(file, object_name, bucket_name, acl)

    def upload_file(self, file, object_name, bucket_name=config.AWS_STORAGE_BUCKET_NAME, acl='public-read'):
        try:
            bucket = self.get_resource().Bucket(bucket_name)
            return bucket.put_object(
                ACL=acl,
                Body=file,
                Key=object_name
            )
        except ClientError as e:
            pass

    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                s3_resource = boto3.client(
                    service_name=config.AWS_SERVICE_NAME,
                    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                    endpoint_url=config.AWS_S3_ENDPOINT_URL,
                )
                cls._client = s3_resource
            except Exception as exception:
                pass

        return cls._client

    def get_list_objects(self, bucket_name=config.AWS_STORAGE_BUCKET_NAME):
        client = self.get_client()
        buck = client.list_objects_v2(Bucket=bucket_name)
        keys = []
        for obj in buck['Contents']:
            keys.append(obj)
        return keys

    def delete_object(self, object_name, bucket_name=config.AWS_STORAGE_BUCKET_NAME):
        try:
            client = self.get_client()
            response = client.delete_object(Bucket=bucket_name, Key=object_name)
        except Exception as exception:
            pass
        else:
            return response

    def download_obj(self, object_name, bucket_name=config.AWS_STORAGE_BUCKET_NAME):
        with open(object_name, 'wb') as f:
            client = self.get_client()
            client.download_fileobj(bucket_name, object_name, f)
            return BASE_DIR.__str__() + '/' + object_name


bucket = Bucket()
