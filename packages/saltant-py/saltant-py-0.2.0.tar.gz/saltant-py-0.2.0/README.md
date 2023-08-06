[![Build Status](https://travis-ci.com/saltant-org/saltant-py.svg?branch=master)](https://travis-ci.com/saltant-org/saltant-py)
[![codecov](https://codecov.io/gh/saltant-org/saltant-py/branch/master/graph/badge.svg)](https://codecov.io/gh/saltant-org/saltant-py)
[![Documentation Status](https://readthedocs.org/projects/saltant-py/badge/?version=latest)](https://saltant-py.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/saltant-py.svg)](https://pypi.org/project/saltant-py/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saltant-py.svg)](https://pypi.org/project/saltant-py/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# saltant SDK for Python

saltant-py is a Python SDK for
[saltant](https://github.com/saltant-org/saltant). It lets you perform any
action possible on the saltant API (some much more conveniently) within
the comforts (hopefully) of Python. As a refresher, you might want to
look at [saltant's API reference](https://saltant-org.github.io/saltant/)
to see what actions are possible.

The documentation for saltant-py is fairly comprehensive, and can be
found at
[saltant-py.readthedocs.io](https://saltant-py.readthedocs.io/en/latest/).

## Installation

Using pip,

```
pip install saltant-py
```

or, from source, after cloning this repository, run

```
python setup.py install
```

where `python` is in versions 2.7 or 3.5+.

## Usage

After connecting to the saltant server with

```python
from saltant.client import from_env
client = from_env() # uses env vars
```

or

```python
from saltant.client import Client
client = Client(
    base_api_url='https://shahlabjobs.ca/api/',
    auth_token='p0gch4mp101fy451do9uod1s1x9i4a')
```

You can perform API operations on task types:

```python
# Load in a task type
my_task_type = client.container_task_types.get(id=1)

# Edit the description of the task type
my_task_type.description = "this description is better"

# Push the description upstream
my_task_type.put()
```

You can launch task instances:

```python
# Launch a task instance
my_task_instance = client.container_task_instances.create(
    task_type_id=my_task_type.id,
    task_queue_id=1,
    arguments={"launch_code": 12345},
)

# Wait for the task instance to finish
my_task_instance.wait_until_finished()
```

And much more! (See the docs for more details.)

## See also

[saltant-cli](https://github.com/saltant-org/saltant-cli/), a saltant CLI.
