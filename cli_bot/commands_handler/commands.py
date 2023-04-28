
from decorator.decorator import input_error
from contacts.display_contacts import display_contacts
from display_help.display_help import display_help

# Processing input commands


@input_error
def hello():
    print("How can I help you?")


@input_error
def good_bye():
    print("\n Bye bye!")
    exit()


@input_error
def helper():
    print(display_help())


@input_error
def error_func():
    raise ValueError("Command not found. Please, try again!")


@input_error
def add_contact(command, contacts):
    keys = command.split()
    if len(keys) != 3:
        raise ValueError("Error!!! You must input 'add <name> <phone>'!")
    if len(keys[0]) != 3 or keys[0] != "add":
        raise ValueError("Command not found. Please, try again!")
    name, phone = keys[1], keys[2]
    if name in contacts:
        raise ValueError(
            f"Contact << {name.capitalize()} >> is already in address book!")
    if all(symb.isdigit() or symb in ['+', '-'] for symb in phone):
        contacts[name] = phone
        return f"Contact << {name.capitalize()} >> has been added to your contacts."
    else:
        raise ValueError(
            "Phone number should contain only digits, plus (+) or minus (-) signs.")


@input_error
def del_contact(command, contacts):
    if len(command.split()) != 2:
        raise ValueError("Error!!! You must input 'del <name>'!")
    name = command.split()[1]
    if name not in contacts:
        raise ValueError(
            f"Contact << {name.capitalize()} >> not found. Please, try again!")
    del contacts[name]
    return f"{name} has been removed from your contacts."


@input_error
def change_phone(command, contacts):
    keys = command.split()
    if len(keys) != 3:
        raise ValueError("Error!!! You must input 'change <name> <phone>'!")
    if len(keys[0]) != 6 or keys[0] != "change":
        raise ValueError("Command not found. Please, try again!")
    name, phone = keys[1], keys[2]
    if name not in contacts:
        raise ValueError(
            f"Contact << {name.capitalize()} >> not found. Please, try again!")
    if all(symb.isdigit() or symb in ['+', '-'] for symb in phone):
        contacts[name] = phone
        return f"Phone number for << {name.capitalize()} >> has been updated."
    else:
        raise ValueError(
            "Phone number should contain only digits, plus (+) or minus (-) signs.")


@input_error
def show_phone(command, contacts):
    if len(command.split()) != 2:
        raise ValueError("Error!!! You must input 'phone <name>'!")
    name = command.split()[1]
    if name not in contacts:
        raise ValueError(
            f"Contact << {name.capitalize()} >> not found. Please, try again!")
    return f"The phone number for << {name.capitalize()} >> is << {contacts[name]} >>."


@input_error
def show_all(command, contacts):
    _ = command.strip()
    if not contacts:
        return "You have no contacts saved."
    elif len(command) == 8:
        return display_contacts(contacts)
    else:
        raise ValueError("Command not found! Try 'help' for a list command")
    # return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
