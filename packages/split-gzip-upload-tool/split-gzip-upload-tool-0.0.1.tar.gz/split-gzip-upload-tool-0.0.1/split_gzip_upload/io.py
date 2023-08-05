import gzip
import io
import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger('split_gzip_upload.io')


class StreamCompressorBase(metaclass=ABCMeta):

    def __init__(self, encoding='utf-8', compression_level=5):
        self.stream = io.BytesIO()
        self.compressor = self.create_compressor(compression_level)
        self.wrapper = io.TextIOWrapper(self.compressor, encoding=encoding)

    @abstractmethod
    def create_compressor(self, compression_level):
        raise NotImplementedError()

    def writelines(self, lines):
        self.wrapper.writelines(lines)

    def finalize(self):
        self.wrapper.close()
        self.compressor.close()
        # self.stream.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finalize()


class GzipCompressedStream(StreamCompressorBase):

    def create_compressor(self, compression_level):
        return gzip.GzipFile(fileobj=self.stream, mode='wb+', compresslevel=compression_level)
