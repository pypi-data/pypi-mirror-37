import boto3
import yaml
from jinja2 import Template
from io import BytesIO
from base64 import b64decode

class EncryptedS3Yaml(object):

    def __init__(self, bucket, object_key, master_key, region, version=None):
        self.bucket = bucket
        self.object_key = object_key
        self.version = version
        self.session = boto3.session.Session(region_name=region)
        self.content = self._pull_object_as_dict(bucket, object_key, master_key, version)

    def _pull_object_as_dict(self, bucket, object_key, master_key, version):
        s3 = self.session.resource('s3')
        s3_object = s3.Object(bucket, object_key)
        object_buffer = BytesIO()
        s3_object.download_fileobj(object_buffer)
        content = object_buffer.getvalue().decode('utf8')
        content_dict = yaml.load(self._render_template(content, master_key))
        content_dict.pop('secrets', {})
        return content_dict

    def _render_template(self, content, master_key):
        encrypted_context = yaml.load(content)
        context = {}
        for key, value in encrypted_context.get('secrets', {}).items():         
            context[key] = self._decrypt(value, master_key)  
        template = Template(content)
        return template.render(secrets=context)

    def _decrypt(self, encrypted_content, master_key):
        """
        decrypts using aws encryption sdk
        """
        client = self.session.client('kms')
        plaintext = client.decrypt(
            CiphertextBlob=bytes(b64decode(encrypted_content))
        )
        return plaintext["Plaintext"]

