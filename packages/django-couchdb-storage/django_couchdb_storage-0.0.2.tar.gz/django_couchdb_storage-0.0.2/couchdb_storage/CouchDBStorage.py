from uuid import uuid4
from urllib import parse
from mimetypes import guess_type
from tempfile import TemporaryFile

from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage

import requests


class CouchDBStorage(Storage):
    def __init__(self, **kwargs):
        self.server = '{}/{}/'.format(settings.COUCHDB_HOST, settings.COUCHDB_DATABASE)
        self.user = settings.COUCHDB_USER
        self.password = settings.COUCHDB_PASSWORD

    def get_valid_name(self, name):
        return parse.quote(name).replace('/', '_')

    def get_available_name(self, name, max_length=200):
        return '{}/{}'.format(uuid4(), self.get_valid_name(name))

    def url(self, name):
        return '{}{}'.format(self.server, name)

    def exists(self, name):
        r = requests.head('{}{}'.format(self.server, name))
        if r.status_code == 404:
            return False
        else:
            return True

    def _save(self, name, content):
        mimeType = guess_type(content.name)[0]

        payload = {}
        headers = {'Content-Type': mimeType}

        r = requests.put('{}{}'.format(self.server, name), auth=(self.user, self.password), headers=headers, json=payload, data=content.file)
        return name

    def delete(self, name):
        r = requests.get('{}{}'.format(self.server, name.split('/')[0]), auth=(self.user, self.password))
        rev = r.json()['_rev']
        r = requests.delete('{}{}?rev={}'.format(self.server, name.split('/')[0], rev), auth=(self.user, self.password))
