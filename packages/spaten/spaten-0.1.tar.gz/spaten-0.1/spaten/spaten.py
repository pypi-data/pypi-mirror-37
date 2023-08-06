import struct
from typing import List

from shapely.wkb import loads

from .fileformat_pb2 import Body


BYTEORDER = 'little'


class Feature(object):
    __slots__ = 'geometry', 'properties'

    def __init__(self, geometry, properties):
        self.geometry = geometry
        self.properties = properties

    def __repr__(self):
        return '{}: ({})'.format(self.geometry.geom_type, self.properties.__repr__())


class File(object):
    vt = {
        0: lambda buf: buf.decode('utf-8'),
        1: lambda buf: int.from_bytes(buf, 'little'),
        2: lambda buf: struct.unpack('d', buf)[0]
    }

    def __init__(self, f):
        """Initialize a Spaten stream. If f is a str, it will be treated as a file
        path, otherwise it will be handled as a stream."""
        self.f = f

    def __enter__(self):
        if isinstance(self.f, str):
            self.r = open(self.f, 'rb')
        self.read_header()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        if hasattr(self.r, 'close'):
            self.r.close()

    def parse_tags(self, tags) -> dict:
        props = {}
        for tag in tags:
            props[tag.key] = self.vt[tag.type](tag.value)
        return props

    def read(self, size: int):
        """Reads the specified number of bytes and checks if EOF has occured"""
        buf = self.r.read(size)
        if len(buf) != size:
            raise EOFError
        return buf

    def read_int(self, size: int) -> int:
        return int.from_bytes(self.read(size), BYTEORDER)

    def read_header(self):
        cookie = self.r.read(4)
        if cookie != b'SPAT':
            raise ValueError('Invalid header')
        version = self.read_int(4)
        if version != 0:
            raise ValueError('The library only supports Spaten version 0')
        return version

    # def write_header(self):

    def read_block(self) -> List[Feature]:
        body_len = self.read_int(4)
        flags = self.read_int(2)
        compression = self.read_int(1)
        message_serialization = self.read_int(1)

        if compression != 0:
            raise AttributeError('compression in Spaten files not supported by library')

        if message_serialization != 0:
            raise AttributeError('non-protobuf Spaten files are not supported')

        bodybuf = self.read(body_len)
        block = Body()
        block.ParseFromString(bodybuf)

        features = []
        for feature in block.feature:
            features.append(Feature(
                geometry=loads(feature.geom),
                properties=self.parse_tags(feature.tags)
            ))
        return features

    def __iter__(self):
        self._rd_buf = []  # type: List[Feature]
        return self

    def __next__(self) -> Feature:
        try:
            if len(self._rd_buf) == 0:
                self._rd_buf = self.read_block()
            return self._rd_buf.pop(0)
        except EOFError:
            raise StopIteration
