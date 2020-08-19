[![](https://img.shields.io/github/license/lqmanh/postgrest-py)](https://github.com/lqmanh/postgrest-py)
[![](https://img.shields.io/pypi/pyversions/postgrest-py)](https://pypi.org/project/postgrest-py)
[![](https://img.shields.io/pypi/v/postgrest-py)](https://pypi.org/project/postgrest-py)
[![](https://img.shields.io/travis/lqmanh/postgrest-py)](https://travis-ci.com/lqmanh/postgrest-py)

# postgrest-py

PostgREST client for Python. This library provides an ORM interface to PostgREST.

Status: **Unstable**

## INSTALLATION

### Requirements

- Python >= 3.7
- PostgreSQL >= 12
- PostgREST >= 7

### Instructions

#### With Poetry (recommended)

```sh
$ poetry add postgrest-py
```

#### With Pip

```sh
$ pip install postgrest-py
```

## USAGE

### Getting started

```py
import asyncio
from postgrest_py import PostgrestClient

async def main():
    async with PostgrestClient("http://localhost:3000") as client:
        r = await client.from_("countries").select("*").execute()
        countries = r.json()

asyncio.run(main())
```

### Create

```py
await client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()
```

### Read

```py
r = await client.from_("countries").select("id", "name").execute()
countries = r.json()
```

### Update

```py
await client.from_("countries").eq("name", "Việt Nam").update({"capital": "Hà Nội"}).execute()
```

### Delete

```py
await client.from_("countries").eq("name", "Việt Nam").delete().execute()
```

### General filters

### Stored procedures (RPC)

## DEVELOPMENT

```sh
$ git clone https://github.com/lqmanh/postgrest-py.git
$ cd postgrest-py
$ poetry install
```

### Testing

```sh
$ poetry run pytest
```

## CHANGELOG

Read more [here](https://github.com/lqmanh/postgrest-py/blob/master/CHANGELOG.md).

## TODO

Read more [here](https://github.com/lqmanh/postgrest-py/blob/master/TODO.md).
