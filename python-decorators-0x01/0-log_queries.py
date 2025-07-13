def log_queries():
    def decorator(func):
        def wrapper(*args, **kwargs):
            query = args[0] if args else kwargs.get('query', '')
            print(f"Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

