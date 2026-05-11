# Collaboration

Put any sources (not included in the assignment) that you referenced in doing this assignment. This includes: websites, people you consulted, and (where sanctioned) GenAI prompts and chatlogs. Include a brief sentence on how you used each resource.

## Independent Flask
Implementation Reference:
- Used to guide routing setup: https://flask.palletsprojects.com/en/stable/quickstart/ 
- Used to guide unit testing setup: https://mangohost.net/blog/unit-test-in-flask-writing-tests-for-python-web-apps/

## Independent DB
Implementation Reference
- pandas documentation: https://pandas.pydata.org/docs/reference/api/ Used for creating and editing the DataFrame: read_csv, to_datetime, to_numeric,
dropna, drop_duplicates, and reset_index.
- psycopg2 documentation: https://www.psycopg.org/docs/
    Used for connecting to the PostgreSQL database on Stearns and executing
    parameterized SQL queries with cursor.execute and fetchall.
- Nominatim API documentation: https://nominatim.org/release-docs/latest/api/Search/
    Used for forward geocoding city names to (lat, lon) coordinates.
- PostgreSQL documentation: https://www.postgresql.org/docs/
    Consulted for CREATE TABLE syntax, data types (INTEGER, DATE, REAL, TEXT),
    and the \copy meta-command for bulk CSV loading.