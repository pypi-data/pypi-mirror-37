import boto3
import yaml
import base64
from jinja2 import Template
from io import BytesIO

class EncryptedS3Yaml(object):

    def __init__(self, bucket, key, version=None):
        self.bucket = bucket
        self.key = key
        self.version = version
        self.content = self._decrypt(self._pull_object_as_dict(bucket, key, version))

    def _pull_object_as_dict(self, bucket, key, version):
        s3 = boto3.resource('s3')
        s3_object = s3.Object(bucket, key)
        object_buffer = BytesIO()
        s3_object.download_fileobj(object_buffer)
        return object_buffer.getvalue().decode('utf-8')

    def _decrypt(self, encrypted_content):
        """
        decrypts values in secrets section created by
        aws kms encrypt --key-id <keyid> --plaintext wtf --output text --query CiphertextBlob | base64 --decode
        """
        kms = boto3.client('kms')
        template = Template(encrypted_content)
        secrets = yaml.load(encrypted_content).get('secrets', {})
        for key, value in secrets.items():
            plaintext_raw = kms.decrypt(CiphertextBlob=bytes(base64.b64decode(value))).get('Plaintext')
            plaintext = plaintext_raw.decode('utf-8')
            secrets[key] = plaintext

        content = yaml.load(template.render(secrets=secrets))
        content.pop('secrets')
        return content

