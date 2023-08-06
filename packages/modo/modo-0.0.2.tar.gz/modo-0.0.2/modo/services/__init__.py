import click
import logging
from modo.utils.s3 import EncryptedS3Yaml

log = logging.getLogger(__name__)

class SowRose(object):

    def __init__(self, bucket_name, key, version):
        self.bucket_name = bucket_name
        self.key = key
        self.version = version
        self.jinja_context = self._decrypt_jinja_context(bucket_name, key, version)

    def _decrypt_jinja_context(self, bucket_name, key, version):
        jinja_context = EncryptedS3Yaml(bucket_name, key, version)
        return jinja_context.decrypt()

    def run(self):
        log.error('Not Implemented!')
        click.Abort('Not Implemented')

class GrowRose(object):

    def run(self):
        log.error('Not Implemented!')
        click.Abort('Not Implemented')
            