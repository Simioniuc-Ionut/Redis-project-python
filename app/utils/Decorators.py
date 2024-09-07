
def debug(func):
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ if args else ''
        print(f"Calling {class_name}.{func.__name__} with args: {args[1:]} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{class_name}.{func.__name__} returned: {result}")
        return result
    return wrapper