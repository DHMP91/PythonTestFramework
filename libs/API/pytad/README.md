# To Generate a new client
1. Copy new schema.yml (https://github.com/DHMP91/PyTAD/blob/main/schema.yml) to tests/api/pytad
2. CD to PythonTestFramework
3. In Projects python venv run
```
openapi-python-client generate --path "libs\\API\\pytad\\schema.yml" --output-path  "libs\\API\\pytad\\client" --overwrite
```
