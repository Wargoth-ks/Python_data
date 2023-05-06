from termcolor import colored

# This function forming table of contacts and phone numbers

def display_contacts(data):
    if not data:
        return "You have no contacts saved."
    # Define max lenght of name contact & phone number
    max_name_len = max([len(name) for name in data.keys()] + [4])
    max_phone_len = max([len(str(phone)) for phone in data.values()] + [13])

    # Header of table
    table = f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+\n'
    table += f'| {"Name":<{max_name_len}} | {"Phone number":<{max_phone_len}} |\n'
    table += f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+\n'

    # Data of table
    for name, phone in data.items():
        table += f'| {name:<{max_name_len}} | {phone:<{max_phone_len}} |\n'

    # Generating the table footer
    table += f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+'

    return colored(table, "cyan")
