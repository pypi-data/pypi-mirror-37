# -*- coding: utf-8 -*-

from tempfile import mkdtemp, mkstemp
from os import fdopen


class TmpFile:

    @staticmethod
    def create(dir=None, filename=None, mode='r'):
        binary = 'b' in mode
        dir = dir or mkdtemp()
        fd, path = filename or mkstemp(dir=dir, text=(not binary))
        return fd, path

    @staticmethod
    def write(fd, data, mode='w'):
        f = fdopen(fd, mode)
        f.write(data)
        f.close()
