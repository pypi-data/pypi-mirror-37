# A couchdb storage backend for Django

For each upload, a new document with the file attached is created.

## Setup

Install this package with pip:

`pip install -U django-couchdb-storage` 

Add it to your INSTALLED_APPS in django settings:

```python
INSTALLED_APPS = [
    ...

    'couch',
]
```

And and configuration to point django to your couchdb:

```python
DEFAULT_FILE_STORAGE = 'couchdb_storage.CouchDBStorage'
COUCHDB_HOST = 'http://127.0.0.1:5984'
COUCHDB_DATABASE = 'django_storage'
COUCHDB_USER = ''
COUCHDB_PASSWORD = ''
```

## Constraints

Right now, this package assumes that content from the storage database can be read anonymously. Writes are authenticated. It is also assumed, that the db host can be accessed publicly.
