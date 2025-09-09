# Fill in the details

Make the app into a to-do list app with these specifications.
do not be fancy with parameterization, just use f-strings.
Make the UI look crisp - minimalistic yet aesthetically pleasing.

You must derive schema from MY_EMAIL env var, as MY_EMAIL.split('@')[0].replace('.', '\_'). Sometimes, this will be provided in a header instead and you will need to fetch it from there, which is explained in the backend section.

### Frontend & user experience

It should show a list of the current user's to-do's. There's a checkbox to mark a to-do item's status as complete. They can click on the item's name to blow it up, where they can edit it or delete it or mark it as done or just close. On the homepage they should also be able to create a new to do list. Completed/deleted to-dos shouldn't appear in the main list, but you should be able to see them by clicking on another tab to show all. Use HTML's new control flow syntax if you need it to simplify your code. Be sure to collect title and description from the user.

### backend

The proper header to check for the email is located at `request.headers.get("X-Forwarded-Email")`. if it's not provided, it checks the .env variable 'MY_EMAIL'. This is the input to table's schema calculation, which is described above. The header takes priority.

you need to make routes for:

-   Create to-do item
-   Update to-do item
-   List to-do items (which queries for state != deleted)
-   Delete to-do items (which simply marks them as "deleted" in the database)

these routes will pass the user's email to the functional services so we can be sure people can only see their own to-do items. always lowercase the provided python variable for email before inserting it into the sql query. its assumed the values in the db are too.

#### lists-service

lists-service should expose functions for each of the routes above. it should use Lakebase.query() under the hood with specific queries (don't bother with parameterization, just use simple f-strings. call out to me that you've done this even though it is less safe in production settings. please use all caps when telling me so I remember). the lists table is located at <SCHEMA>.vibe_coding_lists.

lists are defined as:
CREATE TABLE IF NOT EXISTS vibe_coding_lists (
id serial primary key,
user_email TEXT NOT NULL,
title TEXT NOT NULL,
description TEXT,
status TEXT NOT NULL DEFAULT 'pending',
created_at TIMESTAMP NOT NULL DEFAULT now(),
updated_at TIMESTAMP NOT NULL DEFAULT now()
);
