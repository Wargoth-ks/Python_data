
from decorator.decorator import input_error

from contacts.display_contacts import display_contacts
from display_help.display_help import display_help
from termcolor import colored
from contacts.save_contacts import contacts
# Processing input commands


@input_error
def hello():
    return "How can I help you?"


@input_error
def good_bye():
    print("\n Bye bye!")
    exit()


@input_error
def helper():
    return display_help()


@input_error
def error_func():
    raise ValueError(colored(f"<< Command not found. Please, try again! >>", "red"))

@input_error
def add_contact(name, phone):
    if all(symb.isdigit() or symb in ['+', '-'] for symb in phone):
        contacts[name] = phone
        return f"Contact << {name} >> has been added to the phone book!"
    else:
        return "Value Error:" + colored(" Phone number should contain only digits, plus (+) or minus (-) signs", "red")


@input_error
def del_contact(name):
    if name in contacts:
        del contacts[name]
        return f"Contact << {name} >> has been removed from phone book"
    else:
        return f"Contact << {name} >> not found. Please, try again!"


@input_error
def change_phone(name, phone):
    if name not in contacts:
        return f"contact << {name} >> not found"
    elif all(symb.isdigit() or symb in ['+', '-'] for symb in phone):
        contacts[name] = phone
        return f"Phone number for << {name} >> has been updated"
    else:
        print(f"Phone << {phone} >> should contain only digits, plus (+) or minus (-) signs.")


@input_error
def show_phone(name):
    if name not in contacts:
        return f"Contact << {name} >> not found. Please, try again!"
    else:
        return f"The phone number for << {name} >> is << {contacts[name]} >>"


@input_error
def show_all():
    if not contacts:
        return "<< You have no contacts saved >>"
    else:
        return display_contacts(contacts)

    # return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
