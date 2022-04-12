Getting Started
===============

We connect to the API and authenticate, and fetch some data.

.. code-block:: python
    :linenos:

    import asyncio
    from postgrest import AsyncPostgrestClient

    async def main():
        async with AsyncPostgrestClient("http://localhost:3000") as client:
            client.auth("Bearer <token>")
            r = await client.from_("countries").select("*").execute()
            countries = r.data

    asyncio.run(main())


**CRUD**

.. code-block:: python

    await client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()


.. code-block:: python

    r = await client.from_("countries").select("id", "name").execute()
    countries = r.data


.. code-block:: python

    await client.from_("countries").eq("name", "Việt Nam").update({"capital": "Hà Nội"}).execute()

.. code-block:: python

    await client.from_("countries").eq("name", "Việt Nam").delete().execute()

**Calling RPCs**

.. code-block:: python

    await client.rpc("foo").execute()

.. code-block:: python

    await client.rpc("bar", {"arg1": "value1", "arg2": "value2"}).execute()
