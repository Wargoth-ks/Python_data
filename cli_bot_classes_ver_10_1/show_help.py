# This function show help in table

from termcolor import colored

def show_help():

    cmd_help = {
        "hello": "Say hello",
        "help": "Show this help",
        "add <name> <number>": "Add contact and number",
        "add_phone <number>": "Add new number to contact",
        "add_bd <birthday>": "Add birthday - DD.MM.YYY to contact",
        "del <name>": "Remove contact",
        "del_phone <number>": "Remove contact's number",
        "del_bd <name>": "Remove contact's birthday - DD.MM.YYYY",
        "change <old name>, <new_name>": "Update contact's name",
        "change_phone <name> <new number>": "Change contact's phone number",
        "upd_bd <name> <birthday>": "Change contact's birthday - DD.MM.YYYY",
        "get_bd <name> <birthday>": "Get days to contact's birthday - DD.MM.YYYY",
        "by_name <name>": "Search contact's info by name",
        "by_name <phone>": "Search contact's info by phone",
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