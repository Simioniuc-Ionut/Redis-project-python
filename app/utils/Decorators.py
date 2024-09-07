# app/utils/Decorators.py

def debug(func):
    def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ if args else ''
        print(f"Calling {class_name}class.{func.__name__} with args: {args[1:]} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{class_name}.with func name .{func.__name__} returned: {result}")
        return result

    return wrapper


def debug_process_with_dict(func):
    def wrapper(*args, **kwargs):
        instance = args[0]  # Obținem instanța clasei
        debug_dict = kwargs.get('debug_dict', {})

        print(f"Calling {instance.__class__.__name__}.{func.__name__}")

        # Afișează valorile variabilelor din dicționarul de debug
        for var_name, value in debug_dict.items():
            print(f"DEBUG: {var_name} = {value}")

        # Apelăm funcția originală
        result = func(*args, **kwargs)

        print(f"{instance.__class__.__name__}.{func.__name__} completed")
        return result

    return wrapper
