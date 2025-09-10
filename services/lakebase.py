import os
import uuid
import time
import psycopg2
from databricks.sdk import WorkspaceClient
from typing import List, Tuple, Any, Optional


class Lakebase:
    """Singleton Lakebase service for PostgreSQL connections via Databricks SDK"""

    _instance = None
    _connection = None
    _connection_time = 0
    _workspace_client = None
    _database_instance = None
    _token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Lakebase, cls).__new__(cls)
        return cls._instance

    def _is_connection_expired(self) -> bool:
        """Check if connection is older than 59 minutes (3540 seconds)"""
        return time.time() - self._connection_time > 3540

    def _refresh_connection(self):
        """Refresh the database token and create new connection"""
        try:
            # Close existing connection if it exists
            if self._connection:
                self._connection.close()

            # Generate new credential
            cred = self._workspace_client.database.generate_database_credential(
                request_id=str(uuid.uuid4()),
                instance_names=[self._database_instance.name],
            )
            self._token = cred.token

            # Create new connection
            self._connection = psycopg2.connect(
                host=self._database_instance.read_write_dns,
                dbname=os.getenv("LAKEBASE_DB_NAME"),
                user="2025_vibe_coding",  # hardcoded group name
                password=self._token,
                sslmode="require",
            )
            self._connection_time = time.time()

        except Exception as e:
            raise RuntimeError(f"Failed to refresh Lakebase connection: {str(e)}")

    def _ensure_connection(self):
        """Ensure we have a valid connection, creating or refreshing if needed"""
        if self._connection is None:
            # First time initialization
            self._workspace_client = WorkspaceClient(
                client_id=os.getenv("DATABRICKS_CLIENT_ID"),
                client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
            )

            instance_name = os.getenv("LAKEBASE_INSTANCE_NAME")
            if not instance_name:
                raise RuntimeError(
                    "LAKEBASE_INSTANCE_NAME environment variable is required"
                )

            self._database_instance = (
                self._workspace_client.database.get_database_instance(
                    name=instance_name
                )
            )

            self._refresh_connection()

        elif self._is_connection_expired():
            # Connection is expired, refresh it
            self._refresh_connection()

    def query(self, sql: str) -> List[Tuple[Any, ...]]:
        """Execute a SQL query and return the results as rows

        Args:
            sql: The SQL query string to execute

        Returns:
            List of tuples containing the query results

        Raises:
            RuntimeError: If connection fails or query execution fails
        """
        try:
            self._ensure_connection()

            with self._connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                self._connection.commit()
                return rows

        except Exception as e:
            raise RuntimeError(f"Lakebase query failed: {str(e)}")
