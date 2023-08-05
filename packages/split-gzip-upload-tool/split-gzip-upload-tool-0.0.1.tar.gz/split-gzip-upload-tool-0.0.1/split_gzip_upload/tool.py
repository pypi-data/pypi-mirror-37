import argparse
import concurrent.futures
import functools
import logging
import sys
from itertools import islice, cycle

import boto3
import botocore.client

from .io import GzipCompressedStream
from .s3 import S3MultipartUpload


logging.basicConfig(format='%(asctime)s [%(levelname)-8s] [%(name)-25s] - %(message)s', level='INFO')
logger = logging.getLogger('split_gzip_upload.tool')


def process(input_fileobj, num_slices, batch_size, bucket, path):
    logger.info('Start processing input')

    cycled_num = cycle(range(num_slices))

    num_workers = 2 * num_slices
    session = boto3.client('s3', config=botocore.client.Config(max_pool_connections=num_workers))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        mpu_create_futures = [
            executor.submit(
                S3MultipartUpload,
                bucket,
                path + '.{}.csv.gz'.format(num),
                GzipCompressedStream(),
                session)
            for num in range(num_slices)
        ]

        mpus = []
        for future in concurrent.futures.as_completed(mpu_create_futures):
            try:
                mpus.append(future.result())
            except Exception:
                # TODO: add abort all of MPUs here
                raise

        upload_futures = set()
        while True:
            batch = islice(input_fileobj, batch_size)
            lines = list(batch)
            if not lines:
                break
            mpu = mpus[next(cycled_num)]
            upload_futures.add(executor.submit(mpu.writelines, lines))
            if len(upload_futures) > num_workers:
                upload_futures.remove(get_first_finished(upload_futures))

        check_all_finished_successfully(upload_futures)
        check_all_finished_successfully(executor.submit(mpu.complete) for mpu in mpus)

    logger.info('Finished processing STDIN')
    logger.info('Uploaded {} bytes in total'.format(sum(mpu.uploaded_bytes for mpu in mpus)))


def check_all_finished_successfully(futures, return_first_finished=False):
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception:
            raise
        else:
            if return_first_finished:
                return future


get_first_finished = functools.partial(check_all_finished_successfully, return_first_finished=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', type=str, required=True, help='S3 bucket name')
    parser.add_argument('--path', type=str, required=True,
                        help='path in S3 bucket, some/path will be converted to '
                             'something like some/path.123.csv.gz, where 123 is a slice number'
                        )
    parser.add_argument('--slices', type=int, default=12, help='number of output slices')
    parser.add_argument('--batch-size', type=int, default=2000, help='number of lines in a batch')

    args = parser.parse_args()
    process(sys.stdin, args.slices, args.batch_size, args.bucket, args.path)
