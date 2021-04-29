# pipestat_reader - web API generator for pipeline results

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Pipestat reader is a Python package that is an extension of [pipestat](http://pipestat.databio.org/en/latest/).

Pipestat can be used to collect pipeline results and store them in either a YAML-formatted file or in a database. If the results are stored in the database, then pipestat reader can be used to automatically generate a web API to query these results.

# Usage

1. Create a `pipestat.PipestatManager` object

```python
import pipestat

psm = pipestat.PipestatManager(config="/path/to/config.yaml")
```

2. Pass the objects to the `pipestat_reader.PipestatReader` constructor

```python
import pipestat_reader

psr = pipestat_reader.PipestatReader(pipestat_managers=[psm])
```

3. Generate a [GraphQL](https://graphql.org/) schema

```python
graphql_schema = psr.generate_graphql_schema()
```

4. Use the schema in your web application, for example in [FastAPI](https://fastapi.tiangolo.com/):
```python
from fastapi import FastAPI
from starlette.graphql import GraphQLApp

app = FastAPI(title="test app")
app.mount("/graphql", GraphQLApp(schema=graphql_schema, graphiql=True))
```

5. Retrieve the results reported with pipestat

**By `POST` queries**

```console
curl -X POST \
-H "Content-Type: application/json" \
-d '{"query": "{table_name{edges{node{column_name}}}}"}' \
http://0.0.0.0:8000/graphql/
```

**Using the interactive GraphiQL interface at http://0.0.0.0:8000/graphql/**
