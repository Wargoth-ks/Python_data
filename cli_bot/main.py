from termcolor import colored
from greet.greet import greet

from commands_handler.commands import hello, helper, add_contact, del_contact, error_func
from commands_handler.commands import change_phone, show_all, show_phone, good_bye

dict_cmd = {
        "hello": hello,
        "help": helper,
        "add": add_contact,
        "del": del_contact,
        "change": change_phone,
        "phone": show_phone,
        "show all": show_all,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
        ".": good_bye
    }

def parse_func(user_input):
    command, *args = user_input.split()
    command = command.lstrip()

    try:
        handler = dict_cmd[command.lower()]
    except KeyError:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
        handler = dict_cmd.get(command.lower(), error_func)

    return handler, args

# Main function

def main():
    while True:
        user_input = input(colored("\nEnter command: ", "green"))
        if not user_input:
            handler, *args = error_func, "No command entered"
        else:
            print(colored("You entered: ", "yellow"), colored(f"{user_input}", "white"))
            handler, *args = parse_func(user_input)
        result = handler(*args)
        if result:
            print(handler(*args))

if __name__ == "__main__":
    greet()
    main()

