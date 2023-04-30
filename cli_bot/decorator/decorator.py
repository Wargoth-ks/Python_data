from termcolor import colored
# Decorator

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as key:
            return ("Key Error: " + colored(f"<< {key} >>", "red"))
        except ValueError as val:
            return ("Value Error: " + colored(f"<< {val} >>", "red"))
        except IndexError as ind:
            return ("Index Error: " + colored(f"<< {ind} >>", "red"))
        except TypeError as type:
            return ("Type Error: " + colored(f"<< {type} >>", "red"))
        except Exception as e:
            return ("Exception Error: " + colored(f"<< {e} >>", "red"))
    return inner


