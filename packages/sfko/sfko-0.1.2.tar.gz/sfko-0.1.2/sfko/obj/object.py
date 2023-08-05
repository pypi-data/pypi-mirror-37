import uuid

from ..util.conf import config
from ..util.parse import parse_filesize


class FakeFile:
    def __init__(self, size, content = b'0'):
        self._size = size
        self._pos = 0
        self._content = bytes(content)

    def _readbytes(self, num):
        self._pos += num
        return self._content * num

    def read(self, num = -1):
        if num == -1:
            return self._readbytes(self._size)
        if self._pos == self._size:
            return bytes()
        elif self._size < self._pos + num:
            return self._readbytes(self._size - self._pos)
        return self._readbytes(num)

    def seek(self, offset, from_what = 0):
        if from_what == 0:
            self._pos = offset
        elif from_what == 1:
            self._pos += offset
        elif from_what == 2:
            self._pos = self._size - offset
        return self._pos

    def tell(self):
        return self._pos

    def close(self):
        pass

class ObjectProxy:
    def __init__(self, resource, bucket, count = None, size = None, prefix = None):
        self._count = count if count else config.objects.default.count
        size = size if size is not None else config.objects.default.size
        self._size = parse_filesize(size)
        self._prefix = prefix
        self._resource = resource
        self._bucket = bucket
        self._objects = []

    def _name(self):
        if self._prefix:
            return '%s/%s'%(self._prefix, uuid.uuid4().hex)
        return uuid.uuid4().hex

    def _file(self):
        return FakeFile(self._size)

    def __iter__(self):
        for i in range(self._count):
            name = self._name()
            obj = self._resource.Object(self._bucket, name)
            self._objects.append(name)
            yield obj, self._file()

    @property
    def objects(self):
        for o in self._objects:
            yield self._bucket, o

    @property
    def raw(self):
        for obj, data in self:
            yield self._bucket, obj.key, self._size

    @property
    def resource(self):
        return self._resource

    @property
    def client(self):
        return self._resource.meta.client

class FakeObjectProxy:
    def __init__(self, resource, bucket, key, size):
        self._resource = resource
        self._bucket = bucket
        self._key = key
        self._size = size
        self._objects = ['%s/%s'%(bucket, key)]

    def __iter__(self):
        yield self._resource.Object(self._bucket, self._key), FakeFile(self._size)

    @property
    def raw(self):
        yield self._bucket, self._key, self._size

    @property
    def resource(self):
        return self._resource

    @property
    def client(self):
        return self._resource.meta.client
