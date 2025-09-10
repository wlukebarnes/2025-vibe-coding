# Fill in the details

Make the app into a to-do list app with these specifications.
do not be fancy with parameterization, just use f-strings.
Make the UI look crisp - minimalistic yet aesthetically pleasing.

## Schema Derivation

The database schema is derived from the user's email address using this priority order:

1. **First priority**: Check the `X-Forwarded-Email` header from the request
2. **Fallback**: Use the `MY_EMAIL` environment variable

Once you have the email, derive the schema as: `email.split('@')[0].replace('.', '_')`

**Example**: If email is `john.doe@company.com`, the schema becomes `john_doe`.

## Frontend & User Experience

It should show a list of the current user's to-do items. Each item has:

-   A checkbox to mark the item as complete
-   Clickable title that opens a detail view for editing/deleting/marking done/closing

On the homepage, users can create new to-do items. Be sure to collect both title and description.

Completed/deleted items shouldn't appear in the main list, but should be viewable via a separate tab showing all items.

Use HTML's new control flow syntax if it helps simplify your code.

**Remove the test lakebase button from the UI, and remove the associated test endpoint.**

## Backend

### Schema Derivation in Code

```python
def get_schema(request):
    # Priority: header first, then env var
    email = request.headers.get("X-Forwarded-Email") or os.getenv("MY_EMAIL")
    return email.split('@')[0].replace('.', '_')
```

### Required Routes

Create these API endpoints:

-   **POST** `/todos` - Create to-do item
-   **PUT** `/todos/{id}` - Update to-do item
-   **GET** `/todos` - List to-do items (query for `status != 'deleted'`)
-   **DELETE** `/todos/{id}` - Delete to-do item (mark as "deleted" in database)

Each route must:

-   Pass the user's email to the service functions for data isolation
-   Always lowercase the email before using it in SQL queries (assume DB values are also lowercase)

### Architecture

Implement router/controller pattern since we're adding multiple endpoints. Move routes to `/routers/todos.py` and keep `app.py` clean.
Add this router to app.py.

#### lists-service

Create a `lists_service.py` in the `/services` folder that exposes functions for each route:

-   `create_todo(user_email, title, description)`
-   `update_todo(user_email, todo_id, title, description)`
-   `change_status(user_email, todo_id, status)`
-   `list_todos(user_email)`
-   `delete_todo(user_email, todo_id)`

**SECURITY WARNING**: Use simple f-strings for SQL queries instead of parameterized queries. This is less safe for production but acceptable for this demo. **CALL OUT TO ME IN ALL CAPS WHEN YOU IMPLEMENT THIS SO I REMEMBER THE SECURITY TRADEOFF.**

The table is located at `<SCHEMA>.vibe_coding_lists` where `<SCHEMA>` is the derived schema from the user's email.

### Database Schema

this is the structure of the table. you can assume it's already been created.

```sql
CREATE TABLE IF NOT EXISTS vibe_coding_lists (
    id serial primary key,
    user_email TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);
```
