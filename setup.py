# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postgrest', 'postgrest._async', 'postgrest._sync']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0', 'httpx>=0.23.0,<0.24.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'postgrest-py',
    'version': '0.10.3',
    'description': 'PostgREST client for Python. This library provides an ORM interface to PostgREST.',
    'long_description': '# postgrest-py\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?label=license)](https://opensource.org/licenses/MIT)\n[![CI](https://github.com/supabase-community/postgrest-py/actions/workflows/ci.yml/badge.svg)](https://github.com/supabase-community/postgrest-py/actions/workflows/ci.yml)\n[![Python](https://img.shields.io/pypi/pyversions/postgrest-py)](https://pypi.org/project/postgrest-py)\n[![Version](https://img.shields.io/pypi/v/postgrest-py?color=%2334D058)](https://pypi.org/project/postgrest-py)\n[![Codecov](https://codecov.io/gh/supabase-community/postgrest-py/branch/master/graph/badge.svg)](https://codecov.io/gh/supabase-community/postgrest-py)\n[![Last commit](https://img.shields.io/github/last-commit/supabase-community/postgrest-py.svg?style=flat)](https://github.com/supabase-community/postgrest-py/commits)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/supabase-community/postgrest-py)](https://github.com/supabase-community/postgrest-py/commits)\n[![Github Stars](https://img.shields.io/github/stars/supabase-community/postgrest-py?style=flat&logo=github)](https://github.com/supabase-community/postgrest-py/stargazers)\n[![Github Forks](https://img.shields.io/github/forks/supabase-community/postgrest-py?style=flat&logo=github)](https://github.com/supabase-community/postgrest-py/network/members)\n[![Github Watchers](https://img.shields.io/github/watchers/supabase-community/postgrest-py?style=flat&logo=github)](https://github.com/supabase-community/postgrest-py)\n[![GitHub contributors](https://img.shields.io/github/contributors/supabase-community/postgrest-py)](https://github.com/supabase-community/postgrest-py/graphs/contributors)\n\nPostgREST client for Python. This library provides an ORM interface to PostgREST.\n\nStatus: **Unstable**\n\n## INSTALLATION\n\n### Requirements\n\n- Python >= 3.7\n- PostgreSQL >= 12\n- PostgREST >= 7\n\n### Local PostgREST server\n\nIf you want to use a local PostgREST server for development, you can use our preconfigured instance via Docker Compose.\n\n```sh\ndocker-compose up\n```\n\nOnce Docker Compose started, PostgREST is accessible at <http://localhost:3000>.\n\n### Instructions\n\n#### With Poetry (recommended)\n\n```sh\npoetry add postgrest-py\n```\n\n#### With Pip\n\n```sh\npip install postgrest-py\n```\n\n## USAGE\n\n### Getting started\n\n```py\nimport asyncio\nfrom postgrest import AsyncPostgrestClient\n\nasync def main():\n    async with AsyncPostgrestClient("http://localhost:3000") as client:\n        r = await client.from_("countries").select("*").execute()\n        countries = r.data\n\nasyncio.run(main())\n```\n\n### Create\n\n```py\nawait client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()\n```\n\n### Read\n\n```py\nr = await client.from_("countries").select("id", "name").execute()\ncountries = r.data\n```\n\n### Update\n\n```py\nawait client.from_("countries").update({"capital": "Hà Nội"}).eq("name", "Việt Nam").execute()\n```\n\n### Delete\n\n```py\nawait client.from_("countries").delete().eq("name", "Việt Nam").execute()\n```\n\n### General filters\n\n### Stored procedures (RPC)\n```py\nawait client.rpc("foobar", {"arg1": "value1", "arg2": "value2"}).execute()\n```\n\n## DEVELOPMENT\n\n```sh\ngit clone https://github.com/supabase/postgrest-py.git\ncd postgrest-py\npoetry install\npoetry run pre-commit install\n```\n\n### Testing\n\n```sh\npoetry run pytest\n```\n\n## CHANGELOG\n\nRead more [here](https://github.com/supabase/postgrest-py/blob/master/CHANGELOG.md).\n\n## SPONSORS\n\nWe are building the features of Firebase using enterprise-grade, open source products. We support existing communities wherever possible, and if the products don’t exist we build them and open source them ourselves. Thanks to these sponsors who are making the OSS ecosystem better for everyone.\n\n[![Worklife VC](https://user-images.githubusercontent.com/10214025/90451355-34d71200-e11e-11ea-81f9-1592fd1e9146.png)](https://www.worklife.vc)\n[![New Sponsor](https://user-images.githubusercontent.com/10214025/90518111-e74bbb00-e198-11ea-8f88-c9e3c1aa4b5b.png)](https://github.com/sponsors/supabase)\n',
    'author': 'Gijs Addas',
    'author_email': 'gijsaddas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gijsaddas/postgrest-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
