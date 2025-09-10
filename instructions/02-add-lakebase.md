https://apps-cookbook.dev/docs/fastapi/getting_started/lakebase_connection

# Add a Databricks Lakebase connection (Postgres protocol) via psycopg2

We are connecting to a Lakebase database using the Postgres wire protocol with `psycopg2`, and obtaining a short‑lived database token from the Databricks SDK. Keep it minimal and implement it as a singleton service that exposes `Lakebase.query(sql: str)`.

Environment variables available (used by the Databricks SDK and the connection):

-   `DATABRICKS_HOST` (includes `https://`)
-   `DATABRICKS_CLIENT_ID`
-   `DATABRICKS_CLIENT_SECRET`
-   `LAKEBASE_INSTANCE_NAME`
-   `LAKEBASE_DB_NAME`

Add a button to index.html that selects NOW() from lakebase and displays it in the ui.

Minimal example:

```python
import os
import uuid
import psycopg2
from databricks.sdk import WorkspaceClient

w = WorkspaceClient(
    client_id=os.getenv("DATABRICKS_CLIENT_ID"),
    client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
)
instance_name = os.getenv("LAKEBASE_INSTANCE_NAME")
db_name = os.getenv("LAKEBASE_DB_NAME")
db_user = "2025_vibe_coding"  # this is a group name, fine to leave hard-coded

cred = w.database.generate_database_credential(
    request_id=str(uuid.uuid4()), instance_names=[instance_name]
)
instance = w.database.get_database_instance(name=instance_name)

conn = psycopg2.connect(
    host=instance.read_write_dns,
    dbname=db_name,
    user=db_user,
    password=cred.token,
    sslmode="require",
)
with conn, conn.cursor() as cur:
    cur.execute("SELECT 1;")
    rows = cur.fetchall()
    conn.commit()
    return rows
```

Implementation notes:

-   Wrap this logic in a `services/lakebase.py` singleton. On first `query()`, open the connection; if the connection is older than 59 minutes, refresh the token and reconnect; return rows as‑is.
-   Do not transform results or wrap them in dataframes.
-   For the username on the Lakebase connection, use the hardcoded group from above.
-   Only initialize upon first time trying to use it.
