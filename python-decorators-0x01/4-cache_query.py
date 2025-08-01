import time
import sqlite3 
import functools


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect("users.db") as conn:
            return func(conn, *args, **kwargs)

    return wrapper


query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Try to get the query string from kwargs or args[0]
        query = kwargs.get("query") or (args[0] if args else None)

        if query is None:
            raise ValueError("Missing SQL query string to cache.")

        # Check cache
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]

        # Otherwise, execute the query and cache the result
        print(f"[CACHE MISS] Executing and caching result for: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
