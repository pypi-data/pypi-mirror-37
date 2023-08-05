import logging
import threading

import boto3

logger = logging.getLogger('split_gzip_upload.s3')


class S3MultipartUpload:
    MIN_PART_SIZE_BYTES = 5 * 1024 * 1024

    def __init__(self, bucket, key, compressed_stream, session):
        logger.info('Initializing S3MultipartUpload for {}'.format(key))
        self._compressed = compressed_stream
        self._bucket = bucket
        self._key = key
        self._parts = []
        self._client = session or boto3.client('s3')
        self._mpu_id = None
        self._create_multipart_upload()
        self._lock = threading.Lock()
        self.uploaded_bytes = 0

    def writelines(self, lines):
        with self._lock:
            logger.info('Wrote {} lines to {}'.format(len(lines), self._key))
            self._compressed.writelines(lines)
            if self.can_upload():
                self.upload_data()

    def _create_multipart_upload(self):
        mpu = self._client.create_multipart_upload(Bucket=self._bucket, Key=self._key)
        mpu_id = mpu['UploadId']
        logger.info('Created multipart upload {}'.format(mpu_id))
        self._mpu_id = mpu_id

    def can_upload(self):
        return self._compressed.stream.tell() >= self.MIN_PART_SIZE_BYTES

    def upload_data(self):
        part_num = len(self._parts) + 1

        stream = self._compressed.stream
        len_data = stream.tell()
        stream.seek(0)
        logger.info('Started uploading {} bytes to {}'.format(len_data, self._key))
        part = self._client.upload_part(
            Body=stream,
            Bucket=self._bucket,
            Key=self._key,
            UploadId=self._mpu_id,
            PartNumber=part_num
        )
        logger.info('Uploaded {} bytes to {}'.format(len_data, self._key))
        self.uploaded_bytes += len_data
        self._parts.append({'PartNumber': part_num, 'ETag': part['ETag']})
        stream.seek(0)
        stream.truncate()

    def complete(self):
        logger.info('Completing multipart upload {}'.format(self._mpu_id))
        self._compressed.finalize()
        self.upload_data()
        self._compressed.stream.close()

        self._client.complete_multipart_upload(
            Bucket=self._bucket,
            Key=self._key,
            UploadId=self._mpu_id,
            MultipartUpload={'Parts': self._parts}
        )
