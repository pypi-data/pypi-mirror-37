# -*- coding: utf-8 -*-

import unittest
from .. import unis3
from os.path import realpath, dirname
from django.core.files.base import ContentFile
from tempfile import NamedTemporaryFile
from django.core.files import File
from ..files import TmpFile


class UniS3TestCase(unittest.TestCase):
    """
    " Unit tests for the unis3 wrapper.
    """

    def setUp(self):
        self.storage = unis3.S3Storage('unittest')
        # file for testing : this file
        self.tst_path = realpath(__file__)
        self.src_path = realpath(unis3.__file__)
        self.ext_path = realpath(unittest.__file__)
        self.current_dir = dirname(self.tst_path)
        self.parent_dir = dirname(self.current_dir)
        self.src_url = self.storage.upload(self.src_path)
        self.tst_url = self.storage.upload(self.tst_path)
        self.ext_url = self.storage.upload(self.ext_path)

    def tearDown(self):
        for f in self.storage.listdir()[1]:
            self.storage.delete(f)
        self.storage.delete_bucket()

    def test_bucket_name(self):
        self.assertEqual('unittest', self.storage.bucket)

    def test_bucket_location(self):
        expected = 'https://s3.unistra.fr/unittest'
        self.assertEqual(expected, self.storage.location)

    def test_exists(self):
        self.assertTrue(self.storage.exists(self.tst_path))
        self.assertTrue(self.storage.exists(self.src_path))
        self.assertTrue(self.storage.exists(self.ext_path))

    def test_urls(self):
        self.assertEqual(self.tst_url, self.storage.url(self.tst_url))
        self.assertEqual(self.src_url, self.storage.url(self.src_url))
        self.assertEqual(self.ext_url, self.storage.url(self.ext_url))

    def test_list_dir_from_root(self):
        directories, files = self.storage.listdir()
        self.assertEqual(len(directories), 0)
        self.assertEqual(len(files), 3)
        self.assertTrue(self.tst_path in files)
        self.assertTrue(self.src_path in files)
        self.assertTrue(self.ext_path in files)

    def test_list_dir_from_current_dir(self):
        directories, files = self.storage.listdir(self.current_dir)
        self.assertEqual(len(directories), 0)
        self.assertEqual(len(files), 1)
        self.assertTrue(self.tst_path in files)
        self.assertFalse(self.src_path in files)
        self.assertFalse(self.ext_path in files)

    def test_list_dir_from_parent_dir(self):
        directories, files = self.storage.listdir(self.parent_dir)
        self.assertEqual(len(directories), 0)
        self.assertEqual(len(files), 2)
        self.assertTrue(self.tst_path in files)
        self.assertTrue(self.src_path in files)
        self.assertFalse(self.ext_path in files)

    def test_reupload(self):
        self.assertEqual(len(self.storage.listdir()[1]), 3)
        self.src_url = self.storage.upload(self.src_path)
        self.tst_url = self.storage.upload(self.tst_path)
        self.ext_url = self.storage.upload(self.ext_path)
        self.assertEqual(len(self.storage.listdir()[1]), 3)

    def test_delete(self):
        self.assertTrue(self.storage.exists(self.tst_path))
        self.assertTrue(self.storage.exists(self.src_path))

        res = self.storage.delete(self.src_path)
        self.assertTrue(res)
        self.assertTrue(self.storage.exists(self.tst_path))
        self.assertFalse(self.storage.exists(self.src_path))
        self.assertEqual(len(self.storage.listdir()[1]), 2) # tst and ext remain

        res = self.storage.delete(self.tst_path)
        self.assertTrue(res)
        self.assertFalse(self.storage.exists(self.tst_path))
        self.assertFalse(self.storage.exists(self.src_path))
        self.assertEqual(len(self.storage.listdir()[1]), 1) # only ext remains

    def test_delete_nonexistent(self):
        path = 'non/existent/path'
        self.assertFalse(self.storage.exists(path))
        directories, files = self.storage.listdir(self.current_dir) # before
        res = self.storage.delete(path)
        self.assertTrue(res) # deleting unexistent stuff always successes
        d, f = self.storage.listdir(self.current_dir) # after
        self.assertEqual(len(d), len(directories))
        self.assertEqual(len(f), len(files))

    def test_available_name_overwrite_mode(self):
        self.storage.overwrite = True
        name = self.storage.get_available_name(self.src_path)
        self.assertEqual(self.src_path, name)

    def test_available_name_no_overwrite(self):
        self.storage.overwrite = False
        name = self.storage.get_available_name(self.src_path)
        self.assertGreater(len(name), len(self.src_path))
        common_part = self.src_path[:-len('.py')]
        self.assertTrue(name.startswith(common_part))

    def test_open(self):
        f = self.storage.open(self.src_url)
        self.assertGreater(len(f.read()), 0)
        f.close()

    def test_open_write_mode_failure(self):
        with self.assertRaises(AttributeError) as context:
            self.storage.open(self.src_url, 'w')
        self.assertTrue("Only read operations" in str(context.exception))
        with self.assertRaises(AttributeError) as context:
            self.storage.open(self.src_url, 'r+')
        self.assertTrue("Only read operations" in str(context.exception))
        with self.assertRaises(AttributeError) as context:
            self.storage.open(self.src_url, 'w+')
        self.assertTrue("Only read operations" in str(context.exception))

    def test_read(self):
        with open(self.src_path) as f:
            before = f.read()
        with unis3.S3FileOpener(self.src_url, 'r') as f:
            after = f.read()
        self.assertEqual(after, before)

    def test_overwrite(self):
        before = 'whatever'
        fd, path = TmpFile.create()
        TmpFile.write(fd, before)
        file = File(open(path, 'rb'))
        url = self.storage.save(path, file)
        file.close()

        with unis3.S3FileOpener(url, 'r') as f:
            data = f.read()
            self.assertEqual(data, before)

        self.assertTrue(self.storage.overwrite)

        after = 'tu peux pas test'
        fd2, path2 = TmpFile.create()
        TmpFile.write(fd2, after)
        f2 = File(open(path2, 'rb'))
        url2 = self.storage.save(path, f2) # path, NOT path2 (overwrite)
        f2.close()
        end_of_common_prefix = 'Signature='
        index = url.find(end_of_common_prefix)+len(end_of_common_prefix)
        self.assertEqual(url2[:index], url[:index])
        with unis3.S3FileOpener(url, 'r') as f:
            data = f.read()
            self.assertEqual(data, after)
        self.assertNotEqual(after, before)
