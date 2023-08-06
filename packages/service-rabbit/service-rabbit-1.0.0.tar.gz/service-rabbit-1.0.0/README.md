[![Build Status](https://travis-ci.org/puntonim/service-rabbit.svg?branch=master)](https://travis-ci.org/puntonim/service-rabbit)

# Rabbit service client

This package is service client for Rabbit API.

## Client usage

```python
# Configure settings.
import service_rabbit.conf
d = dict(
    BASE_URL='http://inspire-prod-broker1.cern.ch:15672/api',
    REQUEST_TIMEOUT=30,
    HTTP_AUTH_USERNAME='user',
    HTTP_AUTH_PASSWORD='pass',
)
service_rabbit.conf.settings.configure(**d)

# Use the client.
from service_rabbit.client import RabbitClient
client = RabbitClient()
response = client.get_queue('inspire', 'orcid_push')
response.raise_for_result()
consumers = response.get_consumers_count()
messages = response.get_messages_count()
```

## Development

```bash
# Create a venv and install the requirements:
$ make venv

# Run isort and lint:
$ make isort
$ make lint

# Run all the tests:
$ make test  # tox against Python27 and Python36.
$ tox -e py27  # tox against a specific Python version.
$ pytest  # pytest against the active venv.

# Run a specific test:
$ make test/tests/test_client.py  # tox against Python27 and Python36.
$ tox -e py27 -- tests/test_client.py  # tox against a specific Python version.
$ pytest tests/test_client.py  # pytest against the active venv.
```

To publish on PyPi, first set the PyPi credentials:

```bash
# Edit .pypirc:
$ cat $HOME/.pypirc
[pypi]
username: myuser
password: mypass
```

```bash
# Edit the version in `setup_gen.py`.
# ... version=pep440_version('1.1.1'),
# Then generate setup.py with:
$ make setup.py
# Commit, tag, push:
$ git commit -m '1.1.1 release'
$ git tag 1.1.1
$ git push origin master --tags

# Finally publish:
$ make publish
```
