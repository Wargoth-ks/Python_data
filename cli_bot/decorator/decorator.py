
# Decorator

def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError as key:
            return f"Key Error: {key}"
        except ValueError as val:
            return f'Value Error: {val}'
        except IndexError as ind:
            return f'Index Error: {ind}'
        except TypeError:
            return f"Command not found. Please, try again!"
        except Exception as e:
            return f"Error: {e}"
    return inner
