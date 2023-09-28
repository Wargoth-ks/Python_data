from termcolor import colored
from datetime import datetime
import re

# Decorator & validators


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as key:
            return "Key Error: " + colored(f"<< {key} >>", "red")
        except ValueError as val:
            return "Value Error: " + colored(f"<< {val} >>", "red")
        except IndexError as ind:
            return "Index Error: " + colored(f"<< {ind} >>", "red")
        except TypeError as type:
            return "Type Error: " + colored(f"<< {type} >>", "red")
        except Exception as e:
            return "Exception Error: " + colored(f"<< {e} >>", "red")

    return inner


def validation_exists_name(contacts):
    def decorator(func):
        def wrapper(name, *args, **kwargs):
            if name not in contacts and name.replace(",", "") not in contacts:
                raise ValueError(
                    f"Decorator: Contact << {name} >> not found in phone book!!!"
                )
            return func(name, *args, **kwargs)

        return wrapper

    return decorator


def validation_parametrs(func):
    def wrapp(*args, **kwargs):
        date_arg = re.match(
            r"^(0[1-9]|1[0-9]|2[0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$", args[-1]
        )
        if len(args) >= 2:
            if re.match(r"^[+\-\d]+$", args[-1]):
                dig_arg = str(args[-1])
                args = [" ".join(args[:-1]), dig_arg]
                # print(f"Decorator validate phone: {args}")
            elif not re.match(r"^[+\-\d]+$", args[-2]) and date_arg:
                date_arg = datetime.strptime(args[-1], "%d.%m.%Y").date()
                args = [" ".join(args[:-1]), date_arg]
                # print(f"Decorator add_bd: {args}")
            elif re.match(r"^[+\-\d]+$", args[-2]) and date_arg:
                date_arg = datetime.strptime(args[-1], "%d.%m.%Y").date()
                dig_arg = str(args[-2])
                args = [" ".join(args[:-2]), dig_arg, date_arg]
                # print(f"Decorator validate phone, bd: {args}")
            elif any(re.findall(",", arg) for arg in args):
                args_str = " ".join(args)
                args = [s.strip() for s in args_str.split(",", 1)]
                # print(f"Decorator validate name: {args}")
            elif not re.match(r"^[+\-\d]+$", args[-2]) and not date_arg:
                args_str = " ".join(args)
                args = [args_str.strip()]
                # print(f"Decorator get_bd, del_bd, upd_bd, del contact: {args}")
            else:
                raise ValueError("Decorator: Error!!!")
        return func(*args, **kwargs)

    return wrapp
