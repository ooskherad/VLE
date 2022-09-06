from datetime import datetime
import hashlib

from services.bucket_service import bucket
from home.models import Files, FileGroup


class FileUploadException(Exception):
    pass


class FileService:
    def __init__(self, file, file_name, user, group_file):
        self.file = file
        self.file_name = file_name
        self.user = user
        self.upload_data = None
        self.group_file = group_file

    def upload_and_save(self):
        file = self.upload_file()
        return self.save_in_files(file.key)

    def upload_file(self):
        name = self.make_obj_name
        file = bucket.upload_file(file=self.file, object_name=name)
        self.upload_data = file.get()
        return file

    def save_in_files(self, title):
        if self.successful_update:
            return Files.objects.create(
                type=self.file_content_type,  # todo: must in enum
                format=self.file_format,
                title=title,
                size=self.file_size,
                created_by=self.user,
                group_id=self.group_file,
            )
        raise FileUploadException(
            f"error during upload file \n {self.upload_data['ResponseMetadata']['HTTPStatusCode']}")

    @property
    def file_size(self):
        return self.upload_data['ResponseMetadata']['HTTPHeaders']['content-length']

    @property
    def file_content_type(self):
        return self.upload_data['ResponseMetadata']['HTTPHeaders']['content-type']

    @property
    def successful_update(self):
        return True if self.upload_data['ResponseMetadata']['HTTPStatusCode'] == 200 else False

    @property
    def file_format(self):
        return self.file_name[self.file_name.find('.') + 1:]

    @property
    def make_obj_name(self):
        salt = datetime.now().__str__()
        new_name = self.file_name + salt
        return hashlib.md5(new_name.encode()).hexdigest() + '.' + self.file_format
