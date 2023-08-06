# -*- coding: utf-8 -*-

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property
from s3_local_endpoint import s3_local_endpoint as s3

from urllib.parse import urlparse
import requests
import os

from .files import TmpFile
from django.core.files import File as DjangoNIHFile

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_S3_ENDPOINT_URL = os.environ['AWS_S3_ENDPOINT_URL']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']


class S3FileOpener:

    class File(DjangoNIHFile):
        def close(self):
            super(S3FileOpener.File, self).close()
            os.remove(self.file.name)


    def __init__(self, url, mode=None):
        self.mode = mode or 'r'
        self.request = requests.get(url, allow_redirects=True)
        fd, path = TmpFile.create()
        TmpFile.write(fd, self.request.content, 'wb')
        self.file = self.File(open(path, self.mode))

    def __enter__(self):
        return self.file

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()


@deconstructible
class S3Storage(Storage):

    def __init__(self, bucket=AWS_STORAGE_BUCKET_NAME, overwrite=True):
        """
        " :attr bucket Path to « folder » containing files.
        """
        self.bucket = bucket
        self.client = s3.s3_local_endpoint(
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            AWS_S3_ENDPOINT_URL,
            self.bucket)
        self.overwrite = overwrite

    @cached_property
    def location(self):
        return os.path.join(AWS_S3_ENDPOINT_URL, self.bucket)

    def delete_bucket(self):
        self.client.delete_bucket(self.bucket)

    def delete(self, path):
        assert path, "Path cannot be empty."
        return self.client.delete_file(path)

    def exists(self, path):
        files = self.client.list_files()
        return path in files

    def listdir(self, path=None):
        path = path or ''
        directories, files = [], []
        for f in self.client.list_files():
            if f.startswith(path):
                # list_files doesn't return dirs independantly, ever
                # so we don't have to do something like this, ever:
                # if os.path.isdir(f):
                #   directories.append(f)
                # else:
                files.append(f)
        return directories, files

    def get_available_name(self, name, max_length=None):
        if self.overwrite:
            return name
        return super(S3Storage, self).get_available_name(name, max_length)

    def url(self, name):
        return name

    def _save(self, path, content):
        content.seek(0) # make sure content can be read during upload
        self.client.upload_stream(path, content)
        return self.client.generate_url(path)

    def _open(self, name, mode='rb'):
        if ('w' in mode) or ('+' in mode):
            # writing COULD be done by downloading the file into a TmpFile,
            # then writing in it, then reuploading it at the same url
            # question is : SHOULD it be done ?
            raise AttributeError("Only read operations supported for now.")
        opener = S3FileOpener(name)
        return opener.file

    def upload(self, path):
        f = open(path, 'rb')
        url = self.save(path, f)
        f.close()
        return url
