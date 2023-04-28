from greet.greet import greet
from contacts.save_contacts import contacts
from commands_handler.commands import hello, helper, add_contact, del_contact, error_func
from commands_handler.commands import change_phone, show_all, show_phone, good_bye


# Main function

greet()

print("\nTo get help on the commands, please type \"help\"")


def main():

    dict_cmd = {
        "hello": hello,
        "help": helper,
        "add ": add_contact,
        "del ": del_contact,
        "change ": change_phone,
        "phone": show_phone,
        "show all": show_all,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        ".": good_bye
    }

    simple_cmds = ["hello", "help", "good bye", "close", "exit", "."]

    while True:
        command = input("\nEnter command: ").lower().strip()
        for cmd, func in dict_cmd.items():
            if command.startswith(cmd.strip()):
                if cmd.rstrip() in simple_cmds and len(command) == len(cmd.strip()):
                    func()
                else:
                    print(func(command, contacts))
                break
        else:
            print(error_func())


if __name__ == "__main__":
    main()
