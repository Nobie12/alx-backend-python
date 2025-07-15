from datetime import datetime
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else "UNKNOWN QUERY")
        print(f"[{datetime.now()}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

