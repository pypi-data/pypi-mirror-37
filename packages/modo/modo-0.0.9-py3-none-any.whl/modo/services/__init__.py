import click
import logging
from modo.utils.s3 import EncryptedS3Yaml

log = logging.getLogger(__name__)


class SowRose(object):

    def __init__(self, bucket_name, object_key, master_key, region, version):
        context = EncryptedS3Yaml(
            bucket_name,
            object_key,
            master_key,
            region,
            version)
        self.jinja_context = context.content

    def run(self):
        log.error('Not Implemented!')
        click.Abort('Not Implemented')


class GrowRose(object):

    def run(self):
        log.error('Not Implemented!')
        click.Abort('Not Implemented')
