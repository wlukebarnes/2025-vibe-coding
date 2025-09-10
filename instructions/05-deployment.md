## app.yaml

https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-runtime. Listen to my instructions and use my configurations if they differ from the article.

this app will be deployed on databricks. create a databricks `app.yaml` using the documentation. Use the docs to determine the command section, this is a FastAPI app, and our main file is called app.py.

for the env section, include only the variables used by this app and Lakebase:

-   DATABRICKS_HOST
-   LAKEBASE_INSTANCE_NAME
-   LAKEBASE_DB_NAME

Get the values from `example.env` and add them here. They should be of this type:

-   name: {name of env var}
-   value: {value of env var}x

There should only be command: and env: sections.
