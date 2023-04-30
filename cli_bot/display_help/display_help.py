# This function show help in table

from termcolor import colored

def display_help():

    cmd_help = {
        "hello": "Say hello",
        "add <name> <number>": "Add contact and number",
        "del <name>": "Remove contact",
        "change <name> <new number>": "Change contact's phone number",
        "phone <name>": "Show phone number for a contact",
        "show all": "Show all contacts",
        "good bye, exit, close or .": "Exit program"
    }

    max_name_len = max([len(cmds) for cmds in cmd_help.keys()] + [4])
    max_phone_len = max([len(desc) for desc in cmd_help.values()] + [6])

    # Header of table
    table = f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+\n'
    table += "|{:^62}|\n".format("Bot's command")

    # Header of table
    table += f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+\n'
    table += f'| {"Command":<{max_name_len}} | {"Description":<{max_phone_len}} |\n'
    table += f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+\n'

    # Data of table
    for cmd, desc in cmd_help.items():
        table += f'| {cmd:<{max_name_len}} | {desc:<{max_phone_len}} |\n'

    # Generating the table footer
    table += f'+{"-" * (max_name_len + 2)}+{"-" * (max_phone_len + 2)}+'
    return colored(table, "magenta")

print()