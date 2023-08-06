# 🤒 pyflunearyou: A Python3 API for Flu Near You

[![Travis CI](https://travis-ci.org/bachya/pyflunearyou.svg?branch=master)](https://travis-ci.org/bachya/pyflunearyou)
[![PyPi](https://img.shields.io/pypi/v/pyflunearyou.svg)](https://pypi.python.org/pypi/pyflunearyou)
[![Version](https://img.shields.io/pypi/pyversions/pyflunearyou.svg)](https://pypi.python.org/pypi/pyflunearyou)
[![License](https://img.shields.io/pypi/l/pyflunearyou.svg)](https://github.com/bachya/pyflunearyou/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/pyflunearyou/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pyflunearyou)
[![Maintainability](https://api.codeclimate.com/v1/badges/dee8556060c7d0e7f2d1/maintainability)](https://codeclimate.com/github/bachya/pyflunearyou/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`pyflunearyou` is a simple Python library for retrieving UV-related information
from [Flu Near You](https://flunearyou.org/#!/).

# Installation

```python
pip install pyflunearyou
```

# Python Versions

`pyflunearyou` is currently supported on:

* Python 3.5
* Python 3.6
* Python 3.7

However, running the test suite currently requires Python 3.6 or higher; tests
run on Python 3.5 will fail.

# API Key

# Usage

`pyflunearyou` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession

from pyflunearyou import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client and get to work:

```python
import asyncio

from aiohttp import ClientSession

from pyflunearyou import create_client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      client = await create_client(<LATITUDE>, <LONGITUDE>, websession)

      # Get user data for the client's latitude/longitude:
      await client.user_reports.status()

      # Get user data for the a specific ZIP code:
      await client.user_reports.status_by_zip("90046")

      # Get CDC data for the client's latitude/longitude:
      await client.cdc_reports.status()

      # Get CDC data for North Dakota
      await client.cdc_reports.status_by_state('North Dakota')

asyncio.get_event_loop().run_until_complete(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/pyflunearyou/issues)
  or [initiate a discussion on one](https://github.com/bachya/pyflunearyou/issues/new).
2. [Fork the repository](https://github.com/bachya/pyflunearyou/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
