import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_couchdb_storage",
    version="0.0.2",
    author="Dominik Seemann",
    author_email="dominik@seemann.rocks",
    description="Django storage backend for CouchDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5in4/django-couchdb-storage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests>=2.0'],
)
