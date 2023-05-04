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

simple_cmds = ["show all", "good bye", "close", "exit", ".", "help", "hello"]

def parse_input(user_input):
    command, *data = user_input.strip().split(' ', 1)
    if user_input in simple_cmds:
        simple_func = dict_cmd[user_input.strip()]
        print(simple_func())
    elif not user_input or user_input.split()[0] not in dict_cmd.keys():
        print(error_func())
    else:
        if user_input.split()[0] in dict_cmd.keys() and len(user_input.split()) > 1:
            args = data[0].split(" ")
            handler = dict_cmd[command]
            if len(args) >= 2:
                if all(symb.isdigit() or symb in ['+', '-'] for symb in args[-1]):
                    dig_arg = str(args[-1])
                    list_args = [" ".join(args[:-1]), dig_arg]
                    return handler, list_args
            if len(data) == 1: 
                return handler, data
        else:
            print("Type Error: " + colored(f"<< Command << {user_input} >> must have any arguments !!! >>", "red"))

def main():
    while True:
        user_input = input(colored("\nEnter command: ", "green"))
        try:
            func, args = parse_input(user_input)
            _args = args[0]
            if len(_args) >= 2:
                print(func(*args))
            if len(_args) == 1:
                print(func(_args))
        except TypeError:
            continue

if __name__ == "__main__":
    greet()
    main()
