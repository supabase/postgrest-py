# postgrest_py

PostgREST client for Python. This library provides an ORM interface to PostgREST.

Status: **Unstable**

## INSTALLATION

### Requirements

- Python >= 3.7
- PostgreSQL >= 12
- PostgREST >= 7

### Instructions

#### With Poetry

```sh
$ poetry add git+https://github.com/lqmanh/postgrest_py.git#v0.1.1
```

## USAGE

### Getting started

```py
import asyncio
from postgrest_py import PostgrestClient

async def main():
    async with PostgrestClient("http://localhost:3000") as client:
        r = await client.from_("countries").select("*")
        countries = r.json()

asyncio.run(main())
```

### Create

```py
await client.from_("countries").insert({
    "name": "Việt Nam",
    "capital": "Hà Nội",
})
```

### Read

```py
r = await client.from_("countries").select("id", "name")
countries = r.json()
```

### Update

### Delete

### General filters

### Stored procedures (RPC)

## CHANGELOG

Read more [here](https://github.com/lqmanh/postgrest_py/blob/master/CHANGELOG.md).

## TODO

Read more [here](https://github.com/lqmanh/postgrest_py/blob/master/TODO.md).
